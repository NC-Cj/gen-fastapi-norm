from typing import Optional, Any

from pydantic import BaseModel


class ResponseCode:
    """
    Response Code.

    Defines the response codes used in the application.

    Attributes:
        SUCCESS (int): The success response code.
        FAILURE (int): The failure response code.
        INTERNAL_ERROR (int): The internal error response code.
    """

    SUCCESS = 1000
    FAILURE = 1001
    INTERNAL_ERROR = 1002


class Response(BaseModel):
    code: int
    data: Optional[Any] = None
    msg: Optional[Any] = None
    request_id: Optional[str] = None
