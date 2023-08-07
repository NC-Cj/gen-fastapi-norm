# The request body from your API, usually the body

from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    username: str
    status: Optional[str] = "normal"
