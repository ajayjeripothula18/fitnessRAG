"""
Tests for RequestBodyLimitMiddleware.
"""
from typing import List
import pytest
from starlette.types import Message, Receive, Scope, Send

from app.middleware.request_body_limit import (
    PayloadTooLargeException,
    RequestBodyLimitMiddleware,
)

# Constant test limit: 6 MiB (matching ingestion route threshold)
MAX_SIZE = 6 * 1024 * 1024
TARGET_PATH = "/api/v1/ingestion/file"


class RecordingASGIApp:
    """
    Small ASGI test application that explicitly calls the supplied receive()
    until the request body is complete (or client disconnects) before returning
    its response.
    """

    def __init__(
        self,
        response_status: int = 200,
        response_body: bytes = b"OK",
    ) -> None:
        self.called: bool = False
        self.executed: bool = False
        self.completed: bool = False
        self.received_messages: List[Message] = []
        self.response_status = response_status
        self.response_body = response_body

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        self.called = True

        if scope.get("type") != "http":
            self.executed = True
            return

        while True:
            message = await receive()
            self.received_messages.append(message)
            if message["type"] == "http.request":
                if not message.get("more_body", False):
                    self.completed = True
                    break
            elif message["type"] == "http.disconnect":
                return

        self.executed = True
        await send(
            {
                "type": "http.response.start",
                "status": self.response_status,
                "headers": [[b"content-type", b"text/plain"]],
            }
        )
        await send(
            {
                "type": "http.response.body",
                "body": self.response_body,
            }
        )


def make_receive(messages: List[Message]) -> Receive:
    """Helper to return an ASGI receive callable for a sequence of messages."""
    queue = list(messages)

    async def receive() -> Message:
        if queue:
            return queue.pop(0)
        return {"type": "http.disconnect"}

    return receive


def test_exception_type_is_production_class():
    """Verify that PayloadTooLargeException is the real production exception."""
    assert issubclass(PayloadTooLargeException, Exception)


def test_middleware_default_target_paths():
    """Verify that default target path is /api/v1/ingestion/file."""
    app = RecordingASGIApp()
    middleware = RequestBodyLimitMiddleware(app, max_size=MAX_SIZE)
    assert middleware.target_paths == ["/api/v1/ingestion/file"]


@pytest.mark.asyncio
async def test_middleware_accepts_under_limit():
    """Verify that requests under 6 MiB are accepted and downstream app executes."""
    app = RecordingASGIApp()
    middleware = RequestBodyLimitMiddleware(
        app, max_size=MAX_SIZE, target_paths=[TARGET_PATH]
    )

    body = b"a" * (3 * 1024 * 1024)  # 3 MiB
    receive = make_receive([{"type": "http.request", "body": body, "more_body": False}])
    sent_messages = []

    async def send(message):
        sent_messages.append(message)

    scope = {
        "type": "http",
        "method": "POST",
        "path": TARGET_PATH,
    }

    await middleware(scope, receive, send)

    assert app.called is True
    assert app.executed is True
    assert app.completed is True
    assert len(app.received_messages) == 1
    assert app.received_messages[0]["body"] == body

    assert len(sent_messages) == 2
    assert sent_messages[0]["type"] == "http.response.start"
    assert sent_messages[0]["status"] == 200
    assert sent_messages[1]["type"] == "http.response.body"
    assert sent_messages[1]["body"] == b"OK"


@pytest.mark.asyncio
async def test_middleware_forwards_chunks_incrementally():
    """Verify that valid request chunks are forwarded incrementally and downstream app executes."""
    app = RecordingASGIApp()
    middleware = RequestBodyLimitMiddleware(
        app, max_size=MAX_SIZE, target_paths=[TARGET_PATH]
    )

    chunk1 = b"x" * (2 * 1024 * 1024)  # 2 MiB
    chunk2 = b"y" * (2 * 1024 * 1024)  # 2 MiB
    chunk3 = b"z" * (1 * 1024 * 1024)  # 1 MiB

    receive = make_receive(
        [
            {"type": "http.request", "body": chunk1, "more_body": True},
            {"type": "http.request", "body": chunk2, "more_body": True},
            {"type": "http.request", "body": chunk3, "more_body": False},
        ]
    )
    sent_messages = []

    async def send(message):
        sent_messages.append(message)

    scope = {
        "type": "http",
        "method": "POST",
        "path": TARGET_PATH,
    }

    await middleware(scope, receive, send)

    assert app.called is True
    assert app.executed is True
    assert app.completed is True
    assert len(app.received_messages) == 3
    assert app.received_messages[0]["body"] == chunk1
    assert app.received_messages[1]["body"] == chunk2
    assert app.received_messages[2]["body"] == chunk3

    assert len(sent_messages) == 2
    assert sent_messages[0]["status"] == 200
    assert sent_messages[1]["body"] == b"OK"


