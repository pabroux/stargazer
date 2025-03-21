"""Test utilities for the GitHub app.

This module provides test utility functions for the GitHub app.
"""

from collections.abc import Callable
from typing import Any

from fastapi.testclient import TestClient
from httpx._models import Response

from apps.auth.models import User
from apps.auth.utils import get_current_active_user
from main import app


def disable_oauth(
    func: Callable[..., Any],
) -> Callable[..., Any]:
    """Decorator to disable OAuth authentication.

    This decorator can be used to disable OAuth authentication for a test.

    Args:
        func (Callable): The test function to wrap.

    Returns:
        Callable: The wrapped test function.
    """

    def wrapper(*args: Any, **kwargs: Any) -> Any:
        app.dependency_overrides[get_current_active_user] = (
            override_get_current_active_user
        )
        response = func(*args, **kwargs)
        app.dependency_overrides.clear()
        return response

    return wrapper


@disable_oauth
def client_get_without_oauth(client: TestClient, url: str) -> Response:
    """Queries a GET request to the given URL while disabling OAuth authentication.

    This function is useful for testing endpoints that are protected by OAuth
    authentication.

    Args:
        url (str): The URL to GET.

    Returns:
        Response: The response from the server.
    """
    return client.get(url)


async def override_get_current_active_user() -> User:
    """Overrides the `get_current_active_user` dependency.

    Instead of retrieving the current user from the database, this function
    returns a `User` object with default values. This is used to disable
    authentication for certain tests.

    Returns:
        User: A `User` object with default values.
    """
    return User()
