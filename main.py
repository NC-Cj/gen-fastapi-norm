from fastapi import FastAPI

from app import middlewares
from app.env import env
from app.routes.v1 import user
from initialization import go_init

config = go_init()

"""
Usually your project goes into production, and I don't recommend external access to your documentation
center unless you have specific requests
"""
if env.bool('PROD'):
    app = FastAPI(docs_url=None, redoc_url=None)
else:
    app = FastAPI(
        version='1.2.0',
        openapi_url=f'{config.prefix}/openapi.json',
        docs_url=f'{config.prefix}/docs'
    )

middlewares.init_middlewares(app)

app.include_router(user.app, prefix=config.prefix)

# And so on for other routes and functions in your application
if __name__ == '__main__':
    import uvicorn

    uvicorn.run(**config.server)