@pytest.mark.asyncio
async def test_middleware_rejects_single_chunk_over_limit():
    """Verify that a request crossing 6 MiB receives exactly one 413 and message is not delivered downstream."""
    app = RecordingASGIApp()
    middleware = RequestBodyLimitMiddleware(
        app, max_size=MAX_SIZE, target_paths=[TARGET_PATH]
    )

    body = b"x" * (7 * 1024 * 1024)  # 7 MiB
    receive = make_receive([{"type": "http.request", "body": body, "more_body": False}])
    sent_messages = []

    async def send(message):
        sent_messages.append(message)

    scope = {
        "type": "http",
        "method": "POST",
        "path": TARGET_PATH,
    }

    await middleware(scope, receive, send)

    # Downstream app was entered, but over-limit message was NOT delivered downstream
    assert app.called is True
    assert app.executed is False
    assert app.completed is False
    assert len(app.received_messages) == 0

    # Exactly one 413 response sent to client
    assert len(sent_messages) == 2
    assert sent_messages[0]["type"] == "http.response.start"
    assert sent_messages[0]["status"] == 413
    assert sent_messages[1]["type"] == "http.response.body"
    assert b"Payload too large" in sent_messages[1]["body"]


@pytest.mark.asyncio
async def test_middleware_rejects_chunked_request_crossing_limit():
    """Verify that when a chunk crosses the 6 MiB limit, it is not delivered downstream and 413 is returned."""
    app = RecordingASGIApp()
    middleware = RequestBodyLimitMiddleware(
        app, max_size=MAX_SIZE, target_paths=[TARGET_PATH]
    )

    chunk1 = b"a" * (4 * 1024 * 1024)  # 4 MiB (under limit)
    chunk2 = b"b" * (3 * 1024 * 1024)  # 3 MiB (crosses 6 MiB limit)

    receive = make_receive(
        [
            {"type": "http.request", "body": chunk1, "more_body": True},
            {"type": "http.request", "body": chunk2, "more_body": False},
        ]
    )
    sent_messages = []

    async def send(message):
        sent_messages.append(message)

    scope = {
        "type": "http",
        "method": "POST",
        "path": TARGET_PATH,
    }

    await middleware(scope, receive, send)

    # Chunk 1 was delivered, but chunk 2 crossed the limit and was NOT delivered downstream
    assert app.called is True
    assert app.executed is False
    assert app.completed is False
    assert len(app.received_messages) == 1
    assert app.received_messages[0]["body"] == chunk1

    # Exactly one 413 response sent
    assert len(sent_messages) == 2
    assert sent_messages[0]["type"] == "http.response.start"
    assert sent_messages[0]["status"] == 413
    assert sent_messages[1]["type"] == "http.response.body"
    assert b"Payload too large" in sent_messages[1]["body"]


@pytest.mark.asyncio
async def test_middleware_exact_limit_accepted():
    """Verify that requests exactly at the 6 MiB limit are accepted."""
    app = RecordingASGIApp()
    middleware = RequestBodyLimitMiddleware(
        app, max_size=MAX_SIZE, target_paths=[TARGET_PATH]
    )

    body = b"x" * MAX_SIZE  # Exactly 6 MiB
    receive = make_receive([{"type": "http.request", "body": body, "more_body": False}])
    sent_messages = []

    async def send(message):
        sent_messages.append(message)

    scope = {
        "type": "http",
        "method": "POST",
        "path": TARGET_PATH,
    }

    await middleware(scope, receive, send)

    assert app.called is True
    assert app.executed is True
    assert app.completed is True
    assert len(app.received_messages) == 1
    assert app.received_messages[0]["body"] == body

    assert len(sent_messages) == 2
    assert sent_messages[0]["status"] == 200
    assert sent_messages[1]["body"] == b"OK"


@pytest.mark.asyncio
async def test_middleware_one_byte_over_limit_rejected():
    """Verify that requests exactly 1 byte over the 6 MiB limit are rejected."""
    app = RecordingASGIApp()
    middleware = RequestBodyLimitMiddleware(
        app, max_size=MAX_SIZE, target_paths=[TARGET_PATH]
    )

    body = b"x" * MAX_SIZE + b"y"  # 6 MiB + 1 byte
    receive = make_receive([{"type": "http.request", "body": body, "more_body": False}])
    sent_messages = []

    async def send(message):
        sent_messages.append(message)

    scope = {
        "type": "http",
        "method": "POST",
        "path": TARGET_PATH,
    }

    await middleware(scope, receive, send)

    assert app.called is True
    assert app.executed is False
    assert len(app.received_messages) == 0

    assert len(sent_messages) == 2
    assert sent_messages[0]["status"] == 413
    assert sent_messages[1]["type"] == "http.response.body"


