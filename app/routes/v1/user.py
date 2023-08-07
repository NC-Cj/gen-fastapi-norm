from fastapi import APIRouter

from ...logic.v1 import user

app = APIRouter()


@app.get('/user/list')
def query_user_list():
    return user.query_user_list()
