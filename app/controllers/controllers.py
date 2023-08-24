import asyncio
from functools import wraps
from traceback import print_exc

from .._rules import Rule, ResponseCode
from app.core.logger.log_setup import logger
from ..models.response import PublicResponse
from ..pkg.error import CustomHTTPException, exceptions_to_catch


def catch_controller(fn):
    @wraps(fn)
    async def async_wrapper(*args, **kwargs):
        try:
            resp = await fn(*args, **kwargs)
        except CustomHTTPException as e:
            raise CustomHTTPException(e.message) from e
        except Exception as e:
            logger.warning(f'Caught exception: {e}')
            return handle_exception(e)

        else:
            return PublicResponse(code=ResponseCode.SUCCESS, data=resp, msg="success")

    @wraps(fn)
    def sync_wrapper(*args, **kwargs):
        try:
            resp = fn(*args, **kwargs)
        except CustomHTTPException as e:
            raise CustomHTTPException(e.message) from e
        except Exception as e:
            logger.warning(f'Caught exception: {e}')
            return handle_exception(e)

        else:
            return PublicResponse(code=ResponseCode.SUCCESS, data=resp, msg="success")

    def handle_exception(e):
        if Rule.PRINT_ERROR_STACK:
            print_exc()

        if isinstance(e, tuple(exceptions_to_catch)):
            return PublicResponse(code=ResponseCode.FAILURE, data=None, msg=e.message)

        if Rule.OUTPUT_UNHANDLED_EXCEPTIONS:
            return PublicResponse(code=ResponseCode.INTERNAL_ERROR, data=None, msg=str(e))

        return PublicResponse(code=ResponseCode.INTERNAL_ERROR, data=None, msg="service busy")

    return async_wrapper if asyncio.iscoroutinefunction(fn) else sync_wrapper
