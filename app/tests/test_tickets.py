import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_create_ticket():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        payload = {"title": "Server down", "description": "API not responding"}
        response = await ac.post("/tickets/", json=payload)
    assert response.status_code == 200
    assert response.json()["title"] == "Server down"
