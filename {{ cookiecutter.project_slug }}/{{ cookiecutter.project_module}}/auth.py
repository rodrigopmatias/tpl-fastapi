from logging import getLogger
from pathlib import Path
from typing import Any

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel
from {{cookiecutter.project_module}}.config import settings

get_authorization = HTTPBearer()
logger = getLogger(__name__)
BUFFER_CHUNK_SIZE = 8192

class User(BaseModel):
    id: int
    email: str
    is_admin: bool
    roles: list[str]

    def allowed(self, role: str) -> bool:
        return  self.is_admin or role in self.roles

def load_key(filepath: Path) -> str:
    buffer = ""

    with filepath.open() as fp:
        for chunk in iter(lambda: fp.read(BUFFER_CHUNK_SIZE), ""):
            buffer += chunk

    return buffer[:-1] if buffer[-1] == '\n' else buffer


def current_user(
    authorization: HTTPAuthorizationCredentials = Depends(get_authorization),
) -> User:
    try:
        key = load_key(settings.JWT_SECERT_KEY_FILE)
        
        logger.info("verificando token de autorização.")
        data: dict[str, Any] = jwt.decode(
            authorization.credentials, key, algorithms=[settings.JWT_ALGORITHM], verify=True
        )

        user = User(**data.get("user", {}))
        logger.info(
            f"autorização validada para o usuário com id {user.id} "
            f"como {'administrador' if user.is_admin else 'usuário comum'}"
        )
        return user
    except Exception as e:
        logger.warning("a autorização não passou pela validação")
        logger.error(f"{type(e)}: {e}")

        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "invalid token")
