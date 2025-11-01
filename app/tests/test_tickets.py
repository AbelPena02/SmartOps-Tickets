import pytest

@pytest.mark.asyncio
async def test_create_ticket(client):
    payload = {"title": "Server down", "description": "API not responding"}
    response = await client.post("/tickets/", json=payload)
    assert response.status_code == 200
    assert response.json()["title"] == "Server down"
