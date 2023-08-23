from ...controllers.controllers import catch_controller
from ...dao import crud


@catch_controller
def query_jobs(company_name,
               job_name,
               category):
    return crud.query_jobs(company_name, job_name, category)


@catch_controller
def create_job(job_data):
    return crud.create_job(job_data)


@catch_controller
def update_job(job_id,
               company_name,
               job_name,
               category):
    expression = {
        k: v
        for k, v in {
            "job_name": job_name,
            "company_name": company_name,
            "category": category,
        }.items()
        if v is not None
    }
    return crud.update_job(job_id, expression)


@catch_controller
def delete_job(job_id):
    return crud.delete_job(job_id)
