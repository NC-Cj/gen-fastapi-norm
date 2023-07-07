import json

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import StreamingResponse

from ._rules import Rule
from .core.api_log import logger
from .pkg import tools


class __CustomMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        if request.url.path in ["/favicon.ico", "/api/redoc", "/api/docs", "/api/openapi.json"]:
            return await call_next(request)

        request_id = tools.generate_request_id()
        request_time = tools.generate_request_time()

        request.state.traceid = request_id

        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Request-Time"] = request_time

        if Rule.ADD_REQUEST_LOGGING_MIDDLEWARE:
            body_bytes = b"".join([chunk async for chunk in response.body_iterator])
            body_str = body_bytes.decode("utf-8")
            body = json.loads(body_str)
            custom_code = body.get("code")

            logger.info(f"{request.method} | {request.url} | {request.state.traceid} | {request_time}")
            logger.info(f"HTTP.code | {response.status_code} | {custom_code}")

            async def new_body_iterator():
                yield body_bytes

            response = StreamingResponse(new_body_iterator(), headers=response.headers)

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
