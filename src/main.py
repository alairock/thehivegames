from fastapi import FastAPI
from starlette.middleware import Middleware
from src.databse import async_setup
from src.routes import routes
from src.utils.context import DBContextMiddleware

app = FastAPI(routes=routes(), middleware=[Middleware(DBContextMiddleware)])
app.on_event("startup")(async_setup(app))
