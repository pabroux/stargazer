"""Tests for the router of the GitHub app.

This module contains tests for GitHub-related endpoints.
"""

import pytest
from fastapi import status
from fastapi.testclient import TestClient
from pytest_mock import MockerFixture

from apps.github.tests.utils import (
    client_get_without_oauth,
    mock_get_starneighbours_fetch_stargazers,
    mock_get_starneighbours_fetch_starred_repos,
)
from apps.shared.utils import get_formatted_content
from main import app

client = TestClient(app)


@pytest.mark.anyio
def test_get_starneighbours(mocker: MockerFixture) -> None:
    """Tests the /repos/<user>/<repo>/starneighbours endpoint.

    Tests the response is a 200 OK with a JSON body similar to
    `[{"repo": <str>, "stargazers": [ <str>, ...]}, ...]`.
    """

    mock_get_starneighbours_fetch_stargazers(mocker, content=["pabroux", "Sulfyderz"])
    mock_get_starneighbours_fetch_starred_repos(
        mocker, content=["pabroux/unvx", "pabroux/ai-forge"]
    )
    resp = client_get_without_oauth(client, "/repos/pabroux/unvx/starneighbours")
    output_expected = [
        {"repo": "pabroux/unvx", "stargazers": ["pabroux", "Sulfyderz"]},
        {"repo": "pabroux/ai-forge", "stargazers": ["pabroux", "Sulfyderz"]},
    ]
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json() == output_expected


def test_get_starneighbours_invalid_token() -> None:
    """Tests the /repos/<user>/<repo>/starneighbours endpoint with an invalid token.

    Tests the response is a 401 Unauthorized with a JSON body containing at least
    `{"message": "Could not validate credentials", "status": 401}`.
    """
    response = client.get(
        "/repos/pabroux/unvx/starneighbours",
        headers={
            "Accept": "application/json",
            "Authorization": "Bearer invalid_token",
        },
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == get_formatted_content(
        "Could not validate credentials", status.HTTP_401_UNAUTHORIZED
    )
