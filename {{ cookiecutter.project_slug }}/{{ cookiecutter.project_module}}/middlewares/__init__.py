from core_api.middlewares import request_id, took
from fastapi import FastAPI


def init_app(app: FastAPI) -> None:
    register_middleware = app.middleware("http")

    register_middleware(took.middleware)
    register_middleware(request_id.middleware)
