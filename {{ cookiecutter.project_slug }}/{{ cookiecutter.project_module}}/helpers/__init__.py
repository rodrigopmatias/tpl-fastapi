from typing import AsyncGenerator, TypeVar

T = TypeVar("T")


async def to_list(g: AsyncGenerator[T, None]) -> list[T]:
    return [item async for item in g]
