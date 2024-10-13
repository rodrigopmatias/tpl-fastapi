from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from {{cookiecutter.project_module}} import routes
from {{cookiecutter.project_module}}.config import settings


def create_app() -> FastAPI:
    app = FastAPI(
        debug=settings.DEBUG,
        title="{{ cookiecutter.project_name }}",
        summary="{{ cookiecutter.description }}",
        description="{{ cookiecutter.description }}",
        version="{{ cookiecutter.api_version }}",
        openapi_url="/doc/openapi.json",
        docs_url="/doc/swagger",
        redoc_url=None,
        default_response_class=ORJSONResponse,
    )

    routes.init_app(app)

    return app
