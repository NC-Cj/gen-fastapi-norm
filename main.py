from app.api.hello.v1.api import r
from app.app import app
from app.config.loadenv import loading_environment

loading_environment()

app.include_router(r)

# --app-dir main:app --host 0.0.0.0 --port 9000 --env-file .env --log-level warning --reload
# --app-dir main:app --host 0.0.0.0 --port 9000 --env-file .env --reload
