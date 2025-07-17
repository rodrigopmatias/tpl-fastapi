from core_api.auth import User
from fastapi import APIRouter, Depends, FastAPI
from {{cookiecutter.project_module}}.auth import current_user

router = APIRouter(prefix="/v1/auth", tags=["auth"])


def init_app(app: FastAPI) -> None:
    app.include_router(router)


@router.get("/who-are-you")
async def who_are_you(user: User = Depends(current_user)) -> User:
    return user
