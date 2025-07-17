import asyncio
from logging import getLogger

from core_controller.controllers import DBController
from sqlalchemy import select, text
from {{cookiecutter.project_module}}.broker import broker

logger = getLogger(__name__)


async def is_database_ready(db: DBController) -> bool:
    result = True

    try:
        async with db.begin() as s:
            await s.execute(select(text("1")))
    except Exception as e:
        logger.error(e)
        result = False

    return result


async def is_broker_ready() -> bool:
    await broker.dispatch("health", body={})
    await asyncio.sleep(0.1)

    return broker.is_running()


async def is_ready(db: DBController) -> dict[str, bool]:
    return {
        "db": await is_database_ready(db),
        "broker": await is_broker_ready(),
    }
