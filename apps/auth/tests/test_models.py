"""Tests for the Auth app models.

This module contains tests for the Auth-related models.
"""

from apps.auth.models import Token, TokenData, User


def test_token() -> None:
    """Tests the Token model.

    Tests that the Token model is correctly initialized.
    """
    token = Token(access_token="token", token_type="bearer")
    assert token.access_token == "token"
    assert token.token_type == "bearer"


def test_token_data() -> None:
    """Tests the TokenData model.

    Tests that the TokenData model is correctly initialized.
    """
    token_data = TokenData(username="username")
    assert token_data.username == "username"


def test_user() -> None:
    """Tests the User model.

    Tests that the User model is correctly initialized.
    """
    user = User(
        id=1,
        username="username",
        email="email",
        disabled=False,
        hashed_password="hashed_password",
    )
    assert user.id == 1
    assert user.username == "username"
    assert user.email == "email"
    assert not user.disabled
    assert user.hashed_password == "hashed_password"
    user.id = None
    assert user.id is None
