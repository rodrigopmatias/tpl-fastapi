from fastapi import FastAPI
from {{cookiecutter.project_module}}.routes import auth, probe


def init_app(app: FastAPI) -> None:
    auth.init_app(app)
    probe.init_app(app)
