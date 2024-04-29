#  Copyright 2023/12/19 下午6:22 苏州谋迅智能科技有限公司

import aiohttp

from app.config.constants import VAR_REQUEST_ID
from app.utils.logger.setup import logger


async def fetch_traced_async_response(session,
                                      url,
                                      *,
                                      method='GET',
                                      headers=None,
                                      traceid=None,
                                      **kwargs):
    if headers is None:
        headers = {}

    if traceid:
        headers[VAR_REQUEST_ID] = traceid

    try:
        async with session.request(method, url, headers=headers, **kwargs) as response:
            response.raise_for_status()
            yield response
    except aiohttp.ClientError as e:
        logger.error(f"traced request failed: {e}, http code={response.status}")
