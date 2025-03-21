"""Tests for the router of the GitHub app.

This module contains tests for GitHub-related endpoints.
"""

from fastapi import status
from fastapi.testclient import TestClient

from apps.github.tests.utils import client_get_without_oauth
from apps.shared.utils import get_formatted_content
from main import app

client = TestClient(app)


def test_get_starneighbours() -> None:
    """Tests the /repos/<user>/<repo>/starneighbours endpoint.

    Tests the response is a 200 OK with a JSON body containing
    [{"repo": "pabroux/unvX", "stargazers": ["Sulfyderz", "pabroux"]}].
    """
    response = client_get_without_oauth(client, "/repos/pabroux/unvx/starneighbours")

    assert response.status_code == status.HTTP_200_OK
    assert {
        "repo": "pabroux/unvX",
        "stargazers": ["Sulfyderz", "pabroux"],
    } in response.json()


def test_get_starneighbours_invalid_request() -> None:
    """Tests the /repos/<user>/<repo>/starneighbours endpoint with an invalid request.

    Tests the response is a 502 Bad Gateway with a JSON body containing at least
    {"message": "Bad Gateway for GitHub API", "status": 502, "detail": {"github_api_message": ...}}.
    """
    response = client_get_without_oauth(
        client, "/repos/pabroux/unvx-undefined/starneighbours"
    )
    response_json = response.json()
    print(response_json)
    assert response.status_code == status.HTTP_502_BAD_GATEWAY
    assert "detail" in response_json and "github_api_message" in response_json["detail"]
    del response_json["detail"]
    assert response_json == get_formatted_content(
        "Bad Gateway for GitHub API", status.HTTP_502_BAD_GATEWAY
    )


def test_get_starneighbours_invalid_token() -> None:
    """Tests the /repos/<user>/<repo>/starneighbours endpoint with an invalid token.

    Tests the response is a 401 Unauthorized with a JSON body containing at least
    {"message": "Could not validate credentials", "status": 401}.
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
