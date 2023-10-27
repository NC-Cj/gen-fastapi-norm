from fastapi import APIRouter

from app.routes.job.logic import v1
from app.routes.job.models import Job

router = APIRouter()


@router.get("/list")
async def get_job_list(company_name: str = None,
                       job_name: str = None,
                       category: str = None):
    return await v1.get_job_list(company_name, job_name, category)


@router.post("/job")
async def add_job(data: Job):
    return await v1.add_job(data)
