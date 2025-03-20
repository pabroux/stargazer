"""Models for the Auth app.

This module contains the models used by the Auth app.
"""

from pydantic import BaseModel
from sqlmodel import Field, SQLModel


class Token(BaseModel):
    """Token model for the Auth app.

    Represents the JSON web token returned on successful login.
    """

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Token data model for the Auth app.

    Represents the data embedded in the JSON web token returned on successful login.
    """

    username: str


class User(SQLModel, table=True):
    """User model in the database (ORM).

    Represents a user entry in the database and is used for authentication.
    """

    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    email: str = Field(unique=True, index=True)
    disabled: bool = False
    hashed_password: str
