import traceback

from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from app.project_rules import ResponseCode, Rule
from app.utils.errors.error import global_exceptions_to_catch
from app.utils.logger.log_setup import logger
from app.utils.tools import tools


class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self,
                       request: Request,
                       call_next):
        request.state.request_id = request.headers.get("X-Request-ID") or tools.generate_request_id()
        request.state.request_time = tools.generate_request_time()

        response = await call_next(request)
        response.headers["X-Request-ID"] = request.state.request_id
        response.headers["X-Request-Time"] = request.state.request_time
        return response


class ExceptionHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self,
                       request: Request,
                       call_next):
        try:
            response = await call_next(request)
        except HTTPException as exc:
            error_response = {
                "code": ResponseCode.FAILURE,
                "data": None,
                "request_id": request.state.request_id,
                "msg": exc.detail
            }
            response = JSONResponse(status_code=200, content=error_response)
        except Exception as exc:
            if Rule.PRINT_ERROR_STACK:
                traceback.print_exc()

            if isinstance(exc, tuple(global_exceptions_to_catch)):
                error_response = {
                    "code": ResponseCode.FAILURE,
                    "data": None,
                    "request_id": request.state.request_id,
                    "msg": exc.message
                }
            else:
                if Rule.OUTPUT_ERROR_STACK:
                    traceback_info = traceback.format_exc()
                    msg = traceback_info
                else:
                    msg = "service busy"

                error_response = {
                    "code": ResponseCode.INTERNAL_ERROR,
                    "data": None,
                    "request_id": request.state.request_id,
                    "msg": msg
                }
                print(error_response)
            response = JSONResponse(status_code=200, content=error_response)

        return response


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self,
                       request: Request,
                       call_next):
        try:
            request_id = request.state.request_id
            request_time = request.state.request_time
        except AttributeError:
            request_id = "undefined"
            request_time = "undefined"

        logger.info(f"{request.method} | {request.url} | {request_id} | {request_time}")

        return await call_next(request)
