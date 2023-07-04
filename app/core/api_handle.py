from traceback import print_exc

from fastapi import HTTPException

from .api_log import logger
from .._rules import ResponseCode, Rule
from ..models.response import PublicResponse
from ..pkg.error import exceptions_to_catch


async def async_handle_exceptions(fn, *args, **kwargs):
    try:
        resp = await fn(*args, **kwargs)
    except HTTPException as e:
        return PublicResponse(code=ResponseCode.FAILURE, data=None, msg=e.detail)
    except Exception as e:
        logger.warning(f'Caught exception: {e}')
        if isinstance(e, tuple(exceptions_to_catch)):
            return PublicResponse(code=ResponseCode.FAILURE, data=None, msg=e.message)

        if Rule.PRINT_ERROR_STACK:
            print_exc()

        if Rule.OUTPUT_INTERNAL_ERROR:
            return PublicResponse(code=ResponseCode.INTERNAL_ERROR, data=None, msg=e.__str__())

        return PublicResponse(code=ResponseCode.INTERNAL_ERROR, data=None, msg="service busy")

    else:
        return PublicResponse(code=ResponseCode.SUCCESS, data=resp, msg="success")


def sync_handle_exceptions(fn, *args, **kwargs):
    try:
        resp = fn(*args, **kwargs)
    except HTTPException as e:
        return PublicResponse(code=ResponseCode.FAILURE, data=None, msg=e.detail)
    except Exception as e:
        logger.warning(f'Caught exception: {e}')
        if isinstance(e, tuple(exceptions_to_catch)):
            return PublicResponse(code=ResponseCode.FAILURE, data=None, msg=e.message)

        if Rule.PRINT_ERROR_STACK:
            print_exc()

        if Rule.OUTPUT_INTERNAL_ERROR:
            return PublicResponse(code=ResponseCode.INTERNAL_ERROR, data=None, msg=e.__str__())

        return PublicResponse(code=ResponseCode.INTERNAL_ERROR, data=None, msg="service busy")

    else:
        return PublicResponse(code=ResponseCode.SUCCESS, data=resp, msg="success")
