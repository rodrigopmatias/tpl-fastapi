from fastapi import FastAPI
from {{cookiecutter.project_module}}.middlewares import request_id, took


def init_app(app: FastAPI) -> None:
    register_middleware = app.middleware("http")

    register_middleware(took.middleware)
    register_middleware(request_id.middleware)
