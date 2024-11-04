import logging
from fastapi import FastAPI

from .routers import login


def add_routes(app: FastAPI) -> None:
    prefix = "/login/api"
    app.include_router(login.router, prefix=prefix)


def create_app() -> FastAPI:
    app = FastAPI(
        title="Login Api",
        version="1.0.0",
        description="Create and manage login credentials",
        docs_url="/docs",
    )
    logging.info("Adding routes")
    add_routes(app)
    return app


app = create_app()
