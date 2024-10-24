from typing import Any

from machine_api.broker import broker

EMMITER_CREATED = 0b0001
EMMITER_UPDATED = 0b0010
EMMITER_DELETED = 0b0100
EMMITER_ALL = EMMITER_CREATED | EMMITER_UPDATED | EMMITER_DELETED


class BrokerEmmiter:
    def __init__(self, target: str, options: int = EMMITER_ALL) -> None:
        self._target = target
        self._options = options

    @property
    def target(self) -> str:
        return self._target

    @property
    def options(self) -> int:
        return self._options

    async def created(self, instance: dict[str, Any]) -> None:
        if self.options & EMMITER_CREATED == EMMITER_CREATED:
            await broker.dispatch(self.target, "created", {"instance": instance})

    async def updated(self, instance: dict[str, Any], older: dict[str, Any]) -> None:
        if self.options & EMMITER_UPDATED == EMMITER_UPDATED:
            await broker.dispatch(
                self.target, "updated", {"instance": instance, "older": older}
            )

    async def deleted(self, instance: dict[str, Any]) -> None:
        if self.options & EMMITER_DELETED == EMMITER_DELETED:
            await broker.dispatch(self.target, "deleted", {"instance": instance})
