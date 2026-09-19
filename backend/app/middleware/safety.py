from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from app.services.safety_gateway import (
    check_dangerous_content,
    check_medical_content,
    get_dangerous_content_response,
    get_medical_disclaimer,
)


class SafetyGatewayMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Only check POST requests with JSON body (like /chat endpoint)
        if request.method == "POST" and request.url.path.startswith("/api/v1/chat"):
            # Read the body
            body = await request.body()
            if body:
                # Decode and check for dangerous/medical content
                try:
                    import json

                    data = json.loads(body)
                    # Check if there's a message field
                    if "message" in data and isinstance(data["message"], str):
                        message = data["message"]
                        if check_dangerous_content(message):
                            # Return dangerous content response
                            return Response(
                                content=get_dangerous_content_response(),
                                media_type="text/plain",
                                status_code=200,
                            )
                        elif check_medical_content(message):
                            # For medical content, we'll let it proceed but add disclaimer in the response
                            # We'll handle this in the chat endpoint by adding a disclaimer
                            pass
                except (json.JSONDecodeError, KeyError, TypeError):
                    # If we can't parse, let it through (validation will catch it later)
                    pass

        response = await call_next(request)
        return response
