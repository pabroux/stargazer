"""Utilities for the Auth app.

This module provides utility functions for authenticating users.
"""

from datetime import datetime, timedelta, timezone
from typing import Annotated, Literal

import bcrypt
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from sqlalchemy.exc import OperationalError
from sqlmodel import Session, create_engine, select

from apps.auth.models import TokenData, User
from stargazer import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

database_url = settings.DATABASE_URL
connect_args = {
    "check_same_thread": False  # Use the same database in different threads
}

engine = create_engine(database_url, connect_args=connect_args)


def authenticate_user(username: str, password: str) -> User | Literal[False]:
    """Authenticates a user.

    Authenticates a user using the provided username and password. If the
    username does not exist or the password is incorrect, the function returns
    False. Otherwise, the user object is returned.

    Args:
        username (str): The username of the user to authenticate.
        password (str): The password to verify against the user's hashed password.

    Returns:
        User | bool: The user object if the user is authenticated, False
        otherwise.
    """
    user = get_user_by_username(username)
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(
    data: dict[str, str | datetime], expires_delta: timedelta | None = None
) -> str:
    """Creates a JSON Web Token (JWT) for authentication.

    Generates an encoded JWT using the provided data (i.e., usersame) and optionally
    an expiration time. The expiration time defaults to 15 minutes if not specified.

    Args:
        data (dict[str, str | datetime]): The payload data to include
        in the token, typically containing user identification information.
        expires_delta (timedelta | None): A time delta indicating the
        duration for which the token is valid. If not provided, the token
        expires in 15 minutes.

    Returns:
        str: An encoded JWT string that can be used for user authentication.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    """Retrieves the current user based on the provided bearer token.

    Validates the provided JWT token, extracts the username from the payload, and
    retrieves the corresponding user object from the database.

    Args:
        token: The bearer token to validate and extract the user information from.

    Returns:
        User: The user object associated with the provided bearer token.

    Raises:
        HTTPException: If the token is invalid, the user is not found, or the credentials
        are incorrect, a 401 Unauthorized exception is raised.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError as exc:
        raise credentials_exception from exc
    user = get_user_by_username(token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    """Retrieves the current active user.

    Checks if the current user is active by verifying the `disabled` status.

    Args:
        current_user (User): The user object retrieved from the authentication
        dependency.

    Returns:
        User: The active user object.

    Raises:
        HTTPException: If the user is inactive, a 403 Forbidden exception
        is raised.
    """
    if current_user.disabled:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user",
        )
    return current_user


def get_password_hash(password: str) -> str:
    """Gets the hashed version of the provided password using bcrypt.

    Takes the provided password as a string, encodes it to bytes and
    compute the hashed password. The resulting hashed password is
    returned as a string, decoded from bytes.

    Args:
        password (str): The password to be hashed.

    Returns:
        str: The hashed password as a string.
    """
    pwd_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password_enc = bcrypt.hashpw(password=pwd_bytes, salt=salt)
    return hashed_password_enc.decode()


def get_user_by_username(username: str) -> User | None:
    """Retrieves a user by the username.

    Queries the database to retrieve a user object based on the
    provided username. If the user is not found, it returns None.

    Args:
        username (str): The username to search for.

    Returns:
        User | None: The user object if found, otherwise None.

    Raises:
        HTTPException: If unable to connect to the database, a 503 Service
        Unavailable exception is raised.
    """
    try:
        with Session(engine) as session:
            statement = select(User).where(User.username == username)
            user = session.exec(statement).first()
            return user
    except OperationalError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database not available",
        ) from exc


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain password against a hashed password.

    Checks if a plain password (i.e. given by the user) matches a hashed
    password (i.e. stored in the database).

    Args:
        plain_password (str): The plain password to be verified.
        hashed_password (str): The hashed password to compare against.

    Returns:
        bool: True if the plain password matches the hashed password, otherwise False.
    """
    plain_password_enc = plain_password.encode("utf-8")
    hashed_password_enc = hashed_password.encode("utf-8")
    return bcrypt.checkpw(plain_password_enc, hashed_password_enc)
