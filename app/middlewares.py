import json

from fastapi import FastAPI, Request
from fastapi import status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import StreamingResponse, JSONResponse

from ._rules import Rule
from .core.api_log import logger
from .pkg import tools
from .pkg.error import CustomHTTPException


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

        if Rule.LOGGING_ALL_REQUESTS:
            logger.info(f"{request.method} | {request.url} | {request.state.traceid} | {request_time}")

        if Rule.LOGGING_NON_200_STATUS and response.status_code != 200:
            if Rule.LOGGING_ALL_REQUESTS:
                logger.warning("You have enabled recording of global requests, and any requests will be recorded  \n "
                               "`LOGGING_ALL_REQUESTS` and `LOGGING_NON_200_STATUS` should not be opened simultaneously")
            else:
                logger.info(f"{request.method} | {request.url.path} | {response.status_code}")

        if Rule.LOGGING_CUSTOM_RESPONSE_CODE:
            body_bytes = b"".join([chunk async for chunk in response.body_iterator])
            body_str = body_bytes.decode("utf-8")
            body = json.loads(body_str)
            custom_code = body.get("code")

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


def init_exception_handler(app: FastAPI):
    @app.exception_handler(CustomHTTPException)
    def custom_http_exception_handler(request: Request, exc):
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "code": 1001,
                "data": None,
                "request_id": request.state.traceid,
                "msg": exc.detail
            }
        )
