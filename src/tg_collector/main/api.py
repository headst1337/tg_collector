from fastapi import FastAPI

from .routers import init_routers
from .dependencies import init_dependencies


def create_app() -> FastAPI:
    app = FastAPI(title='TG Collector', version='0.1.0')
    init_routers(app)
    init_dependencies(app)
    return app