@pytest.mark.asyncio
async def test_middleware_sends_exactly_one_413_response():
    """Verify that exactly one valid 413 response is sent and no request messages are sent."""
    app = RecordingASGIApp()
    middleware = RequestBodyLimitMiddleware(
        app, max_size=MAX_SIZE, target_paths=[TARGET_PATH]
    )

    body = b"x" * (8 * 1024 * 1024)  # 8 MiB
    receive = make_receive([{"type": "http.request", "body": body, "more_body": False}])
    sent_messages = []

    async def send(message):
        sent_messages.append(message)

    scope = {
        "type": "http",
        "method": "POST",
        "path": TARGET_PATH,
    }

    await middleware(scope, receive, send)

    assert len(sent_messages) == 2
    assert sent_messages[0]["type"] == "http.response.start"
    assert sent_messages[0]["status"] == 413
    assert sent_messages[1]["type"] == "http.response.body"
    assert b"Payload too large" in sent_messages[1]["body"]

    # Verify no http.request messages were erroneously passed to send()
    request_messages = [m for m in sent_messages if m.get("type") == "http.request"]
    assert len(request_messages) == 0


@pytest.mark.asyncio
async def test_middleware_misleading_content_length_header():
    """Verify that body-size limit is enforced using actual bytes, ignoring misleading Content-Length."""
    # Subtest A: Misleadingly small Content-Length header with 7 MiB body -> 413
    app = RecordingASGIApp()
    middleware = RequestBodyLimitMiddleware(
        app, max_size=MAX_SIZE, target_paths=[TARGET_PATH]
    )

    body = b"x" * (7 * 1024 * 1024)
    receive = make_receive([{"type": "http.request", "body": body, "more_body": False}])
    sent_messages = []

    async def send(message):
        sent_messages.append(message)

    scope = {
        "type": "http",
        "method": "POST",
        "path": TARGET_PATH,
        "headers": [[b"content-length", b"100"]],
    }

    await middleware(scope, receive, send)

    assert app.executed is False
    assert len(app.received_messages) == 0
    assert sent_messages[0]["status"] == 413

    # Subtest B: Misleadingly huge Content-Length header with 2 MiB body -> 200 OK
    app_small = RecordingASGIApp()
    middleware_small = RequestBodyLimitMiddleware(
        app_small, max_size=MAX_SIZE, target_paths=[TARGET_PATH]
    )

    small_body = b"y" * (2 * 1024 * 1024)
    receive_small = make_receive(
        [{"type": "http.request", "body": small_body, "more_body": False}]
    )
    sent_messages_small = []

    async def send_small(message):
        sent_messages_small.append(message)

    scope_small = {
        "type": "http",
        "method": "POST",
        "path": TARGET_PATH,
        "headers": [[b"content-length", b"999999999"]],
    }

    await middleware_small(scope_small, receive_small, send_small)

    assert app_small.executed is True
    assert app_small.completed is True
    assert sent_messages_small[0]["status"] == 200


@pytest.mark.asyncio
async def test_middleware_handles_missing_content_length():
    """Verify that missing Content-Length header still enforces actual byte limit."""
    # Subtest A: Missing Content-Length with 7 MiB body -> 413
    app = RecordingASGIApp()
    middleware = RequestBodyLimitMiddleware(
        app, max_size=MAX_SIZE, target_paths=[TARGET_PATH]
    )

    body = b"x" * (7 * 1024 * 1024)
    receive = make_receive([{"type": "http.request", "body": body, "more_body": False}])
    sent_messages = []

    async def send(message):
        sent_messages.append(message)

    scope = {
        "type": "http",
        "method": "POST",
        "path": TARGET_PATH,
    }

    await middleware(scope, receive, send)

    assert app.executed is False
    assert len(app.received_messages) == 0
    assert sent_messages[0]["status"] == 413

    # Subtest B: Missing Content-Length with 2 MiB body -> 200 OK
    app_small = RecordingASGIApp()
    middleware_small = RequestBodyLimitMiddleware(
        app_small, max_size=MAX_SIZE, target_paths=[TARGET_PATH]
    )

    small_body = b"y" * (2 * 1024 * 1024)
    receive_small = make_receive(
        [{"type": "http.request", "body": small_body, "more_body": False}]
    )
    sent_messages_small = []

    async def send_small(message):
        sent_messages_small.append(message)

    scope_small = {
        "type": "http",
        "method": "POST",
        "path": TARGET_PATH,
    }

    await middleware_small(scope_small, receive_small, send_small)

    assert app_small.executed is True
    assert app_small.completed is True
    assert sent_messages_small[0]["status"] == 200


