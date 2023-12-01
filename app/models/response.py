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


class PublicResponse(BaseModel):
    """
    Public Response.

    Represents a response object for public cases.

    Attributes:
        code (int): The response code.
        data (Optional[Any]): The response data (default: None).
        msg (Optional[Any]): The response message (default: None).
    """

    code: ResponseCode
    data: Optional[Any] = None
    msg: Optional[Any] = None


class AbnormalResponse(BaseModel):
    """
    Abnormal Response.

    Represents a response object for abnormal cases.

    Attributes:
        code (int): The response code.
        data (Optional[Any]): The response data (default: None).
        msg (Optional[Any]): The response message (default: None).
        request_id (Optional[str]): The request ID (default: None).
    """

    code: ResponseCode
    data: Optional[Any] = None
    msg: Optional[Any] = None
    request_id: Optional[str] = None
