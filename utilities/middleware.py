from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

class HeaderValidationMiddleware(BaseHTTPMiddleware):
    """Middleware to validate headers in incoming requests."""
    async def dispatch(self, request: Request, call_next):
        required_headers = ["X-API-Key"]  # Define required headers
        missing_headers = [header for header in required_headers if header not in request.headers]

        if missing_headers:
            return JSONResponse(
                status_code=400,
                content={
                    "error": "Header Validation Error",
                    "message": f"Missing required headers: {', '.join(missing_headers)}",
                },
            )

        response = await call_next(request)
        return response

