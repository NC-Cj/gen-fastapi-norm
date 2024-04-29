from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.config.constants import VAR_REQUEST_ID
from app.utils.logger.setup import logger
from app.utils.tools import tools


class InitialMiddleware(BaseHTTPMiddleware):
    async def dispatch(self,
                       request: Request,
                       call_next):
        request.state.request_id = request.headers.get(VAR_REQUEST_ID) or tools.generate_request_id()
        request.state.request_time = tools.generate_request_time()

        logger.info(
            f"Request connection",
            request_id=request.state.request_id,
            request_time=request.state.request_time,
            method=request.method,
            url=request.url.__str__()
        )

        return await call_next(request)
