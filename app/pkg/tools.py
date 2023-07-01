import datetime
import uuid
from typing import Any

from .error import UnsupportedDataTypeError


def generate_request_id():
    # Generate a random UUID
    uuid_str = str(uuid.uuid4())

    # Remove the hyphens from the UUID
    uuid_str = uuid_str.replace("-", "")

    # Insert hyphens at the appropriate positions
    return f"1-{uuid_str[:8]}-{uuid_str[8:12]}-{uuid_str[12:16]}-{uuid_str[16:]}"


def generate_request_time():
    # Load the Asia/Shanghai timezone
    tz = datetime.timezone(datetime.timedelta(hours=8))

    # Get the current time in the Asia/Shanghai timezone
    now = datetime.datetime.now(tz)

    # Format the time as a string in the desired format
    return now.strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def model_to_dict(data: Any) -> Any:
    if isinstance(data, list):
        return [model_to_dict(item) for item in data]
    elif isinstance(data, dict):
        return data
    elif hasattr(data, 'dict'):
        return data.dict()
    else:
        raise UnsupportedDataTypeError(f'Unsupported data type: {type(data)}')
