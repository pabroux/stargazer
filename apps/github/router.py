"""Router for the GitHub app.

This module provides a FastAPI router for GitHub-API-related endpoints.
"""

from collections import defaultdict
from typing import Annotated, Any

import httpx
from fastapi import APIRouter, Depends

import settings
from apps.auth.models import User
from apps.auth.utils import get_current_active_user

from .utils import fetch_stargazers, fetch_starred_repos

router = APIRouter()


@router.get("/repos/{user}/{repo}/starneighbours")
async def get_starneighbours(
    user: str,
    repo: str,
    _: Annotated[User, Depends(get_current_active_user)],
) -> list[dict[str, Any]]:
    """Gets star neighbours for a given GitHub repository.

    Retrieves a list of repositories that are starred by at least one stargazer of the
    requested repository, along with a list of stargazers of those repositories that also
    starred the requested repository.

    Args:
        user (str): The user who owns the repository.
        repo (str): The name of the repository.
        _ (User): The user making the request.

    Returns:
        A list of dictionaries, where each dictionary contains the name of a repository
        starred by at least one stargazer of the requested repository, along with a list of
        stargazers of that repository that also starred the requested repository. The returned
        list is sorted by the number of stargazers in descending order.
    """
    # Use Httpx to make asynchronous requests
    async with httpx.AsyncClient() as client:

        # Fecth stargazers
        stargazers = []
        page = 1
        while page <= settings.GITHUB_MAX_PAGE_REPO:
            stargazers_chunk, has_next = await fetch_stargazers(
                client, user, repo, page
            )
            stargazers.extend(stargazers_chunk)
            # Stop if no more pages to fetch
            if not has_next:
                break
            page += 1

        # Build neighbor relationships
        neighbors = defaultdict(list)
        for stargazer in stargazers:
            stargazer_stars = []
            page = 1
            while page <= settings.GITHUB_MAX_PAGE_STARGAZER:
                stars_chunk, has_next = await fetch_starred_repos(
                    client, stargazer, page
                )
                stargazer_stars.extend(stars_chunk)
                # Stop if no more pages to fetch
                if not has_next:
                    break
                page += 1

            for starred_repo in stargazer_stars:
                neighbors[starred_repo].append(stargazer)

    return sorted(
        [
            {"repo": repo_name, "stargazers": stargazers_list}
            for repo_name, stargazers_list in neighbors.items()
        ],
        key=lambda x: len(x["stargazers"]),
        reverse=True,
    )
