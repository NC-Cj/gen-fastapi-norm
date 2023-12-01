from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.middlewares import LoggingMiddleware, ExceptionHandlerMiddleware, RequestIDMiddleware
from app.routes.job.api import v1


# from app.project_rules import GlobalProjectResponses


def get_application():
    _app = FastAPI(
        # title=_project_name,
        # version=_version,
        # openapi_url=_openapi_url,
        # docs_url=_docs_url,
        # redoc_url=_redoc_url
    )

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # _app.add_middleware(LoggingMiddleware)
    _app.add_middleware(ExceptionHandlerMiddleware)
    _app.add_middleware(RequestIDMiddleware)

    return _app


app = get_application()
app.include_router(v1.router)
# --app-dir main:app --host 0.0.0.0 --port 9000 --env-file .env --log-level warning --reload
# --app-dir main:app --host 0.0.0.0 --port 9000 --env-file .env --reload
