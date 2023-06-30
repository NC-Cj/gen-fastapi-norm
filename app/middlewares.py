from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from .core.api_log import logger
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

        logger.debug(f"{request_id} | {request_time}")

        return response


# Add request logging middleware
class __LogRequest(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        logger.info(f"{request.method} | {request.url}")

        response = await call_next(request)

        logger.debug(response.status_code)

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
