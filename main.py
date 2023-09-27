from fastapi import FastAPI

from app import middlewares
from app.env import env
from app.routes.v1 import job

_environment = env.bool("PROD")
_host = env.str("HOST")
_port = env.int("PORT")

_prefix = "/api"
_project_name = "gen-fastapi-norm"
_version = "2.0"

# Prohibit the opening of document centers in production environments
_openapi_url = None if _environment else f"{_prefix}/openapi.json"
_docs_url = None if _environment else f"{_prefix}/docs"
_redoc_url = None

app = FastAPI(
    title=_project_name,
    version=_version,
    openapi_url=_openapi_url,
    docs_url=_docs_url,
    redoc_url=_redoc_url
)

middlewares.init_middlewares(app)
middlewares.init_exception_handler(app)

app.include_router(job.app, prefix=_prefix)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app", host=_host, port=_port)
