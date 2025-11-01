from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_ticket():
    payload = {"title": "Server down", "description": "API not responding"}
    response = client.post("/tickets/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Server down"
    assert data["description"] == "API not responding"
