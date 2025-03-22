"""Test utilities for the Auth app.

This module provides test utility functions for the Auth app.
"""

from pytest_mock import MockerFixture

from apps.auth.models import User
from apps.auth.utils import get_password_hash


def mock_get_user_by_username(
    mocker: MockerFixture, simulate_match: bool = True
) -> User | None:
    """Mocks the `get_user_by_username` function.

    Mocks the `get_user_by_username` function in the `apps.auth.utils` context.
    This mock is used in tests to avoid having to create a user in the database.

    Args:
        mocker (MockerFixture): The mocker fixture used to mock the function.
        similuate_match (bool): Whether to simulate a match or not (default: True).
        Simulate a match returns a user object, otherwise returns None.

    Returns:
        User | None: The mocked user object if a match is simulated, otherwise None.
    """
    user = (
        User(
            username="pabroux",
            email="pabroux@stargazer.com",
            hashed_password=f"{get_password_hash("password")}",
            disabled=False,
        )
        if simulate_match
        else None
    )
    mocker.patch("apps.auth.utils.get_user_by_username", return_value=user)
    return user
