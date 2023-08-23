from fastapi import FastAPI

from app import middlewares
from app.env import env
from app.routes.v1 import job
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
middlewares.init_exception_handler(app)

# And so on for other routes and functions in your application
app.include_router(job.app, prefix=config.prefix)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(**config.server)
