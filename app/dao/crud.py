from ..models import schema


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
    return schema.Boss.filter(**expression)


def create_job(data):
    return schema.Boss(**data.dict()).save(refresh=True)
    # data = [
    #     schema.Boss(company_name="tiam1", job_name="华为", salary="华为", address="华为"),
    #     schema.Boss(company_name="tiam2", job_name="华为", salary="华为", address="华为"),
    #     schema.Boss(company_name="tiam3", job_name="华为", salary="华为", address="华为")
    # ]
    # return schema.Boss.save_many(data=data)
    # return schema.Boss(
    #     company_name="tiam",
    #     job_name="华为",
    #     salary="华为",
    #     address="华为"
    # ).save()


def update_job(job_id,
               expression):
    return schema.Boss.update(id=job_id, data=expression)


def delete_job(job_id):
    return schema.Boss.delete(id=job_id)
