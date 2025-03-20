"""Utilities for the app.

This module contains helper functions that can be used by any app.
"""

from typing import Any, Dict, Optional, Sequence, Union

from fastapi.encoders import jsonable_encoder


def get_formatted_content(
    message: str,
    status: int,
    detail: Optional[Union[Sequence[Any], Dict[str, Any]]] = None,
) -> Any:
    """Formats a response content.

    Formats a response content with a message, documentation URL path,
    status, and optional details.

    Args:
        message (str): The message to be included in the response.
        status (int): The HTTP status code associated with the response.
        detail (Optional[Sequence[Any]]): Extra details for the response.

    Returns:
        Any: A JSON-encoded response dictionary containing the message,
        documentation URL path, status, and optional details.
    """
    response: Dict[str, Union[int, str, Sequence[Any], Dict[str, Any]]] = {
        "message": message,
        "documentation_url_path": "/docs",
        "status": status,
    }
    if detail is not None:
        response["detail"] = detail
    return jsonable_encoder(response)
