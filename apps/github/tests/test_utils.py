"""Tests for the utilities of the GitHub app.

This module contains tests for utility functions dedicated to query GitHub API.
"""

import pytest
from httpx import AsyncClient
from pytest_mock import MockerFixture

from apps.github.exceptions import GitHubException
from apps.github.tests.utils import mock_async_client_get
from apps.github.utils import fetch_stargazers, fetch_starred_repos, get_github_headers
from stargazer import settings


def test_get_github_headers() -> None:
    """Tests the `get_github_headers` function.

    Tests that `get_github_headers` returns a dictionary with the expected
    keys and values.
    """

    headers = get_github_headers()
    assert "Accept" in headers and headers["Accept"] == "application/json"
    assert (
        "X-GitHub-Api-Version" in headers
        and headers["X-GitHub-Api-Version"] == "2022-11-28"
    )
    if settings.GITHUB_TOKEN:
        assert (
            "Authorization" in headers
            and headers["Authorization"] == f"Bearer {settings.GITHUB_TOKEN}"
        )


@pytest.mark.anyio
async def test_fetch_stargazers(mocker: MockerFixture) -> None:
    """Tests the `fetch_stargazers` function.

    Tests that a `GitHubException` is raised when the request to fetch
    stargazers fails. Checks that the function returns the expected
    output when the request is successful, correctly retrieving the
    list of stargazers and the presence of a next page.
    """

    mock_async_client_get(mocker, simulate_success=False)
    client = AsyncClient()
    with pytest.raises(GitHubException):
        await fetch_stargazers(client=client, user="user", repo="repo", page=1)
    resp = mock_async_client_get(
        mocker, simulate_success=True, content=[{"login": "user"}]
    )
    output_expected = [
        resp_user["login"] for resp_user in resp.json()
    ], "next" in resp.links
    assert output_expected == await fetch_stargazers(
        client=client, user="user", repo="repo", page=1
    )


@pytest.mark.anyio
async def test_fetch_starred_repos(mocker: MockerFixture) -> None:
    """Tests the `fetch_starred_repos` function.

    Tests that a `GitHubException` is raised when the request to fetch
    starred repositories fails. Checks that the function returns the expected
    output when the request is successful, correctly retrieving the list of
    starred repositories and the presence of a next page.
    """
    mock_async_client_get(mocker, simulate_success=False)
    client = AsyncClient()
    with pytest.raises(GitHubException):
        await fetch_starred_repos(client=client, stargazer="stargazer", page=1)
    resp = mock_async_client_get(
        mocker,
        simulate_success=True,
        content=[{"name": "repo", "owner": {"login": "user"}}],
    )
    output_expected = [
        resp_repo["owner"]["login"] + "/" + resp_repo["name"]
        for resp_repo in resp.json()
    ], "next" in resp.links
    assert output_expected == await fetch_starred_repos(
        client=client, stargazer="stargazer", page=1
    )
