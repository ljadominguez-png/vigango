"""Test the API health endpoint and its expected response."""

from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


# Verify that the health endpoint returns HTTP 200 and an OK status.
def test_health_returns_ok():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