@pytest.mark.asyncio
async def test_middleware_does_not_affect_other_endpoints():
    """Verify that requests to non-target paths are not limited by the middleware."""
    app = RecordingASGIApp()
    middleware = RequestBodyLimitMiddleware(
        app, max_size=MAX_SIZE, target_paths=[TARGET_PATH]
    )

    body = b"x" * (7 * 1024 * 1024)  # 7 MiB
    receive = make_receive([{"type": "http.request", "body": body, "more_body": False}])
    sent_messages = []

    async def send(message):
        sent_messages.append(message)

    scope = {
        "type": "http",
        "method": "POST",
        "path": "/health",  # Non-target path
    }

    await middleware(scope, receive, send)

    assert app.called is True
    assert app.executed is True
    assert app.completed is True
    assert len(app.received_messages) == 1
    assert app.received_messages[0]["body"] == body
    assert sent_messages[0]["status"] == 200


@pytest.mark.asyncio
async def test_middleware_only_applies_to_post():
    """Verify that non-POST methods (e.g. GET) on target path are not limited."""
    app = RecordingASGIApp()
    middleware = RequestBodyLimitMiddleware(
        app, max_size=MAX_SIZE, target_paths=[TARGET_PATH]
    )

    body = b"x" * (7 * 1024 * 1024)  # 7 MiB
    receive = make_receive([{"type": "http.request", "body": body, "more_body": False}])
    sent_messages = []

    async def send(message):
        sent_messages.append(message)

    scope = {
        "type": "http",
        "method": "GET",
        "path": TARGET_PATH,
    }

    await middleware(scope, receive, send)

    assert app.called is True
    assert app.executed is True
    assert app.completed is True
    assert len(app.received_messages) == 1
    assert app.received_messages[0]["body"] == body
    assert sent_messages[0]["status"] == 200


@pytest.mark.asyncio
async def test_middleware_bypasses_non_http_scope():
    """Verify that non-HTTP scopes (e.g. websocket, lifespan) are passed through."""
    app = RecordingASGIApp()
    middleware = RequestBodyLimitMiddleware(
        app, max_size=MAX_SIZE, target_paths=[TARGET_PATH]
    )

    receive = make_receive([])
    sent_messages = []

    async def send(message):
        sent_messages.append(message)

    scope = {
        "type": "websocket",
        "path": TARGET_PATH,
    }

    await middleware(scope, receive, send)

    assert app.called is True
    assert app.executed is True
    assert len(sent_messages) == 0


@pytest.mark.asyncio
async def test_middleware_handles_immediate_disconnect():
    """Verify that client disconnect before body completes does not hang or send 413."""
    app = RecordingASGIApp()
    middleware = RequestBodyLimitMiddleware(
        app, max_size=MAX_SIZE, target_paths=[TARGET_PATH]
    )

    receive = make_receive([{"type": "http.disconnect"}])
    sent_messages = []

    async def send(message):
        sent_messages.append(message)

    scope = {
        "type": "http",
        "method": "POST",
        "path": TARGET_PATH,
    }

    await middleware(scope, receive, send)

    assert app.called is True
    assert app.executed is False  # Disconnected before app finished
    assert len(app.received_messages) == 1
    assert app.received_messages[0]["type"] == "http.disconnect"
    assert len(sent_messages) == 0


@pytest.mark.asyncio
async def test_middleware_handles_disconnect_during_chunked_stream():
    """Verify that client disconnect after initial chunks does not hang or send 413."""
    app = RecordingASGIApp()
    middleware = RequestBodyLimitMiddleware(
        app, max_size=MAX_SIZE, target_paths=[TARGET_PATH]
    )

    chunk = b"a" * (2 * 1024 * 1024)  # 2 MiB
    receive = make_receive(
        [
            {"type": "http.request", "body": chunk, "more_body": True},
            {"type": "http.disconnect"},
        ]
    )
    sent_messages = []

    async def send(message):
        sent_messages.append(message)

    scope = {
        "type": "http",
        "method": "POST",
        "path": TARGET_PATH,
    }

    await middleware(scope, receive, send)

    assert app.called is True
    assert app.executed is False
    assert len(app.received_messages) == 2
    assert app.received_messages[0]["body"] == chunk
    assert app.received_messages[1]["type"] == "http.disconnect"
    assert len(sent_messages) == 0


