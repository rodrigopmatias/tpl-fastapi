from typing import AsyncGenerator

from sqlalchemy import Integer
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from {{cookiecutter.project_module}}.config import settings

type DBSessionFactory = async_sessionmaker[AsyncSession]

class DBModel(DeclarativeBase):
    id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True)


class __DBSessionFactory:
    def __init__(self) -> None:
        self._engine: AsyncEngine | None = None
        self._migrated = False

    @property
    def is_migrated(self) -> bool:
        return self._migrated

    @property
    def engine(self) -> AsyncEngine:
        if not self._engine:
            self._engine = create_async_engine(settings.DB_URL)

        return self._engine

    async def _migrate(self) -> None:
        if not self.is_migrated:
            async with self.engine.connect() as conn:
                await conn.run_sync(DBModel.metadata.create_all)

            self._migrated = True

    async def __call__(self) -> AsyncGenerator[DBSessionFactory, None]:
        try:
            await self._migrate()
            yield async_sessionmaker(self.engine)
        finally:
            await self.engine.dispose()


db_session_factory = __DBSessionFactory()
