"""Tests for the router of the Auth app.

This module contains tests for Auth-related endpoints.
"""

from copy import deepcopy

from fastapi import status
from fastapi.testclient import TestClient
from pytest_mock import MockerFixture

from apps.auth.tests.utils import mock_get_user_by_username
from apps.shared.utils import get_formatted_content
from main import app

client = TestClient(app)

fake_data = {
    "grant_type": "password",
    "username": "pabroux",
    "password": "password",
}


def test_login_for_access_token(mocker: MockerFixture) -> None:
    """Tests the /login_for_access_token endpoint.

    Tests the response is a 200 OK with a JSON body containing
    {"access_token": <str>, "token_type": "bearer"}.

    Args:
        mocker (MockerFixture): The mocker fixture used to mock functions.
    """

    # Mock the `get_user_by_username` function
    mock_get_user_by_username(mocker)

    response = client.post(
        "/token",
        data=fake_data,
    )
    response_json = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert response_json.keys() == {"access_token", "token_type"}
    assert response_json["token_type"] == "bearer"
    assert isinstance(response_json["access_token"], str)


def test_login_for_access_token_invalid_credentials(mocker: MockerFixture) -> None:
    """Tests the /login_for_access_token endpoint with invalid credentials.

    Tests the response is a 401 Unauthorized with a JSON body containing
    at least {"message": "Incorrect username or password", "status": 401}.

    Args:
        mocker (MockerFixture): The mocker fixture used to mock functions.
    """

    # Mock the `get_user_by_username` function
    mock_get_user_by_username(mocker)

    fake_data_invalid_password = deepcopy(fake_data)
    fake_data_invalid_password["password"] = "invalid_password"

    response_invalid_password = client.post(
        "/token",
        data=fake_data_invalid_password,
    )

    assert response_invalid_password.status_code == status.HTTP_401_UNAUTHORIZED
    assert response_invalid_password.json() == get_formatted_content(
        "Incorrect username or password", status.HTTP_401_UNAUTHORIZED
    )


def test_login_for_access_token_invalid_grant_type(mocker: MockerFixture) -> None:
    """Tests the /login_for_access_token endpoint with invalid grant_type.

    Tests the response is a 422 Unprocessable Entity with a JSON body containing
    at least {"message": "Invalid input", "status": 422, "detail": <str>}.

    Args:
        mocker (MockerFixture): The mocker fixture used to mock functions.
    """

    # Mock the `get_user_by_username` function
    mock_get_user_by_username(mocker)

    fake_data_invalid_grant = deepcopy(fake_data)
    fake_data_invalid_grant["grant_type"] = "invalid_grant"

    response_invalid_password = client.post(
        "/token",
        data=fake_data_invalid_grant,
    )

    response_json = response_invalid_password.json()

    assert response_invalid_password.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "detail" in response_json
    del response_json["detail"]
    assert response_json == get_formatted_content(
        "Invalid input", status.HTTP_422_UNPROCESSABLE_ENTITY
    )


def test_login_for_access_token_invalid_input(mocker: MockerFixture) -> None:
    """Tests the /login_for_access_token endpoint with invalid inputs.

    Tests the response is a 422 Unprocessable Entity with a JSON body containing
    at least {"message": "Invalid input", "status": 422, "detail": <str>}.

    Args:
        mocker (MockerFixture): The mocker fixture used to mock functions.
    """

    # Mock the `get_user_by_username` function
    mock_get_user_by_username(mocker)

    for key in fake_data:
        fake_data_no_key = deepcopy(fake_data)
        del fake_data_no_key[key]

        response_no_key = client.post(
            "/token",
            data=fake_data_no_key,
        )

        response_json = response_no_key.json()

        assert response_no_key.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert "detail" in response_json
        del response_json["detail"]
        assert response_json == get_formatted_content(
            "Invalid input", status.HTTP_422_UNPROCESSABLE_ENTITY
        )
