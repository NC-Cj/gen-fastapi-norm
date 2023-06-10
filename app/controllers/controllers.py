from functools import wraps
from traceback import print_exc

from fastapi import HTTPException

from ..models.response import PublicResponse


def sync_catch_controller(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            resp = fn(*args, **kwargs)
        except HTTPException as e:
            return PublicResponse(code=1001, data=None, msg=e.detail)
        except Exception as e:
            print('Caught exception:', e)
            print_exc()
            return PublicResponse(code=1002, data=None, msg="service busy")
        else:
            return PublicResponse(code=1002, data=resp, msg="success")

    return wrapper


def catch_controller(fn):
    @wraps(fn)
    async def wrapper(*args, **kwargs):
        try:
            resp = await fn(*args, **kwargs)
            print(resp)
        except HTTPException as e:
            return PublicResponse(code=1001, data=None, msg=e.detail)
        except Exception as e:
            print('Caught exception:', e)
            print_exc()
            return PublicResponse(code=1002, data=None, msg="service busy")
        else:
            return PublicResponse(code=1002, data=resp, msg="success")

    return wrapper
