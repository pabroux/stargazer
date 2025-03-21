"""Exceptions for the GitHub app.

This module contains exceptions for the GitHub app.
"""

from typing import Any

from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from starlette.requests import Request

from apps.shared.utils import get_formatted_content


class GitHubException(Exception):
    """Custom exception for GitHub API errors.

    The exception to raise when the GitHub API returns an error.
    """

    def __init__(self, detail: str):
        self.detail = detail


async def github_exception_handler(_: Request, exc: Any) -> JSONResponse:
    """Handles GitHubException and returns a formatted response.

    For any GitHubException, the app returns a JSON response with a formatted
    content and a 502 Bad Gateway code.

    Args:
        _ (Request): The request that triggered the exception.
        exc (Any): The exception instance.

    Returns:
        JSONResponse: A JSON response with a formatted content.
    """
    return JSONResponse(
        status_code=status.HTTP_502_BAD_GATEWAY,
        content=get_formatted_content(
            "Bad Gateway for GitHub API",
            status.HTTP_502_BAD_GATEWAY,
            {"github_api_message": exc.detail},
        ),
    )


def include_app(app: FastAPI) -> None:
    """Includes the exception handlers related to the github app in the given FastAPI app.

    Associates the exception handler `github_exception_handler` with the FastAPI app.

    Args:
        app (FastAPI): The app to include the exception handlers in.
    """
    app.add_exception_handler(GitHubException, github_exception_handler)
