from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from ._rules import Rule
from .core.api_log import logger
from .pkg import tools


class __CustomMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        response = None

        if Rule.ADD_REQUEST_LOGGING_MIDDLEWARE:
            logger.info(f"{request.method} | {request.url}")
            response = await call_next(request)
            logger.debug(response.status_code)

        if Rule.ADD_LINK_TRACKING_MIDDLEWARE:
            request_id = tools.generate_request_id()
            request_time = tools.generate_request_time()

            request.state.traceid = request_id
            response = await call_next(request)

            response.headers["X-Request-ID"] = request_id
            response.headers["X-Request-Time"] = request_time

            logger.debug(f"{request_id} | {request_time}")

        if response is None:
            response = await call_next(request)

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

    app.add_middleware(__CustomMiddleware)
