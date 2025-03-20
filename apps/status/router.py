"""Router for Status app.

This module provides a FastAPI router for status-related endpoints.
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health_check() -> dict[str, str]:
    """Gets the health status of the FastAPI app.

    Returns a response with a single key "status" and value "healthy".
    It is used to check the health of the FastAPI app.

    Returns:
        Dict[str, str]: A dict with a single key "status" and value "healthy".
    """
    return {"status": "healthy"}
