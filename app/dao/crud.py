from ..core import api_db
from ..models import schema


def query_user_list():
    return api_db.simple_query(schema.User)
