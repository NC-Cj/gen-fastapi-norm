from typing import Optional, Any

from pydantic import BaseModel


class PublicResponse(BaseModel):
    code: int
    data: Optional[Any] = None
    msg: Optional[Any] = None
