import asyncio
import traceback
from functools import wraps

from ..models.response import PublicResponse
from ..project_rules import Rule, ResponseCode
from ..utils.errors.error import CustomHTTPException, global_exceptions_to_catch
from ..utils.logger.log_setup import logger


def catch_controller(fn):
    @wraps(fn)
    async def async_wrapper(*args,
                            **kwargs):
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
    def sync_wrapper(*args,
                     **kwargs):
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
            traceback.print_exc()

        if isinstance(e, tuple(global_exceptions_to_catch)):
            msg = str(e.message) if isinstance(e.message, Exception) else e.message
            return PublicResponse(code=ResponseCode.FAILURE, data=None, msg=msg)

        if Rule.OUTPUT_UNHANDLED_EXCEPTIONS:
            traceback_info = traceback.format_exc()
            return PublicResponse(code=ResponseCode.INTERNAL_ERROR, data=None, msg=traceback_info)

        return PublicResponse(code=ResponseCode.INTERNAL_ERROR, data=None, msg="service busy")

    return async_wrapper if asyncio.iscoroutinefunction(fn) else sync_wrapper
