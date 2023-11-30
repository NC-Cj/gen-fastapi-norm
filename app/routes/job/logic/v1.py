from app.routes.job import crud
from app.utils.db.db_helpers import execute_raw_sql
from app.utils.tools import tools

async def get_job_list(company_name: str = None,
                       job_name: str = None,
                       category: str = None):
    return await crud.get_job_list(company_name, job_name, category)


async def add_job(data):
    tools.get_current_time()
    execute_raw_sql()
    return await crud.add_job(data)
