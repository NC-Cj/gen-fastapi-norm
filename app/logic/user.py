from fastapi import HTTPException

from ..controllers.controllers import sync_catch_controller
from ..dao import crud


@sync_catch_controller
def query_user(uid):
    if uid == 1:
        raise HTTPException(500, 'No permissions')
    return crud.query_user(uid)


@sync_catch_controller
def query_user_list():
    return crud.query_user_list()
