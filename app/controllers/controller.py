import asyncio
from functools import wraps

from app.models.response import PublicResponse
from app.project_rules import ResponseCode


def rc(fn):
    """
    Response Controller.

    Wraps a function and returns a PublicResponse with the result.

    Args:
        fn: The function to be wrapped.

    Returns:
        async_wrapper or sync_wrapper: The wrapped function that returns a PublicResponse.
    """

    @wraps(fn)
    async def async_wrapper(*args,
                            **kwargs):
        resp = await fn(*args, **kwargs)
        return PublicResponse(code=ResponseCode.SUCCESS, data=resp, msg="success")

    @wraps(fn)
    def sync_wrapper(*args,
                     **kwargs):
        resp = fn(*args, **kwargs)
        return PublicResponse(code=ResponseCode.SUCCESS, data=resp, msg="success")

    return async_wrapper if asyncio.iscoroutinefunction(fn) else sync_wrapper
