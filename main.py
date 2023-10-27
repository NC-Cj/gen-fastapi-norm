from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.middlewares import LoggingMiddleware, ExceptionHandlerMiddleware, RequestIDMiddleware
from app.project_rules import GlobalProjectResponses
from app.routes.job.api import v1


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

    _app.add_middleware(LoggingMiddleware)
    _app.add_middleware(ExceptionHandlerMiddleware)
    _app.add_middleware(RequestIDMiddleware)

    return _app


app = get_application()
app.include_router(v1.router, responses=GlobalProjectResponses)

# _environment = env.bool("PROD")

#
# _project_name = "gen-fastapi-norm-template"
# _prefix = "/api"
# _version = "2.0"
#
# # Prohibit the opening of document centers in production environments
# _openapi_url = None if _environment else f"{_prefix}/openapi.json"
# _docs_url = None if _environment else f"{_prefix}/docs"
# _redoc_url = None
#
# app = FastAPI(
#     title=_project_name,
#     version=_version,
#     openapi_url=_openapi_url,
#     docs_url=_docs_url,
#     redoc_url=_redoc_url
# )
#
# middlewares.init_middlewares(app)
# middlewares.init_exception_handler(app)
#
# app.include_router(job.app, prefix=_prefix, responses=GlobalProjectResponses)
# # app.include_router(you_routes.app, prefix=_prefix, responses=GlobalProjectResponses)
#
