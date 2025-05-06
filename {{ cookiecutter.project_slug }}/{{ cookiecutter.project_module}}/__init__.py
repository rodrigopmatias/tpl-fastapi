from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from {{cookiecutter.project_module}} import broker, logger, middlewares, routes
from {{cookiecutter.project_module}}.config import settings
from {{cookiecutter.project_module}}.life import life_control


def create_app() -> FastAPI:
    logger.setup()
    broker.setup()

    app = FastAPI(
        debug=settings.DEBUG,
        title="{{ cookiecutter.project_name }}",
        summary="{{ cookiecutter.description }}",
        description="{{ cookiecutter.description }}",
        version="{{ cookiecutter.api_version }}",
        openapi_url="/doc/openapi.json",
        docs_url="/doc/swagger",
        redoc_url=None,
        lifespan=life_control,
        default_response_class=ORJSONResponse,
    )

    middlewares.init_app(app)
    routes.init_app(app)

    return app
