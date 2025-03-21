"""Utilities for the GitHub app.

This module provides utility functions for making requests with GitHub API.
"""

from fastapi import status
from httpx import AsyncClient

from apps.github.exceptions import GitHubException
from stargazer import settings


def get_github_headers() -> dict[str, str]:
    """Gets the headers to be sent with each GitHub API request.

    Returns a dictionary of headers to be sent with each GitHub API request. If a
    `GITHUB_TOKEN` environment variable is set, it will be included in the headers as
    a Bearer token.

    Returns:
        dict[str, str]: A dictionary of headers to be sent with each GitHub API request.
    """
    headers = {
        "Accept": "application/json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if settings.GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {settings.GITHUB_TOKEN}"
    return headers


async def fetch_stargazers(
    client: AsyncClient, user: str, repo: str, page: int
) -> tuple[list[str], bool]:
    """Fetches the stargazers for a given GitHub repository.

    Retrieves a list of stargazers for a given GitHub repository at a specific page
    through the GitHub API.

    Args:
        client (AsyncClient): The HTTPX client to use for the request.
        user (str): The user who owns the repository.
        repo (str): The name of the repository.
        page (int): The page number to fetch.

    Returns:
        A tuple containing:
            1. A list of strings, where each string is the name of a stargazer.
            2. A boolean indicating whether there is a next page of results.

    Raises:
        GitHubException: If the request to the GitHub API fails, a GitHubException is raised.
    """
    url = f"https://api.github.com/repos/{user}/{repo}/stargazers?per_page=100&page={page}"
    headers = get_github_headers()
    resp = await client.get(url, headers=headers)
    if resp.status_code != status.HTTP_200_OK:
        raise GitHubException(detail=resp.json())
    return [resp_user["login"] for resp_user in resp.json()], "next" in resp.links


async def fetch_starred_repos(
    client: AsyncClient, stargazer: str, page: int
) -> tuple[list[str], bool]:
    """Fetches the repositories starred by a given GitHub user.

    Retrieves a list of repositories starred by a given GitHub user at a specific page
    through the GitHub API.

    Args:
        client (AsyncClient): The HTTPX client to use for the request.
        stargazer (str): The GitHub user whose starred repositories are to be fetched.
        page (int): The page number to fetch.

    Returns:
        A tuple containing:
            1. A list of strings, where each string is the name of a repository starred
            by the given user, in the format "user/repo".
            2. A boolean indicating whether there is a next page of results.

    Raises:
        GitHubException: If the request to the GitHub API fails, a GitHubException is raised.
    """
    url = f"https://api.github.com/users/{stargazer}/starred?per_page=100&page={page}"
    headers = get_github_headers()
    resp = await client.get(url, headers=headers)
    if resp.status_code != status.HTTP_200_OK:
        raise GitHubException(detail=resp.json())
    return [
        f"{resp_repo['owner']['login']}/{resp_repo['name']}"
        for resp_repo in resp.json()
    ], "next" in resp.links
