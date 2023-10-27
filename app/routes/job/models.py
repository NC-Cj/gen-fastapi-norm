from pydantic import BaseModel


class Job(BaseModel):
    company_name: str
    job_name: str
    salary: str
    address: str
    category: str
