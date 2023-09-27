from fastapi import APIRouter

from ...logic.v1 import job
from ...models.request import Job

app = APIRouter()


@app.get('/jobs')
def query_jobs(company_name: str = None,
               job_name: str = None,
               category: str = None):
    return job.query_jobs(company_name, job_name, category)


@app.post('/jobs')
def create_job(job_data: list[Job]):
    return job.create_job(job_data)


@app.put('/jobs/{job_id}')
def update_job(job_id: int,
               company_name: str = None,
               job_name: str = None,
               category: str = None):
    return job.update_job(job_id, company_name, job_name, category)


@app.delete('/jobs/{job_id}')
def delete_job(job_id: int):
    return job.delete_job(job_id)
