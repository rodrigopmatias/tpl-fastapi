from typing import AsyncGenerator

from sqlalchemy import Integer
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from {{cookiecutter.project_module}}.config import settings

type Datasource = async_sessionmaker[AsyncSession]


class DBModel(DeclarativeBase):
    id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True)


async def migrate(bind: AsyncEngine) -> None:
    async with bind.connect() as conn:
        await conn.run_sync(DBModel.metadata.create_all)


async def datasource() -> AsyncGenerator[Datasource, None]:
    try:
        bind = create_async_engine(settings.DB_URL)
        await migrate(bind)
        yield async_sessionmaker(bind)
    finally:
        await bind.dispose()
