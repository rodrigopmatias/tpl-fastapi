from unittest import mock

import pytest
from {{cookiecutter.project_module}} import broker


@pytest.mark.asyncio
@mock.patch("asyncio.sleep", new_callable=mock.AsyncMock)
@mock.patch("asyncio.Queue.empty", return_value=True)
async def test_broker_dry_when_queue_is_empty(
    mocked_empty: mock.AsyncMock,
    mocked_sleep: mock.AsyncMock,
) -> None:
    with mock.patch(
        "{{ cookiecutter.project_module }}.broker.__broker_dry.is_running", side_effect=[True, False]
    ):
        await broker.__broker_dry.run()

    assert mocked_sleep.await_count == 1
    assert mocked_empty.call_count == 1


@pytest.mark.asyncio
@mock.patch("asyncio.sleep", new_callable=mock.AsyncMock)
@mock.patch("asyncio.Queue.empty", return_value=False)
@mock.patch(
    "asyncio.Queue.get",
    new_callable=mock.AsyncMock,
    return_value=broker.Envelop(
        target="fake", routing_key="fake", header=broker.EnvelopHeader(), body={}
    ),
)
async def test_broker_dry_when_queue_have_message(
    mocked_queue_get: mock.AsyncMock,
    mocked_empty: mock.AsyncMock,
    mocked_sleep: mock.AsyncMock,
) -> None:
    with mock.patch(
        "{{ cookiecutter.project_module }}.broker.__broker_dry.is_running", side_effect=[True, False]
    ):
        await broker.__broker_dry.run()

    assert mocked_sleep.await_count == 0
    assert mocked_empty.call_count == 1
    assert mocked_queue_get.await_count == 1


@pytest.mark.asyncio
@mock.patch("sys.exit")
async def test_broker_amqp_when_run_raise_exception(
    mocked_exit: mock.Mock,
) -> None:
    with mock.patch(
        "{{ cookiecutter.project_module }}.broker.__BrokerAMQP._run",
        new_callable=mock.AsyncMock,
        side_effect=Exception("fake-exception"),
    ):
        await broker.__broker_amqp.run()

    mocked_exit.assert_called_with(100)


@pytest.mark.asyncio
@mock.patch("asyncio.Queue.empty", return_value=True)
@mock.patch("asyncio.sleep", new_callable=mock.AsyncMock)
@mock.patch("aio_pika.connect_robust", new_callable=mock.AsyncMock)
async def test_broker_amqp_when_queue_empty(
    mocked_connect_robust: mock.AsyncMock,
    mocked_sleep: mock.AsyncMock,
    mocked_empty: mock.Mock,
) -> None:
    with mock.patch(
        "{{ cookiecutter.project_module }}.broker.__broker_amqp.is_running", side_effect=[True, False]
    ):
        await broker.__broker_amqp.run()

    assert mocked_empty.call_count == mocked_sleep.await_count
    mocked_connect_robust.assert_awaited()


@pytest.mark.asyncio
@mock.patch("asyncio.Queue.empty", return_value=False)
@mock.patch("asyncio.sleep", new_callable=mock.AsyncMock)
@mock.patch("aio_pika.connect_robust", new_callable=mock.AsyncMock)
@mock.patch(
    "asyncio.Queue.get",
    new_callable=mock.AsyncMock,
    return_value=broker.Envelop(target="fake", routing_key="fake", body={}),
)
async def test_broker_amqp_when_with_messages(
    mocked_queue_get: mock.AsyncMock,
    mocked_connect_robust: mock.AsyncMock,
    mocked_sleep: mock.AsyncMock,
    mocked_empty: mock.Mock,
) -> None:
    with mock.patch(
        "{{ cookiecutter.project_module }}.broker.__broker_amqp.is_running", side_effect=[True, False]
    ):
        await broker.__broker_amqp.run()

    assert mocked_empty.call_count == 1
    assert mocked_sleep.await_count == 0
    assert mocked_queue_get.await_count == 1
    mocked_connect_robust.assert_awaited()


@pytest.mark.asyncio
@mock.patch("asyncio.Queue.put")
async def test_dispatch_message(mocked_queue_put: mock.AsyncMock) -> None:
    await broker.dispatch("fake", "fake", {})
    assert mocked_queue_put.await_count == 1


@pytest.mark.asyncio
@mock.patch("asyncio.Queue.put")
async def test_dispatch_message_by_dry(mocked_queue_put: mock.AsyncMock) -> None:
    await broker.dispatch_by_dry("fake", "fake", {})
    assert mocked_queue_put.await_count == 1


@pytest.mark.asyncio
@mock.patch("asyncio.Queue.put")
async def test_dispatch_message_by_amqp(mocked_queue_put: mock.AsyncMock) -> None:
    await broker.dispatch_by_amqp("fake", "fake", {})
    assert mocked_queue_put.await_count == 1
