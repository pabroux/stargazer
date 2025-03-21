"""Tests for the router of the Status app.

This module contains tests for Status-related endpoints.
"""

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_health_check() -> None:
    """Tests the /health endpoint.

    GET /health returns a 200 with a JSON body of {"status": "healthy"}.
    """
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
