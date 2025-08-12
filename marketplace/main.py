from fastapi import FastAPI

from marketplace.api import api_router
from marketplace.containers.application import ApplicationContainer


def create_app() -> FastAPI:
    app = FastAPI(title="marketplace", version="0.1.0")

    container = ApplicationContainer()
    app.container = container
    container.wire(packages=["marketplace.products"])

    app.include_router(api_router)

    return app


app = create_app()
