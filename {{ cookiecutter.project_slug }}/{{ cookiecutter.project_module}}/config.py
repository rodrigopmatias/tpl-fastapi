from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class __Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=("prod.env", "stage.env", "dev.env"))

    DEBUG: bool = Field(
        default=True, description="Configura o serviço para rodar em modo debug."
    )

    DB_URL: str = Field(
        default="sqlite+aiosqlite://", description="Configura conexão com base de dados"
    )

    JWT_ALGORITHM: str = Field(
        default="RS256", description="Algoritimo de assinatura e criptografia do token"
    )

    JWT_SECERT_KEY_FILE: Path = Field(
        default="pub.pem",
        description="Arquivo que armazena a secret para validação do token",
    )


settings = __Settings()
