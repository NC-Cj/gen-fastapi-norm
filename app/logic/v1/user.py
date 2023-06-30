from fastapi import HTTPException

from ...controllers.controllers import catch_controller
from ...dao import crud


@catch_controller
def query_user(uid):
    if uid == 1:
        raise HTTPException(500, 'No permissions')
    return crud.query_user(uid)


@catch_controller
def query_user_list():
    return crud.query_user_list()
