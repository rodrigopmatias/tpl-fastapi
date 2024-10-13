from unittest import mock

import pytest
from fastapi import status
from fastapi.testclient import TestClient


@pytest.mark.asyncio
async def test_live_return_ok(client: TestClient) -> None:
    resp = client.get("/v1/live")
    assert resp.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_ready_return_ok(client: TestClient) -> None:
    resp = client.get("/v1/ready")
    assert resp.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_ready_with_database_error(client: TestClient) -> None:
    with mock.patch(
        "sqlalchemy.ext.asyncio.AsyncSession.execute",
        new_callable=mock.AsyncMock,
        side_effect=Exception(),
    ):
        resp = client.get("/v1/ready")
        assert resp.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
