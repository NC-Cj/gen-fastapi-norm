import functools
import traceback

from fastapi import HTTPException

from app.models import response


def serialize(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            result = await func(*args, **kwargs)
        except HTTPException as e:
            exc = await receive(e, True)
            print("Error ===>", exc, flush=True)
            return response.Response(
                code=response.ResponseCode.FAILURE,
                data=[],
                msg=e.detail
            )
        except Exception as e:
            exc = await receive(e, False)
            print("Error ===>", exc, flush=True)
            return response.Response(
                code=response.ResponseCode.INTERNAL_ERROR,
                msg="Server is busy"
            )
        return response.Response(
            code=response.ResponseCode.SUCCESS,
            data=result,
            msg="Success"
        )

    async def receive(e, _http):
        if _http:
            message = e.detail
            status_code = e.status_code
        else:
            message = e.__repr__()
            status_code = 500

        tb = traceback.extract_tb(e.__traceback__)
        filename, lineno, name, line_code = tb[-1] if tb else ('', 0, '<unknown>', '')
        exc = {
            "filename": filename,
            "funcname": name,
            "line": lineno,
            "message": message,
            "status_code": status_code
        }
        return exc

    return wrapper
