"""Tests for the utilities of the Auth app.

This module contains tests for utility functions dedicated to authenticate users.
"""

from datetime import timedelta

import pytest
from fastapi import HTTPException
from pytest_mock import MockerFixture

from apps.auth.models import User
from apps.auth.tests.utils import mock_get_user_by_username
from apps.auth.utils import (
    authenticate_user,
    create_access_token,
    get_current_active_user,
    get_current_user,
    get_password_hash,
    verify_password,
)


def test_authenticate_user(mocker: MockerFixture) -> None:
    """Tests the `authenticate_user` function.

    Tests that the `authenticate_user` function correctly authenticates
    a user with the correct username and password, and returns the user object.
    Also tests that the function returns `False` when provided with an incorrect
    password.

    Args:
        mocker (MockerFixture): The mocker fixture used to mock functions.
    """

    # Mock the `get_user_by_username` function
    user = mock_get_user_by_username(mocker, simulate_match=True)

    assert authenticate_user("username", "password") == user
    assert not authenticate_user("username", "wrong_password")


def test_create_access_token() -> None:
    """Tests the `create_access_token` function.

    Tests that the `create_access_token` function correctly creates a JSON web
    token with the provided data and returns it as a string. Also tests that the
    function returns a string when provided with an expiration delta.
    """

    token = create_access_token(data={"sub": "username"})
    token_with_expiration = create_access_token(
        data={"sub": "username"}, expires_delta=timedelta(minutes=5)
    )
    assert isinstance(token, str)
    assert isinstance(token_with_expiration, str)


@pytest.mark.anyio
async def test_get_current_user(mocker: MockerFixture) -> None:
    """Tests the `get_current_user` function.

    Tests that the `get_current_user` function correctly retrieves a user
    object given a valid token. Also tests that the function raises an
    `HTTPException` when given an invalid token, an empty token, or when the
    user is not found in the database.
    """
    user = mock_get_user_by_username(mocker, simulate_match=True)
    token_valid = create_access_token(data={"sub": "username"})
    user_retrieved = await get_current_user(token_valid)
    assert user == user_retrieved
    with pytest.raises(HTTPException):
        await get_current_user("")
    with pytest.raises(HTTPException):
        token_invalid = create_access_token(data={})
        await get_current_user(token_invalid)
    with pytest.raises(HTTPException):
        mock_get_user_by_username(mocker, simulate_match=False)
        await get_current_user(token_valid)


@pytest.mark.anyio
async def test_get_current_active_user() -> None:
    """Tests the `get_current_active_user` function.

    Tests that the `get_current_active_user` function correctly returns
    the provided user object if the user is active, and raises an
    `HTTPException` if the user is inactive.
    """
    user = User(disabled=True)
    with pytest.raises(HTTPException):
        await get_current_active_user(user)
    user.disabled = False
    assert await get_current_active_user(user) == user


def test_get_password_hash() -> None:
    """Tests the `get_password_hash` function.

    Tests that the `get_password_hash` function correctly returns a hashed
    version of the provided password as a string, and that the hashed password
    can be verified using the `verify_password` function.
    """
    password = get_password_hash("password")
    assert isinstance(password, str)
    assert verify_password("password", password)


def test_verify_password() -> None:
    """Tests the `verify_password` function.

    Tests that the `verify_password` function correctly checks if the
    provided plain password matches the hashed password. Checks that if the
    hashed password is a mere string, a `ValueError` is raised.
    """
    password = get_password_hash("password")
    with pytest.raises(ValueError):
        verify_password("password", "password")
    assert verify_password("password", password)
    assert not verify_password("password_invalid", password)
