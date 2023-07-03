from typing import List

from ..core import api_db
from ..models import request
from ..models.schema import Mxuser


def query_user_list():
    return api_db.query_all(Mxuser)


def query_user(uid):
    return api_db.query_first(Mxuser, id=uid)


def insert_user(model):
    return api_db.insert(Mxuser, data=model, refresh=True)


def insert_users(model: List[request.User]):
    return api_db.insert(Mxuser, data=model, refresh=True)


def update_user(uid, model: request.User):
    return api_db.update(Mxuser, id=[uid, 2], username='cj', data={'status': 'fix'}, refresh=True)
