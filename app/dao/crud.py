from ..models import schema
from ..utils.tools import tools
from ..utils.types.converter_type import DictConverter


def query_jobs(company_name,
               job_name,
               category):
    expression = {
        k: v
        for k, v in {
            "company_name": company_name,
            "job_name": job_name,
            "category": category,
        }.items()
        if v is not None
    }
    return schema.Boss.filter(result_converter=DictConverter, **expression)


def create_job(data):
    # if you an instance
    # return schema.Boss(**data.dict()).save(refresh=True)

    # if you multiple instances
    orm = tools.body_to_orm_objects(schema.Boss, data)
    return schema.Boss.save_many(data=orm, refresh=True)


def update_job(job_id,
               expression):
    return schema.Boss.update(id=job_id, data=expression)


def delete_job(job_id):
    return schema.Boss.delete(id=job_id)
