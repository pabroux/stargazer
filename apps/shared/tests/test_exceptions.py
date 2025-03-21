"""Tests for the exceptions of the app.

This module contains tests for exceptions of the app.
"""

import pytest
from fastapi import status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.testclient import TestClient
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.requests import Request

from apps.shared.exceptions import http_exception_handler, validation_exception_handler
from main import app

client = TestClient(app)


@pytest.mark.anyio
async def test_http_exception_handler() -> None:
    """Tests the `http_exception_handler` function.

    Testst that the response object is an instance of `JSONResponse`.
    """
    exc = StarletteHTTPException(status.HTTP_200_OK)
    response = await http_exception_handler(Request({"type": "http"}), exc)
    assert isinstance(response, JSONResponse)


@pytest.mark.anyio
async def test_validation_exception_handler() -> None:
    """Tests the `validation_exception_handlerr` function.

    Testst that the response object is an instance of `JSONResponse`.
    """
    exc = RequestValidationError(errors="errors")
    response = await validation_exception_handler(Request({"type": "http"}), exc)
    assert isinstance(response, JSONResponse)
