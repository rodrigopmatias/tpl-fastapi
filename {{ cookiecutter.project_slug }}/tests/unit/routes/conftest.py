from pathlib import Path
from typing import Any

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from jose import jwt
from {{cookiecutter.project_module}} import create_app
from {{cookiecutter.project_module}}.auth import load_key
from {{cookiecutter.project_module}}.config import settings


def change_settings() -> None:
    settings.DB_URL = "sqlite+aiosqlite://"
    settings.JWT_ALGORITHM = "HS256"
    settings.JWT_SECERT_KEY_FILE = Path("pub.key")


@pytest.fixture()
def app() -> FastAPI:
    change_settings()
    return create_app()


@pytest.fixture()
def client(app: FastAPI) -> TestClient:
    return TestClient(app)


@pytest.fixture()
def user_data() -> dict[str, Any]:
    return {
        "id": 1,
        "email": "fake@email.com",
        "is_admin": False,
        "roles": ["role1", "role2"],
    }


@pytest.fixture()
def authorization(user_data: dict[str, Any]) -> str:
    change_settings()

    return jwt.encode(
        {"user": user_data},
        load_key(settings.JWT_SECERT_KEY_FILE),
        settings.JWT_ALGORITHM,
    )


@pytest.fixture()
def authorized_client(app: FastAPI, authorization: str) -> TestClient:
    return TestClient(app, headers={"authorization": f"Bearer {authorization}"})
