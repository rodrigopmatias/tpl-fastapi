from unittest import mock

import pytest
from {{cookiecutter.project_module}}.emmiter import (
    EMMITER_CREATED,
    EMMITER_DELETED,
    EMMITER_UPDATED,
    BrokerEmmiter,
)


class TestBrokerEmmiter:

    @pytest.mark.asyncio
    @mock.patch("{{ cookiecutter.project_module }}.broker.broker.dispatch", new_callable=mock.AsyncMock)
    async def test_deleted_when_its_disabled(
        self, mocked_broker_dispatch: mock.AsyncMock
    ):
        emmiter = BrokerEmmiter("fake", 0)
        await emmiter.deleted({})

        assert mocked_broker_dispatch.await_count == 0

    @pytest.mark.asyncio
    @mock.patch("{{ cookiecutter.project_module }}.broker.broker.dispatch", new_callable=mock.AsyncMock)
    async def test_deleted_when_its_enabled(
        self, mocked_broker_dispatch: mock.AsyncMock
    ):
        emmiter = BrokerEmmiter("fake", EMMITER_DELETED)
        await emmiter.deleted({})

        assert mocked_broker_dispatch.await_count == 1

    @pytest.mark.asyncio
    @mock.patch("{{ cookiecutter.project_module }}.broker.broker.dispatch", new_callable=mock.AsyncMock)
    async def test_updated_when_its_disabled(
        self, mocked_broker_dispatch: mock.AsyncMock
    ):
        emmiter = BrokerEmmiter("fake", 0)
        await emmiter.updated({}, {})

        assert mocked_broker_dispatch.await_count == 0

    @pytest.mark.asyncio
    @mock.patch("{{ cookiecutter.project_module }}.broker.broker.dispatch", new_callable=mock.AsyncMock)
    async def test_updated_when_its_enabled(
        self, mocked_broker_dispatch: mock.AsyncMock
    ):
        emmiter = BrokerEmmiter("fake", EMMITER_UPDATED)
        await emmiter.updated({}, {})

        assert mocked_broker_dispatch.await_count == 1

    @pytest.mark.asyncio
    @mock.patch("{{ cookiecutter.project_module }}.broker.broker.dispatch", new_callable=mock.AsyncMock)
    async def test_created_when_its_disabled(
        self, mocked_broker_dispatch: mock.AsyncMock
    ):
        emmiter = BrokerEmmiter("fake", 0)
        await emmiter.created({})

        assert mocked_broker_dispatch.await_count == 0

    @pytest.mark.asyncio
    @mock.patch("{{ cookiecutter.project_module }}.broker.broker.dispatch", new_callable=mock.AsyncMock)
    async def test_created_when_its_enabled(
        self, mocked_broker_dispatch: mock.AsyncMock
    ):
        emmiter = BrokerEmmiter("fake", EMMITER_CREATED)
        await emmiter.created({})

        assert mocked_broker_dispatch.await_count == 1
