from contextlib import asynccontextmanager
from logging import getLogger
from typing import Annotated, Any, AsyncGenerator, Callable, Generic, TypeVar

from pydantic import BaseModel, Field
from sqlalchemy import (
    BinaryExpression,
    ColumnElement,
    UnaryExpression,
    func,
    select,
    update,
)
from sqlalchemy.exc import DatabaseError
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from {{cookiecutter.project_module}}.helpers.models import DBModel

logger = getLogger(__name__)

type FilterExpression = UnaryExpression | BinaryExpression | ColumnElement


def extract_filters(
    values: dict[str, Any], filter_map: dict[str, Callable[[Any], FilterExpression]]
) -> list[FilterExpression]:
    sentences: list[FilterExpression] = []

    for attr, value in values.items():
        fn_filter = filter_map.get(attr)
        if fn_filter:
            sentences.append(fn_filter(value))

    return sentences


class EntityNotFoundError(Exception):
    pass


class DBController:
    def __init__(self, db_url: str, model_base: type[DBModel]) -> None:
        self._engine: AsyncEngine | None = None
        self._sessionmaker: async_sessionmaker[AsyncSession] | None = None
        self._migrated: bool = False
        self._db_url = db_url
        self._model_base = model_base

    @property
    def engine(self) -> AsyncEngine:
        if not self._engine:
            logger.info("inicializado engine de base de dados.")
            self._engine = create_async_engine(self._db_url)

        return self._engine

    @property
    def sessionmaker(self) -> async_sessionmaker[AsyncSession]:
        if not self._sessionmaker:
            logger.info("inicializando o construtor de sessões de base de dados")
            self._sessionmaker = async_sessionmaker(bind=self.engine)

        return self._sessionmaker

    async def migrate(self) -> None:
        if not self._migrated:
            async with self.engine.connect() as conn:
                logger.info("migrando base de dados")
                await conn.run_sync(
                    self._model_base.metadata.create_all, checkfirst=True
                )
                await conn.commit()

            self._migrated = True

    @asynccontextmanager
    async def begin(self):
        await self.migrate()
        session = self.sessionmaker()

        try:
            yield session
            await session.commit()
        except DatabaseError:
            await session.rollback()
            raise


M = TypeVar("M", bound=DBModel)
CP = TypeVar("CP", bound=BaseModel)
PUP = TypeVar("PUP", bound=BaseModel)
R = TypeVar("R", bound=BaseModel)


