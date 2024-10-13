from typing import Any

import pytest
from fastapi import status
from fastapi.testclient import TestClient


@pytest.mark.asyncio
async def test_who_are_you_when_user_authenticated(
    authorized_client: TestClient, user_data: dict[str, Any]
) -> None:
    resp = authorized_client.get("/v1/auth/who-are-you")

    assert resp.status_code == status.HTTP_200_OK
    assert resp.json() == user_data


@pytest.mark.asyncio
async def test_who_are_you_with_bad_authorization(client: TestClient) -> None:
    resp = client.get(
        "/v1/auth/who-are-you", headers={"authorization": "Bearer bad-authorization"}
    )
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_who_are_you_when_user_is_not_authenticated(client: TestClient) -> None:
    resp = client.get("/v1/auth/who-are-you")
    assert resp.status_code == status.HTTP_403_FORBIDDEN
