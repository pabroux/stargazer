"""Tests for the exceptions of the app.

This module contains tests for exceptions of the app.
"""

import pytest
from fastapi import status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.requests import Request

from apps.shared.exceptions import http_exception_handler, validation_exception_handler
from apps.shared.utils import get_formatted_content


@pytest.mark.anyio
async def test_http_exception_handler() -> None:
    """Tests the `http_exception_handler` function.

    Tests that the response object is an instance of `JSONResponse`.
    """
    exc = StarletteHTTPException(status_code=status.HTTP_200_OK, detail="detail")
    response = await http_exception_handler(Request({"type": "http"}), exc)
    assert isinstance(response, JSONResponse)
    assert response.status_code == status.HTTP_200_OK
    assert response.body == response.render(
        get_formatted_content(
            str(exc.detail),
            exc.status_code,
        ),
    )


@pytest.mark.anyio
async def test_validation_exception_handler() -> None:
    """Tests the `validation_exception_handlerr` function.

    Tests that the response object is an instance of `JSONResponse`, has
    a 422 Unprocessable Entity status code and the correct content.
    """
    exc = RequestValidationError(errors="errors")
    response = await validation_exception_handler(Request({"type": "http"}), exc)
    assert isinstance(response, JSONResponse)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.body == response.render(
        get_formatted_content(
            "Invalid input",
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            exc.errors(),
        ),
    )
