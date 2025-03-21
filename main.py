"""FastAPI entrypoint.

This module contains the entrypoint of the FastAPI app.
"""

from fastapi import FastAPI

import apps.github.exceptions as exceptions_github
import apps.shared.exceptions as exceptions_shared
from apps.auth.router import router as router_auth
from apps.auth.utils import check_database_exist
from apps.github.router import router as router_github
from apps.status.router import router as router_status
from stargazer import settings

# Check if the database specified in settings exists
check_database_exist()

# Create FastAPI app
app = FastAPI(
    docs_url="/docs" if settings.DOC_ACTIVATE else None,
    redoc_url="/redoc" if settings.DOC_ACTIVATE else None,
)

# Setup routers to the app
app.include_router(router_auth)
app.include_router(router_github)
app.include_router(router_status)

# Setup exceptions to the app
exceptions_github.include_app(app)
exceptions_shared.include_app(app)