class BaseController(Generic[M, CP, PUP, R]):
    model: type[M]
    return_datatype: type[R]
    _db: DBController

    def __init__(self, db_url: str) -> None:
        type(self)._db = DBController(db_url, self.model)

    @property
    def joins(self) -> dict[type[DBModel], FilterExpression]:
        return {}

    @property
    def db(self) -> DBController:
        return type(self)._db

    async def exists(
        self,
        *,
        filters: list[FilterExpression] | None = None,
    ) -> bool:
        filters = filters if filters else []
        async with self.db.begin() as s:
            logger.info(
                f"verificando a existencia de {self.model.__tablename__} para o filtro"
            )
            stmt = select(func.count(self.model.id)).where(*filters).limit(1)

            for target, sentence in self.joins.items():
                stmt = stmt.join(target, sentence)

            return (await s.execute(stmt)).scalar_one() > 0

    async def count(
        self,
        *,
        filters: list[FilterExpression] | None = None,
    ) -> int:
        filters = filters if filters else []
        async with self.db.begin() as s:
            logger.info(
                f"contando os items de {self.model.__tablename__} para o filtro"
            )
            stmt = select(func.count(self.model.id)).where(*filters)

            for target, sentence in self.joins.items():
                stmt = stmt.join(target, sentence)

            return (await s.execute(stmt)).scalar_one()

    async def find(
        self,
        *,
        filters: list[FilterExpression] | None = None,
        ordering: list[UnaryExpression] | None = None,
        offset: Annotated[int, Field(ge=0)] = 0,
        limit: Annotated[int, Field(gt=0, le=100)] = 30,
    ) -> AsyncGenerator[R, Any]:
        filters = filters if filters else []
        ordering = ordering if ordering else []

        async with self.db.begin() as s:
            stmt = (
                select(self.model)
                .where(*filters)
                .order_by(*ordering)
                .offset(offset)
                .limit(limit)
            )

            for target, sentence in self.joins.items():
                stmt = stmt.join(target, sentence)

            logger.info(f"buscando itens em {self.model.__tablename__} para o filtro")
            result = await s.execute(stmt)
            for entity in result.scalars():
                yield self.return_datatype.model_validate(entity)

    async def update_or_create(
        self,
        id: int,
        payload: CP,
        allow_create: bool = True,
        extra_filters: list[FilterExpression] | None = None,
    ) -> tuple[bool, R]:
        async with self.db.begin() as s:
            sentences = [self.model.id == id, *(extra_filters if extra_filters else [])]
            stmt = select(self.model).where(*sentences)

            for target, sentence in self.joins.items():
                stmt = stmt.join(target, sentence)

            entity = (await s.execute(stmt)).scalar_one_or_none()

            if entity:
                logger.info(
                    f"atualizando os dados de {self.model.__tablename__} com id {id}"
                )
                await s.execute(
                    update(self.model)
                    .where(self.model.id == id)
                    .values(payload.model_dump(exclude_unset=True))
                )
                await s.commit()
                await s.refresh(entity)

                return False, self.return_datatype.model_validate(entity)

            if not allow_create:
                raise EntityNotFoundError(f"item com id {id} não foi encontrado.")

            entity = self.model(id=id, **payload.model_dump())
            logger.info(f"criando novo item {self.model.__tablename__} com id {id}")

            s.add(entity)
            await s.commit()
            await s.refresh(entity)

            return True, self.return_datatype.model_validate(entity)

    async def partial_update(
        self, id: int, payload: PUP, extra_filters: list[FilterExpression] | None = None
    ) -> R:
        async with self.db.begin() as s:
            sentences = [self.model.id == id, *(extra_filters if extra_filters else [])]
            stmt = select(self.model).where(*sentences)

            for target, sentence in self.joins.items():
                stmt = stmt.join(target, sentence)

            entity = (await s.execute(stmt)).scalar_one_or_none()

            if entity:
                logger.info(
                    f"atualizando os dados de {self.model.__tablename__} com id {id}"
                )
                await s.execute(
                    update(self.model)
                    .where(self.model.id == id)
                    .values(payload.model_dump(exclude_unset=True))
                )
                await s.commit()
                await s.refresh(entity)

                return self.return_datatype.model_validate(entity)

            logger.error(
                f"o item {self.model.__tablename__} com id {id} não foi encontrado"
            )
            raise EntityNotFoundError(f"item com id {id} não foi encontrado.")

    async def delete(
        self, id: int, extra_filters: list[FilterExpression] | None = None
    ) -> None:
        async with self.db.begin() as s:
            sentences = [self.model.id == id, *(extra_filters if extra_filters else [])]
            stmt = select(self.model).where(*sentences)

            for target, sentence in self.joins.items():
                stmt = stmt.join(target, sentence)

            entity = (await s.execute(stmt)).scalar_one_or_none()

            if entity:
                logger.error(
                    f"o item {self.model.__tablename__} com id {id} foi deletado"
                )

                await s.delete(entity)
                await s.commit()
                return

            logger.error(
                f"o item {self.model.__tablename__} com id {id} não foi encontrado"
            )
            raise EntityNotFoundError(f"item com id {id} não foi encontrado.")

    async def retrive(
        self, id: int, extra_filters: list[FilterExpression] | None = None
    ) -> R:
        async with self.db.begin() as s:
            logger.info(f"recuperando o item {self.model.__tablename__} com id {id}")
            sentences = [self.model.id == id, *(extra_filters if extra_filters else [])]
            stmt = select(self.model).where(*sentences)

            for target, sentence in self.joins.items():
                stmt = stmt.join(target, sentence)

            entity = (await s.execute(stmt)).scalar_one_or_none()

            if entity:
                return self.return_datatype.model_validate(entity)

            logger.error(
                f"o item {self.model.__tablename__} com id {id} não foi encontrado"
            )
            raise EntityNotFoundError(f"item com id {id} não foi encontrado.")

    async def create(self, payload: CP) -> R:
        async with self.db.begin() as s:
            entity = self.model(**payload.model_dump())
            logger.info(f"criando novo item {self.model.__tablename__}")
            s.add(entity)
            await s.commit()
            await s.refresh(entity)

            logger.info(
                f"criado novo item {self.model.__tablename__} com id {entity.id}"
            )
            return self.return_datatype.model_validate(entity)
