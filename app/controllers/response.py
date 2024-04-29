from typing import Optional, Any

from pydantic import BaseModel

SUCCESS = 1000
FAILURE = 1001
INTERNAL_ERROR = 1002

VAR_CODE_TO_LEVEL = {
    SUCCESS: "DEBUG",
    FAILURE: "WARN",
    INTERNAL_ERROR: "ERROR",
}


class BaseResponse(BaseModel):
    pass


class PublicResponse(BaseResponse):
    """
    Public Response.

    Represents a response object for public cases.

    Attributes:
        code (int): The response code.
        data (Optional[Any]): The response data (default: None).
        msg (Optional[Any]): The response message (default: None).
        request_id (Optional[str]): The request ID (default: None).
    """

    code: int
    data: Optional[Any] = None
    msg: Optional[Any] = None
    request_id: Optional[str] = None


class AbnormalResponse(BaseResponse):
    """
    Abnormal Response.

    Represents a response object for abnormal cases.

    Attributes:
        code (int): The response code.
        data (Optional[Any]): The response data (default: None).
        msg (Optional[Any]): The response message (default: None).
        request_id (Optional[str]): The request ID (default: None).
    """

    code: int
    data: Optional[Any] = None
    msg: Optional[Any] = None
    request_id: Optional[str] = None
