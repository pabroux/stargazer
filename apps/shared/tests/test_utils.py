"""Tests for the utilities of the app.

This module contains tests for utility functions that can be used by any app.
"""

from fastapi import status

from apps.shared.utils import get_formatted_content
from stargazer import settings


def test_get_formatted_content() -> None:
    """Tests the `get_formatted_content` function.

    Ensures that the function correctly formats the response content
    with given message, status, and detail. Also checks for the presence
    of the documentation URL path based on the `DOCS_ACTIVATE` environment
    variable.
    """

    message = "Test message"
    detail = ["Test detail"]
    formatted_content = get_formatted_content(
        message=message, status=status.HTTP_200_OK, detail=detail
    )
    assert formatted_content["message"] == message
    assert formatted_content["status"] == status.HTTP_200_OK
    assert formatted_content["detail"] == detail
    if settings.DOCS_ACTIVATE:
        assert "documentation_url_path" in formatted_content
        assert formatted_content["documentation_url_path"] == "/docs"
    else:
        assert "documentation_url_path" not in formatted_content
