from app.models import schema
from app.utils.types.converter_type import DictConverter


async def get_job_list(company_name,
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


async def add_job(data):
    return schema.Boss(**data.dict()).save(refresh=True)
