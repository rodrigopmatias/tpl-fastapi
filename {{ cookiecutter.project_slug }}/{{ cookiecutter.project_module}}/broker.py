import asyncio
import sys
from asyncio import Queue
from importlib import metadata
from logging import getLogger
from typing import Any
from uuid import uuid4

import aio_pika
import orjson as json
from pydantic import BaseModel, Field
from {{cookiecutter.project_module}}.config import settings
from {{cookiecutter.project_module}}.life import LifeControlTask, life_control
from {{cookiecutter.project_module}}.middlewares import request_id

logger = getLogger(__name__)
APP_USER_AGENT = f"{{ cookiecutter.project_slug }}/v{metadata.version('{{ cookiecutter.project_slug }}')}"

def setup():
    life_control.include_life_task(
        f"broker-{'dry' if settings.BROKER_DRY else 'amqp'}", broker
    )


class EnvelopHeader(BaseModel):
    trace_id: str = Field(default_factory=lambda: str(uuid4()))
    attempts: int = Field(default=0)
    total_attempts: int = Field(default=0)
    errors: list[str] = Field(default_factory=lambda: [])


class Envelop(BaseModel):
    target: str
    routing_key: str = Field(default="")
    header: EnvelopHeader = Field(default_factory=lambda: EnvelopHeader())
    body: dict[str, Any]


class __Broker(LifeControlTask):
    def __init__(self, queue_size: int = 30) -> None:
        self._queue: Queue[Envelop] = Queue(queue_size)

    def is_running(self) -> bool:  # pragma: nocover
        return True

    async def dispatch(
        self,
        target: str,
        routing_key: str = "",
        body: dict[str, Any] = Field(default_factory=lambda: {}),
    ) -> None:
        await self._queue.put(
            Envelop(
                target=target,
                routing_key=routing_key,
                body=body,
                header=EnvelopHeader(trace_id=request_id.restore()),
            )
        )


class __BrokerDRY(__Broker):
    async def run(self) -> None:
        while self.is_running():
            if self._queue.empty():
                await asyncio.sleep(0.1)
                continue

            envelop = await self._queue.get()
            request_id.store(envelop.header.trace_id)

            logger.info(
                json.dumps(
                    envelop.model_dump(), default=str, option=json.OPT_INDENT_2
                ).decode()
            )


class __BrokerAMQP(__Broker):
    async def run(self) -> None:
        try:
            await self._run()
        except Exception as e:
            logger.error(e)
            sys.exit(100)

    async def _run(self) -> None:
        async with await aio_pika.connect_robust(settings.BROKER_URL) as amqp_conn:
            while self.is_running():
                if self._queue.empty():
                    await asyncio.sleep(0.1)
                    continue

                envelop = await self._queue.get()
                request_id.store(envelop.header.trace_id)

                logger.info(
                    f"enviando mensagem para {envelop.target}:{envelop.routing_key}"
                )
                ch = await amqp_conn.channel()
                exchange = await ch.get_exchange(envelop.target)

                await exchange.publish(
                    aio_pika.Message(
                        json.dumps(
                            {
                                "header": envelop.header.model_dump(),
                                "body": envelop.body,
                            },
                            default=str,
                            option=json.OPT_INDENT_2,
                        ),
                        app_id=APP_USER_AGENT,
                        content_type="application/json",
                        correlation_id=envelop.header.trace_id,
                    ),
                    routing_key=envelop.routing_key,
                )


__broker_dry = __BrokerDRY()
__broker_amqp = __BrokerAMQP()

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
