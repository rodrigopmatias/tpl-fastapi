from typing import Annotated, Generic, TypeVar

from pydantic import BaseModel, Field

BM = TypeVar("BM", bound=BaseModel)


class BaseResultSet(BaseModel, Generic[BM]):
    count: Annotated[int, Field(ge=0)] = 0
    next: str | None = None
    previous: str | None = None
    items: list[BM] = Field(default_factory=list)


class BaseQueryParam(BaseModel):
    offset: Annotated[int, Field(ge=0)] = 0
    limit: Annotated[int, Field(ge=1, le=100)] = 30
