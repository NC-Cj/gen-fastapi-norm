from fastapi import APIRouter

from ...logic.v1 import user

app = APIRouter()


@app.get('/user/list')
def query_user_list():
    return user.query_user_list()


@app.get('/user')
def query_user(uid: int):
    return user.query_user(uid)
