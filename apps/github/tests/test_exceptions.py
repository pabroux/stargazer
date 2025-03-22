"""Tests for the exceptions of the GitHub app.

This module contains tests for exceptions of the GitHubapp.
"""

import pytest
from fastapi import status
from fastapi.responses import JSONResponse
from starlette.requests import Request

from apps.github.exceptions import GitHubException, github_exception_handler
from apps.shared.utils import get_formatted_content


def test_github_exception() -> None:
    """Tests the GitHubException class.

    Tests that the GitHubException class has `detail` attribute and
    is an instance of Exception.
    """
    github_exception = GitHubException(detail="detail")
    assert github_exception.detail == "detail"
    assert isinstance(github_exception, Exception)


@pytest.mark.anyio
async def test_github_exception_handler() -> None:
    """Tests the GitHubException handler.

    Tests that the response object is an instance of `JSONResponse`.
    """
    exc = GitHubException(detail="detail")
    content = get_formatted_content(
        "Bad Gateway for GitHub API",
        status.HTTP_502_BAD_GATEWAY,
        {"github_api_message": exc.detail},
    )
    response = await github_exception_handler(Request({"type": "http"}), exc)
    assert isinstance(response, JSONResponse)
    assert response.status_code == status.HTTP_502_BAD_GATEWAY
    assert response.body == response.render(content)
