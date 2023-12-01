from fastapi import APIRouter

from app.routes.job.logic import v1

router = APIRouter()


@router.get("/list")
async def query_list():
    return await v1.query_list()


@router.post("/list")
async def add_list():
    return await v1.add_list()


@router.put("/list")
async def raise_list():
    return await v1.raise_list()


@router.delete("/list/{id}")
async def delete_list(id: str):
    return await v1.delete_list(id)
