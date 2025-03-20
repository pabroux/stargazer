"""
Settings for the app.

This module contains settings used by the app.

Attributes:
    ACCESS_TOKEN_EXPIRE_MINUTES (float): The number of minutes the access token to the app remains
        valid (defaults to 30).
    DATABASE_URL (str): The URL of the database used by the app.
    GITHUB_TOKEN (str): The GitHub API token.
    GITHUB_MAX_PAGE_REPO (int): The maximum number of pages to fetch for the requested repository
        (defaults to 1).
    GITHUB_MAX_PAGE_STARGAZER (int): The maximum number of pages to fetch for a stargazer of the
        requested repository (defaults to 1).
    JWT_ALGORITHM (str): The algorithm used to sign the JWT tokens. Possible values: "HS256"
        (default), "HS384" and "HS512".
    JWT_SECRET_KEY (str): The secret key used by the app for signing JWT.
"""

from os import getenv

# Authentification-related/security settings
ACCESS_TOKEN_EXPIRE_MINUTES = max(1, float(getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")))
JWT_ALGORITHM = (
    jwt_algo
    if ((jwt_algo := getenv("JWT_ALGORITHM")) in ["HS384", "HS512"])
    else "HS256"
)
JWT_SECRET_KEY = getenv("JWT_SECRET_KEY")

# Database settings
# Here we use a simple database (SQLite) for development environment.
# In production, we should use a better database (e.g. PostgreSQL).
DATABASE_URL = getenv("DATABASE_URL", "sqlite:///database/user.db")

# GitHub-API-related settings
GITHUB_TOKEN = getenv("GITHUB_TOKEN")
GITHUB_MAX_PAGE_REPO = max(1, int(getenv("GITHUB_MAX_PAGE_REPO", "1")))
GITHUB_MAX_PAGE_STARGAZER = max(1, int(getenv("GITHUB_MAX_PAGE_STARGAZERS", "1")))
