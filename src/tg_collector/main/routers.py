from fastapi import FastAPI

from tg_collector.web import(
    dashboard_router,
    post_router,
)


def init_routers(app: FastAPI) -> None:
    app.include_router(dashboard_router)
    app.include_router(post_router)
