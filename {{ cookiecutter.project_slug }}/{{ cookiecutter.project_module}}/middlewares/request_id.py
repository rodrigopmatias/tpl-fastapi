from contextvars import ContextVar
from typing import Awaitable, Callable
from uuid import uuid4

from fastapi import Request, Response

__context = ContextVar[str]("request_id_ctx", default="***")


def store(value: str) -> None:
    __context.set(value)


def restore() -> str:
    return __context.get()


async def middleware(
    request: Request, next_call: Callable[[Request], Awaitable[Response]]
) -> Response:
    req_id = request.headers.get("x-request-id", str(uuid4()))
    store(req_id)

    response = await next_call(request)
    response.headers["x-request-id"] = req_id

    return response
