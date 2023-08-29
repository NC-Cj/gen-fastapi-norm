import uuid
from datetime import datetime
from zoneinfo import ZoneInfo


def generate_request_id():
    # Generate a random UUID
    uuid_str = str(uuid.uuid4())

    # Remove the hyphens from the UUID
    uuid_str = uuid_str.replace("-", "")

    # Insert hyphens at the appropriate positions
    return f"1-{uuid_str[:8]}-{uuid_str[8:12]}-{uuid_str[12:16]}-{uuid_str[16:]}"


def generate_request_time(timezone="Asia/Shanghai"):
    now = datetime.now(ZoneInfo(timezone))
    # Format the time as a string in the desired format
    return now.strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def convert_to_orm_objects(orm_model,
                           model,
                           field_mapping=None):
    if field_mapping is None:
        field_mapping = {}

    if isinstance(model, list):
        orm_objects = []
        for item in model:
            orm_kwargs = {field_mapping.get(k, k): v for k, v in vars(item).items()}
            orm_objects.append(orm_model(**orm_kwargs))

    else:
        orm_kwargs = {field_mapping.get(k, k): v for k, v in vars(model).items()}
        orm_objects = orm_model(**orm_kwargs)

    return orm_objects


def get_current_time(time_format='%Y-%m-%d %H:%M:%S',
                     timezone="Asia/Shanghai",
                     include_date=True,
                     include_time=True):
    current_time = datetime.now()

    if timezone:
        current_time = datetime.now(ZoneInfo(timezone))

    formatted_time = current_time.strftime(time_format)

    if not include_date:
        formatted_time = formatted_time.split(' ')[1]  # 只保留时间部分

    if not include_time:
        formatted_time = formatted_time.split(' ')[0]  # 只保留日期部分

    return formatted_time
