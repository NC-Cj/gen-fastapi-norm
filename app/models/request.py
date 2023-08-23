# The request body from your API, usually the body

from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    username: str
    status: Optional[str] = "normal"


class Job(BaseModel):
    company_name: str
    job_name: str
    salary: str
    address: str
    category: str
