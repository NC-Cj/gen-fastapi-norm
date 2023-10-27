from app.routes.job import crud


async def get_job_list(company_name: str = None,
                       job_name: str = None,
                       category: str = None):
    return await crud.get_job_list(company_name, job_name, category)


async def add_job(data):
    return await crud.add_job(data)
