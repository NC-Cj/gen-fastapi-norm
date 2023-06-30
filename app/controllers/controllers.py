import asyncio
from functools import wraps

from ..core.api_handle import async_handle_exceptions, sync_handle_exceptions


def catch_controller(fn):
    @wraps(fn)
    async def async_wrapper(*args, **kwargs):
        return await async_handle_exceptions(fn, *args, **kwargs)

    @wraps(fn)
    def sync_wrapper(*args, **kwargs):
        return sync_handle_exceptions(fn, *args, **kwargs)

    return async_wrapper if asyncio.iscoroutinefunction(fn) else sync_wrapper
