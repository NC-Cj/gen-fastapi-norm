from fastapi import FastAPI, Request

from app import middlewares
from app.env import env
from app.routers import user

prefix = "/api"

if env.bool('PROD'):
    app = FastAPI(docs_url=None, redoc_url=None)
else:
    app = FastAPI(
        version='1.2.0',
        openapi_url=f'{prefix}/openapi.json',
        docs_url=f'{prefix}/docs'
    )

middlewares.add_middlewares(app)


# Add request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    # Log the request
    print(f"Received request: {request.method} {request.url}")

    # Call the next middleware or route handler
    response = await call_next(request)

    # Log the response
    print(f"Sent response: {response.status_code}")

    return response


app.include_router(user.app, prefix=prefix)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=9000, reload=True)
