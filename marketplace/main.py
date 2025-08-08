from fastapi import FastAPI

from marketplace.presentation.api import api_router


def create_app() -> FastAPI:
    app = FastAPI(title="marketplace", version="0.1.0")

    # Routers
    app.include_router(api_router)

    return app


app = create_app()
