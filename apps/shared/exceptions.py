"""Exceptions for the app.

This module contains exceptions for the app.
"""

from typing import Any

from fastapi import FastAPI, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.requests import Request

from apps.shared.utils import get_formatted_content


async def http_exception_handler(_: Request, exc: Any) -> JSONResponse:
    """Handles HTTPExceptions and returns a formatted response.

    For any HTTPException, the app returns a JSON response with a formatted content.

    Args:
        _ (Request): The request that triggered the exception.
        exc (Any): The exception instance.

    Returns:
        JSONResponse: A JSON response with a formatted content.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content=get_formatted_content(
            str(exc.detail),
            exc.status_code,
        ),
    )


async def validation_exception_handler(_: Request, exc: Any) -> JSONResponse:
    """Handles ValidationExceptions and returns a formatted response.

    For any ValidationException, the app returns a JSON response with a formatted
    content and a code 422.

    Args:
        _ (Request): The request that triggered the exception.
        exc (Any): The exception instance.

    Returns:
        JSONResponse: A JSON response with a formatted content.
    """
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=get_formatted_content(
            "Invalid input",
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            exc.errors(),
        ),
    )


def include_app(app: FastAPI) -> None:
    """Includes the exception handlers related to the app in the given FastAPI app.

    Associates the exception handlers 'http_exception_handler' and
    'validation_exception_handler' with the FastAPI app.

    Args:
        app (FastAPI): The app to include the exception handlers in.
    """
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
