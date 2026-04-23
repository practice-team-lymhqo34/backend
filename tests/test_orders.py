import pytest
from fastapi import status
from httpx import AsyncClient

from app.enums import OrderStatus, UserRole


@pytest.mark.asyncio
async def test_create_order(client: AsyncClient):
    user_payload = {
        "email": "order_owner@example.com",
        "password": "password123",
        "full_name": "Order Owner",
        "role": UserRole.CLIENT,
        "phone_number": "+380990001122",
    }
    await client.post("/api/v1/auth/register", json=user_payload)

    login_data = {
        "email": "order_owner@example.com",
        "password": "password123",
    }
    await client.post("/api/v1/auth/login", json=login_data)

    order_payload = {
        "title": "Доставка будматеріалів",
        "description": "Привезти 10 мішків цементу",
        "weight": 500.5,
    }

    response = await client.post("/api/v1/orders/", json=order_payload)

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["title"] == order_payload["title"]
    assert data["description"] == order_payload["description"]
    assert data["weight"] == order_payload["weight"]
    assert data["status"] == OrderStatus.PENDING
    assert "id" in data
    assert "owner_id" in data


@pytest.mark.asyncio
async def test_create_order_unauthorized(client: AsyncClient):
    order_payload = {"title": "Спроба без логіну", "weight": 10.0}
    response = await client.post("/api/v1/orders/", json=order_payload)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Not authenticated"
