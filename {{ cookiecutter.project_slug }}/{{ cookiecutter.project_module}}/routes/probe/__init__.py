from core_controller.controllers import DBController
from core_controller.models import DBModel
from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from pydantic import BaseModel
from {{cookiecutter.project_module}}.config import settings
from {{cookiecutter.project_module}}.routes.probe import probes

router = APIRouter(prefix="/v1", tags=["probe"])


def factory_db() -> DBController:
    return DBController(settings.DB_URL, DBModel)


def init_app(app: FastAPI) -> None:
    app.include_router(router)


class ProbeMessage(BaseModel):
    message: str


@router.get("/live")
async def live(
    db: DBController = Depends(factory_db),
) -> ProbeMessage:
    result = await probes.is_ready(db)

    if all(result.values()):
        return ProbeMessage(message="Im live!!!")

    raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, "service unavaliable")


@router.get("/ready")
async def ready(
    db: DBController = Depends(factory_db),
) -> ProbeMessage:
    result = await probes.is_ready(db)

    if all(result.values()):
        return ProbeMessage(message="Im ready!!!")

    raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, "service unavaliable")
