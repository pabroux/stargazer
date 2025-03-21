"""Utilities for the app.

This module contains utility functions that can be used by any app.
"""

from collections.abc import Sequence
from typing import Any

from fastapi.encoders import jsonable_encoder

from stargazer import settings


def get_formatted_content(
    message: str,
    status: int,
    detail: Sequence[Any] | dict[str, Any] | None = None,
) -> Any:
    """Formats a response content.

    Formats a response content with a message, documentation URL path,
    status, and optional details.

    Args:
        message (str): The message to be included in the response.
        status (int): The HTTP status code associated with the response.
        detail (Sequence[Any] | dict[str, Any] | None): Extra details for the response.

    Returns:
        Any: A JSON-encoded response dictionary containing the message,
        documentation URL path, status, and optional details.
    """
    response: dict[str, int | str | Sequence[Any] | dict[str, Any]] = {
        "message": message,
        "status": status,
    }
    if settings.DOC_ACTIVATE:
        response["documentation_url_path"] = "/docs"
    if detail is not None:
        response["detail"] = detail
    return jsonable_encoder(response)
