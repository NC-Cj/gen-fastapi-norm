from functools import wraps
from traceback import print_exc

from fastapi import HTTPException

from ..models.response import PublicResponse
from ..pkg.error import exceptions_to_catch

__ServiceSuccess = 1000
__ServiceFailure = 1001
__ServiceException = 1002


def sync_catch_controller(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            resp = fn(*args, **kwargs)
        except HTTPException as e:
            return PublicResponse(code=__ServiceFailure, data=None, msg=e.detail)
        except Exception as e:
            print('Caught exception:', e)
            if isinstance(e, tuple(exceptions_to_catch)):
                return PublicResponse(code=__ServiceFailure, data=None, msg=e.message)

            print_exc()
            return PublicResponse(code=__ServiceException, data=None, msg="service busy")

        else:
            return PublicResponse(code=__ServiceSuccess, data=resp, msg="success")

    return wrapper


def catch_controller(fn):
    @wraps(fn)
    async def wrapper(*args, **kwargs):
        try:
            resp = await fn(*args, **kwargs)
        except HTTPException as e:
            return PublicResponse(code=__ServiceFailure, data=None, msg=e.detail)
        except Exception as e:
            print('Caught exception:', e)
            if isinstance(e, tuple(exceptions_to_catch)):
                return PublicResponse(code=__ServiceFailure, data=None, msg=e.message)

            print_exc()
            return PublicResponse(code=__ServiceException, data=None, msg="service busy")

        else:
            return PublicResponse(code=__ServiceSuccess, data=resp, msg="success")

    return wrapper
