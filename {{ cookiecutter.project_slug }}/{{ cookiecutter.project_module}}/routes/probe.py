from fastapi import APIRouter, Depends, FastAPI, Response, status
from pydantic import BaseModel
from sqlalchemy import select, text
from {{cookiecutter.project_module}}.db import Datasource, datasource

router = APIRouter(prefix="/v1", tags=["probe"])


def init_app(app: FastAPI) -> None:
    app.include_router(router)


class ProbeMessage(BaseModel):
    message: str


@router.get("/live")
async def live() -> ProbeMessage:
    return ProbeMessage(message="Im live!!!")


@router.get("/ready")
async def ready(
    response: Response, db: Datasource = Depends(datasource)
) -> ProbeMessage:
    try:
        async with db() as s:
            await s.execute(select(text("1")))

        return ProbeMessage(message="Im ready!!!")
    except Exception:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return ProbeMessage(message="database is not ready")
