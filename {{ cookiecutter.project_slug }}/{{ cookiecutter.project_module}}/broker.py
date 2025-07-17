from importlib import metadata
from logging import getLogger
from typing import Any

from core_api.broker import BrokerAMQP, BrokerDRY
from core_api.life import life_control
from pydantic import Field
from {{cookiecutter.project_module}}.config import settings

logger = getLogger(__name__)
APP_USER_AGENT = f"{{ cookiecutter.project_slug }}/v{metadata.version('{{ cookiecutter.project_slug }}')}"

def setup():
    life_control.include_life_task(
        f"broker-{'dry' if settings.BROKER_DRY else 'amqp'}", broker
    )

__broker_dry = BrokerDRY()
__broker_amqp = BrokerAMQP(settings.BROKER_URL, APP_USER_AGENT)

broker = __broker_dry if settings.BROKER_DRY else __broker_amqp

async def dispatch(
    target: str,
    routing_key: str = "",
    body: dict[str, Any] = Field(default_factory=lambda: {}),
) -> None:
    await broker.dispatch(target, routing_key, body)


async def dispatch_by_dry(
    target: str,
    routing_key: str = "",
    body: dict[str, Any] = Field(default_factory=lambda: {}),
) -> None:
    await __broker_dry.dispatch(target, routing_key, body)


async def dispatch_by_amqp(
    target: str,
    routing_key: str = "",
    body: dict[str, Any] = Field(default_factory=lambda: {}),
) -> None:
    await __broker_amqp.dispatch(target, routing_key, body)
