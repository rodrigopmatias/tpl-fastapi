import time
from typing import Awaitable, Callable

from fastapi import Request, Response


async def middleware(
    request: Request, next_call: Callable[[Request], Awaitable[Response]]
) -> Response:
    start_mark = time.perf_counter()
    response = await next_call(request)
    response.headers["x-took-response"] = (
        f"{(time.perf_counter() - start_mark):0.3f} segunds"
    )

    return response
