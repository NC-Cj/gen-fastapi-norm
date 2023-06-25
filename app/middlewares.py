from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from .pkg import tools

# Use request id to check service response
class __AddRequestHeaders(BaseHTTPMiddleware):

    async def dispatch(self, request, call_next):
        response = await call_next(request)
        request_id = tools.generate_request_id()
        request_time = tools.generate_request_time()

        response.headers["X-Request-ID"] = request_id
        response.headers["X-Request-Time"] = request_time

        print(request_id, request_time)

        return response


def add_middlewares(app: FastAPI):
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
