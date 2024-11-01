from unittest import mock

import pytest
from fastapi import FastAPI

from fake_api.life import LifeControlTask, life_control


class TestLifeControl:
    def test_reset_tasks(self):
        life_control.reset_tasks()
        assert len(list(life_control.tasks)) == 0

    def test_include_life_task(self) -> None:
        life_control.reset_tasks()

        life_control.include_life_task("task-1", LifeControlTask())
        life_control.include_life_task("task-2", LifeControlTask())
        life_control.include_life_task("task-3", LifeControlTask())

        assert len(list(life_control.tasks)) == 3
        life_control.reset_tasks()

    @pytest.mark.asyncio
    @mock.patch("asyncio.BaseEventLoop.create_task", new_callable=mock.Mock)
    @mock.patch("fake_api.life.LifeControlTask.run", new_callable=mock.Mock)
    async def test_caller(
        self,
        mocked_task_run: mock.Mock,
        mocked_create_task: mock.Mock,
        app: FastAPI,
    ) -> None:
        life_control.reset_tasks()

        life_control.include_life_task("task-1", LifeControlTask())
        life_control.include_life_task("task-2", LifeControlTask())
        life_control.include_life_task("task-3", LifeControlTask())

        async with life_control(app):
            pass

        life_control.reset_tasks()
        assert mocked_create_task.call_count == 3
        assert mocked_task_run.call_count == 3
