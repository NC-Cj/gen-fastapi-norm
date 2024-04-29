from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.middlewares.middlewares import RequestIDMiddleware


def _get_application():
    _app = FastAPI()

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    _app.add_middleware(RequestIDMiddleware)

    return _app


app = _get_application()
