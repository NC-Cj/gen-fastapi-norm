from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from .pkg import tools


# Add request headers middleware
class __AddRequestHeaders(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        request_id = tools.generate_request_id()
        request_time = tools.generate_request_time()

        request.state.traceid = request_id
        response = await call_next(request)

        response.headers["X-Request-ID"] = request_id
        response.headers["X-Request-Time"] = request_time

        print(request_id, request_time)

        return response


# Add request logging middleware
class __LogRequest(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        print(f"[LOG] Received request: {request.method} {request.url}")
        response = await call_next(request)
        print(f"[LOG] Sent response: {response.status_code}")

        return response


def init_middlewares(app: FastAPI):
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Add trusted host middleware
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["*"],
    )

    app.add_middleware(__AddRequestHeaders)
    app.add_middleware(__LogRequest)
