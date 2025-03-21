"""Tests for the router of the Auth app.

This module contains tests for Auth-related endpoints.
"""

from fastapi import status
from fastapi.testclient import TestClient
from pytest_mock import MockerFixture

from apps.auth.models import User
from apps.auth.utils import get_password_hash
from main import app

client = TestClient(app)


def test_login_for_access_token(mocker: MockerFixture) -> None:
    """Tests the /login_for_access_token endpoint.

    Tests the response is a 200 OK with a JSON body containing
    {"access_token": <str>, "token_type": "bearer"}.
    """

    # Mock the `get_user_by_username` function
    get_user_by_username = mocker.patch("apps.auth.utils.get_user_by_username")
    get_user_by_username.return_value = User(
        username="pabroux",
        email="pabroux@stargazer.com",
        hashed_password=f"{get_password_hash("password")}",
        disabled=False,
    )
    response = client.post(
        "/token",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        data={
            "grant_type": "password",
            "username": "pabroux",
            "password": "password",
        },
    )
    response_json = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert response_json.keys() == {"access_token", "token_type"}
    assert response_json["token_type"] == "bearer"
    assert isinstance(response_json["access_token"], str)
