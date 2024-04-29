from app.api.hello.logic.logic import HelloController
from fastapi import APIRouter, Request

r = APIRouter()


@r.get("/hello/{name}")
async def hello(req: Request, name: str):
    ctrl = HelloController(req)
    return await ctrl.hello(name)
