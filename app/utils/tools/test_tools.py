from unittest import TestCase

from pydantic import BaseModel

import tools
from app.models.schema import Boss


class T(BaseModel):
    company: str
    job: str


class Test(TestCase):

    def test_generate_request_id(self):
        for _ in range(10):
            print(tools.generate_request_id())

    def test_generate_request_time(self):
        timezone_list = ["Asia/Shanghai", "America/Adak", "America/Anchorage"]
        for i in timezone_list:
            print(tools.generate_request_time(i))

    def test_body_to_orm_objects(self):
        model = T(company="bim", job="python")
        orm = tools.body_to_orm_objects(Boss, model, {"company": "company_name", "job": "job_name"})
        print(orm.__dict__)
        print(type(model))
        print(vars(model))

        models = [
            T(company="c1", job="python", ),
            T(company="c2", job="python"),
        ]
        orms = tools.body_to_orm_objects(Boss, models, {"company": "company_name", "job": "job_name"})
        for i in orms:
            print(i.__dict__)

    def test_get_current_time(self):
        print(tools.get_current_time(time_format="%Y-%m-%d"))
        print(tools.get_current_time(time_format="America/Adak"))
        print(tools.get_current_time(include_date=False))
        print(tools.get_current_time(include_time=False))
