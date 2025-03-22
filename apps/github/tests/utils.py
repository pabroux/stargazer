"""Test utilities for the GitHub app.

This module provides test utility functions for the GitHub app.
"""

import json
from collections.abc import Callable
from typing import Any
from unittest.mock import AsyncMock

from fastapi import status
from fastapi.testclient import TestClient
from httpx._models import Response
from pytest_mock import MockerFixture

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


def mock_async_client_get(
    mocker: MockerFixture,
    simulate_success: bool = True,
    content: list[Any] | None = None,
) -> Response:
    """Mocks the `get` method of the `httpx.AsyncClient` object.

    Mocks the `get` method of the `httpx.AsyncClient` object in the
    `apps.auth.utils` context. This mock is used in tests to avoid
    having to make real HTTP requests to the GitHub API.

    Args:
        mocker (MockerFixture): The pytest-mock fixture to use for mocking.
        simulate_success (bool, optional): Whether to simulate a successful
        response (defaults to True).
        content (list[Any], optional): The content of the response.

    Returns:
        Response: The mocked response object.
    """
    status_code = status.HTTP_200_OK if simulate_success else status.HTTP_404_NOT_FOUND
    content_json = json.dumps(content if content else ["test"]).encode("utf-8")
    resp = Response(status_code=status_code, content=content_json)
    mocker.patch("apps.github.utils.AsyncClient.get", AsyncMock(return_value=resp))
    return resp


def mock_get_starneighbours_fetch_stargazers(
    mocker: MockerFixture, content: list[Any] | None = None
) -> None:
    """Mocks the `fetch_stargazers` function used in `get_starneighbours`.

    Mocks the `fetch_stargazers` function used in `get_starneighbours` in the
    `apps.auth.utils` context. This mock is used in tests to avoid
    making real HTTP requests to the GitHub API.

    Args:
        mocker (MockerFixture): The pytest-mock fixture to use for mocking.
        content (list[Any], optional): The content of the response.
    """
    mocker.patch(
        "apps.github.router.fetch_stargazers",
        AsyncMock(return_value=((content if content else [], False))),
    )


def mock_get_starneighbours_fetch_starred_repos(
    mocker: MockerFixture, content: list[Any] | None = None
) -> None:
    """Mocks the `fetch_starred_repos` function used in `get_starneighbours`.

    Mocks the `fetch_starred_repos` function used in `get_starneighbours` in the
    `apps.auth.utils` context. This mock is used in tests to avoid
    making real HTTP requests to the GitHub API.

    Args:
        mocker (MockerFixture): The pytest-mock fixture to use for mocking.
        content (list[Any], optional): The content of the response.
    """
    mocker.patch(
        "apps.github.router.fetch_starred_repos",
        AsyncMock(return_value=((content if content else [], False))),
    )


async def override_get_current_active_user() -> User:
    """Overrides the `get_current_active_user` dependency.

    Instead of retrieving the current user from the database, this function
    returns a `User` object with default values. This is used to disable
    authentication for certain tests.

    Returns:
        User: A `User` object with default values.
    """
    return User()
