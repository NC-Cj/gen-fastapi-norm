from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

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
