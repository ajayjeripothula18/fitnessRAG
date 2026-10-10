"""
Pure ASGI request body size limit middleware to prevent disk exhaustion.
Applies size limit before multipart parsing for specific routes.
"""
from typing import List
from starlette.types import ASGIApp, Receive, Scope, Send


class PayloadTooLargeException(Exception):
    """Exception raised when request body exceeds the size limit."""

    pass


class RequestBodyLimitMiddleware:
    """
    Pure ASGI middleware to enforce request body size limit before multipart parsing.

    This middleware counts actual request body bytes as they arrive in http.request
    messages and rejects requests that exceed the limit with 413 Payload Too Large.
    It applies only to specific routes to avoid affecting other endpoints.

    Unlike buffering implementations, this middleware processes messages incrementally
    and never accumulates the full body in memory.
    """

    def __init__(
        self,
        app: ASGIApp,
        max_size: int,
        target_paths: List[str] | None = None,
    ) -> None:
        """
        Initialize the middleware.

        Args:
            app: The ASGI application
            max_size: Maximum request body size in bytes
            target_paths: List of path prefixes that the limit applies to
        """
        self.app = app
        self.max_size = max_size
        self.target_paths = target_paths or ["/api/v1/ingestion/file"]

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        """
        Process the ASGI connection, enforcing body size limits for specific routes.

        Args:
            scope: The ASGI connection scope
            receive: Receive function for incoming messages
            send: Send function for outgoing messages
        """
        # Only apply to HTTP requests
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        # Check if this request should have the size limit applied
        if not self._should_apply_limit(scope):
            await self.app(scope, receive, send)
            return

        # Only apply to POST requests
        if scope.get("method") != "POST":
            await self.app(scope, receive, send)
            return

        # For POST requests to target paths, enforce the body size limit
        await self._enforce_body_limit(scope, receive, send)

    def _should_apply_limit(self, scope: Scope) -> bool:
        """Check if the size limit should be applied to this request."""
        path = scope.get("path", "")
        for path_prefix in self.target_paths:
            if path.startswith(path_prefix):
                return True
        return False

    async def _enforce_body_limit(
        self, scope: Scope, receive: Receive, send: Send
    ) -> None:
        """
        Enforce the body size limit by processing incoming messages incrementally.

        Args:
            scope: The ASGI connection scope
            receive: Receive function for incoming messages
            send: Send function for outgoing messages
        """
        total_body_size = 0
        response_started = False

        async def wrapped_receive() -> dict:
            """Wrap receive to count body bytes and enforce limits."""
            nonlocal total_body_size
            message = await receive()

            if message["type"] == "http.request":
                # This is a body chunk
                body_chunk = message.get("body", b"")
                chunk_size = len(body_chunk)

                # Check if adding this chunk would exceed the limit
                if total_body_size + chunk_size > self.max_size:
                    # Limit exceeded - raise exception to be caught below
                    raise PayloadTooLargeException()
                else:
                    # This chunk is within the limit, update counter and return message
                    total_body_size += chunk_size
                    return message
            else:
                # For non-body messages, return as-is
                return message

        async def send_wrapper(message: dict) -> None:
            """Wrap send to track when response has started."""
            nonlocal response_started
            if message["type"] == "http.response.start":
                response_started = True
            await send(message)

        try:
            # Pass control to the application with our wrapped functions
            await self.app(scope, wrapped_receive, send_wrapper)
        except PayloadTooLargeException:
            # Handle the payload too large exception
            if not response_started:
                # If response hasn't started yet, we can send a 413 response
                await send(
                    {
                        "type": "http.response.start",
                        "status": 413,
                        "headers": [
                            [b"content-type", b"text/plain"],
                        ],
                    }
                )
                await send(
                    {
                        "type": "http.response.body",
                        "body": b"Payload too large",
                    }
                )
                return
            # If response has already started, we cannot send another response start.
            # Re-raise so the server or caller can handle the connection failure
            # without violating ASGI protocol by sending duplicate response headers.
            raise
