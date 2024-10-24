import asyncio
from contextlib import asynccontextmanager
from logging import getLogger
from typing import AsyncGenerator

from fastapi import FastAPI

logger = getLogger(__name__)


class LifeControlTask:
    async def run(self) -> None:
        pass


class __LifeControl:

    def __init__(self) -> None:
        self._tasks: list[tuple[str, LifeControlTask]] = []

    def include_life_task(self, name: str, task: LifeControlTask) -> None:
        self._tasks.append((name, task))

    @asynccontextmanager
    async def __call__(self, _app: FastAPI) -> AsyncGenerator[None, None]:
        loop = asyncio.get_running_loop()

        logger.info("LifeControl will initialize tasks")
        for name, task in self._tasks:
            loop.create_task(task.run(), name=f"life_control_task({name})")
            logger.info(f"task {name} initialized.")

        yield


life_control = __LifeControl()
