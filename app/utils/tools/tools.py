import uuid
from datetime import datetime
from typing import Dict, Any, TypeVar, Type, List
from typing import Union

import pytz
from pydantic import BaseModel
from pydantic import create_model

T = TypeVar('T', bound='RecursiveModel')


def generate_request_id():
    uuid_str = str(uuid.uuid4())
    uuid_str = uuid_str.replace("-", "")
    return f"1-{uuid_str[:8]}-{uuid_str[8:12]}-{uuid_str[12:16]}-{uuid_str[16:]}"


def generate_request_time(timezone="Asia/Shanghai"):
    return get_current_time(timezone=timezone)


def body_to_orm_objects(orm_model,
                        model: Union[BaseModel, List[BaseModel]],
                        field_mapping=None):
    if field_mapping is None:
        field_mapping = {}

    if isinstance(model, list):
        orm_objects = []
        for item in model:
            orm_kwargs = {field_mapping.get(k, k): v for k, v in item.model_dump().items()}
            orm_objects.append(orm_model(**orm_kwargs))

    else:
        orm_kwargs = {field_mapping.get(k, k): v for k, v in model.model_dump().items()}
        orm_objects = orm_model(**orm_kwargs)

    return orm_objects


def get_current_time(time_format='%Y-%m-%d %H:%M:%S',
                     timezone="Asia/Shanghai",
                     include_date=True,
                     include_time=True):
    current_time = datetime.now()

    if timezone:
        current_time = datetime.now(pytz.timezone(timezone))

    formatted_time = current_time.strftime(time_format)

    if not include_date:
        formatted_time = formatted_time.split(' ')[1]  # 只保留时间部分

    if not include_time:
        formatted_time = formatted_time.split(' ')[0]  # 只保留日期部分

    return formatted_time


def datetime_to_string(dt,
                       format_str='%Y-%m-%d %H:%M:%S') -> str:
    """Convert time to a string"""
    return dt.strftime(format_str)


def string_to_datetime(string,
                       format_str='%Y-%m-%d %H:%M:%S') -> datetime:
    """Convert string to time"""
    return datetime.strptime(string, format_str)


class RecursiveModel(BaseModel):
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        for name, field in cls.model_fields.items():
            if isinstance(field.type_, type) and issubclass(field.type_, RecursiveModel):
                field.type_ = field.type_


def dynamic_model(data: Dict[str, Any]) -> Type[RecursiveModel]:
    def build_fields(d: Dict[str, Any], parent_key: str = '') -> Dict[str, Any]:
        field_list = {}
        for k, v in d.items():
            key = f"{parent_key}_{k}" if parent_key else k
            if isinstance(v, dict):
                model_name = key.title().replace('_', '')
                field_list[key] = (dynamic_model(v), ...)
            else:
                field_list[key] = (type(v), ...)
        return field_list

    fields = build_fields(data)
    return create_model("Mode", __base__=RecursiveModel, **fields)
