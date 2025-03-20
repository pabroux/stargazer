"""Router for the Auth app.

This module provides a FastAPI router for all Auth-related endpoints.
"""

from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestFormStrict

import settings

from .models import Token
from .utils import authenticate_user, create_access_token

router = APIRouter()


@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestFormStrict, Depends()],
) -> Token:
    """Gets an access token for a user.

    Authenticates a user and returns an access token, valid for a limited period.
    The limited period is defined by the `ACCESS_TOKEN_EXPIRE_MINUTES`
    environment variable.

    Args:
        form_data (OAuth2PasswordRequestFormStrict): The form data containing
        the username and password provided by the user.

    Returns:
        Token: A token containing the access token and token type.

    Raises:
        HTTPException: If the credentials are incorrect, a 401 Unauthorized
        exception is raised.
    """
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
