import requests

from app.utils.errors.error import CustomHTTPException
from ..logger.log_setup import logger


def send_traced_http_request(traceid,
                             url,
                             method='GET',
                             params=None,
                             data=None,
                             headers=None):
    if headers is None:
        headers = {}

    headers["X-Request-ID"] = traceid

    try:
        response = requests.request(method, url, params=params, data=data, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.error(f"traced request failed: {e}, http code={response.status_code}")
    else:
        result = response.json()
        if result["code"] != 1000:
            raise CustomHTTPException(f"traceid={traceid}, response={result['code']} {result['msg']}")

        return result
