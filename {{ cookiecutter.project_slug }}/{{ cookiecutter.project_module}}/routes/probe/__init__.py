from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from pydantic import BaseModel
from {{cookiecutter.project_module}}.db import DBSessionFactory, db_session_factory
from {{cookiecutter.project_module}}.routes.probe import probes

router = APIRouter(prefix="/v1", tags=["probe"])


def init_app(app: FastAPI) -> None:
    app.include_router(router)


class ProbeMessage(BaseModel):
    message: str


@router.get("/live")
async def live(
    db_factory: DBSessionFactory = Depends(db_session_factory),
) -> ProbeMessage:
    result = await probes.is_ready(db_factory)

    if all(result.values()):
        return ProbeMessage(message="Im live!!!")

    raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, "service unavaliable")


@router.get("/ready")
async def ready(
    db_factory: DBSessionFactory = Depends(db_session_factory),
) -> ProbeMessage:
    result = await probes.is_ready(db_factory)

    if all(result.values()):
        return ProbeMessage(message="Im ready!!!")

    raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, "service unavaliable")