@pytest.mark.asyncio
async def test_middleware_handles_request_completion_with_empty_final_chunk():
    """Verify request completes when final chunk has body=b'' and more_body=False."""
    app = RecordingASGIApp()
    middleware = RequestBodyLimitMiddleware(
        app, max_size=MAX_SIZE, target_paths=[TARGET_PATH]
    )

    chunk1 = b"hello "
    chunk2 = b"world"

    receive = make_receive(
        [
            {"type": "http.request", "body": chunk1, "more_body": True},
            {"type": "http.request", "body": chunk2, "more_body": True},
            {"type": "http.request", "body": b"", "more_body": False},
        ]
    )
    sent_messages = []

    async def send(message):
        sent_messages.append(message)

    scope = {
        "type": "http",
        "method": "POST",
        "path": TARGET_PATH,
    }

    await middleware(scope, receive, send)

    assert app.called is True
    assert app.executed is True
    assert app.completed is True
    assert len(app.received_messages) == 3
    assert sent_messages[0]["status"] == 200
    assert sent_messages[1]["body"] == b"OK"


@pytest.mark.asyncio
async def test_middleware_reraises_when_response_already_started():
    """Verify that when the downstream application has already sent http.response.start
    and the payload-limit exception occurs afterward:
    - The middleware does not send a second response.
    - The exception propagates to the caller.
    - No duplicate or malformed ASGI response messages are emitted.
    """

    async def early_response_app(scope: Scope, receive: Receive, send: Send):
        # Downstream app starts sending response headers before consuming request body
        await send(
            {
                "type": "http.response.start",
                "status": 200,
                "headers": [[b"content-type", b"text/plain"]],
            }
        )
        # Next receive call will encounter an over-limit payload
        await receive()

    middleware = RequestBodyLimitMiddleware(
        early_response_app, max_size=MAX_SIZE, target_paths=[TARGET_PATH]
    )

    body = b"x" * (7 * 1024 * 1024)  # 7 MiB (exceeds 6 MiB limit)
    receive = make_receive([{"type": "http.request", "body": body, "more_body": False}])
    sent_messages = []

    async def send(message):
        sent_messages.append(message)

    scope = {
        "type": "http",
        "method": "POST",
        "path": TARGET_PATH,
    }

    # Exception must propagate to the caller because response has already started
    with pytest.raises(PayloadTooLargeException):
        await middleware(scope, receive, send)

    # Middleware must NOT have sent a duplicate response-start or 413 response body
    assert len(sent_messages) == 1
    assert sent_messages[0]["type"] == "http.response.start"
    assert sent_messages[0]["status"] == 200


@pytest.mark.asyncio
async def test_middleware_reraises_when_response_already_started_chunked():
    """Verify that when downstream app sends response headers after an initial valid chunk
    and a subsequent chunk exceeds the limit:
    - The middleware does not send a second response.
    - PayloadTooLargeException propagates to caller.
    - Only the application's initial response message was emitted.
    """

    async def streaming_app(scope: Scope, receive: Receive, send: Send):
        # Read first chunk
        chunk1 = await receive()
        assert chunk1["type"] == "http.request"

        # Start response early
        await send(
            {
                "type": "http.response.start",
                "status": 200,
                "headers": [[b"content-type", b"text/plain"]],
            }
        )

        # Read next chunk which crosses the limit
        await receive()

    middleware = RequestBodyLimitMiddleware(
        streaming_app, max_size=MAX_SIZE, target_paths=[TARGET_PATH]
    )

    chunk1 = b"a" * (4 * 1024 * 1024)  # 4 MiB (under limit)
    chunk2 = b"b" * (3 * 1024 * 1024)  # 3 MiB (crosses 6 MiB limit)
    receive = make_receive(
        [
            {"type": "http.request", "body": chunk1, "more_body": True},
            {"type": "http.request", "body": chunk2, "more_body": False},
        ]
    )
    sent_messages = []

    async def send(message):
        sent_messages.append(message)

    scope = {
        "type": "http",
        "method": "POST",
        "path": TARGET_PATH,
    }

    with pytest.raises(PayloadTooLargeException):
        await middleware(scope, receive, send)

    # Middleware must not emit duplicate or malformed response messages
    assert len(sent_messages) == 1
    assert sent_messages[0]["type"] == "http.response.start"
    assert sent_messages[0]["status"] == 200
