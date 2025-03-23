# 💫 Stargazer

<p align="left">
  <a href="https://github.com/pabroux/stargazer/blob/master/LICENSE">
    <picture>
      <img src="https://img.shields.io/badge/License-MIT-green" alt="License Badge">
    </picture>
  </a>
  <a href="https://github.com/pabroux/stargazer/actions/workflows/ci-tester.yml">
    <picture>
      <img src="https://github.com/pabroux/stargazer/actions/workflows/ci-tester.yml/badge.svg" alt="CI Tester Badge">
    </picture>
  </a>
  <a href="https://github.com/pabroux/stargazer/actions/workflows/code-quality-checker.yml">
    <picture>
      <img src="https://github.com/pabroux/stargazer/actions/workflows/code-quality-checker.yml/badge.svg" alt="Code Quality Checker Badge">
    </picture>
  </a>
  <a href="https://github.com/pabroux/stargazer/actions/workflows/code-security-checker.yml">
    <picture>
      <img src="https://github.com/pabroux/stargazer/actions/workflows/code-security-checker.yml/badge.svg" alt="Code Security Checker Badge">
    </picture>
  </a>
</p>

## About

Stargazer is a REST API that leverages GitHub's _stargazers_ feature to find related repositories. A "neighbour" of a repository is defined as another repository that has been starred by at least one of the same users (stargazers).
Stargazer offers an API endpoint that, when given a GitHub repository (owner and name), returns a JSON list of neighbour repositories, along with the stargazers they have in common. It supports OAuth2 authentication.

Stargazer is developed in Python and uses the [FastAPI](https://fastapi.tiangolo.com/) framework. Underneath, it queries GitHub API.

## Table of contents

- [Requirements](#requirements)
- [Usage](#usage)
- [Configuration](#configuration)
- [Structure](#structure)
- [Resources](#resources)

## Requirements

To run the app, you will need:

- [Python 3.12 or higher](https://www.python.org/downloads/);
- [Docker](https://docs.docker.com/get-docker/);
- [Docker Compose](https://docs.docker.com/compose/install/).

## Usage

Create a fake database by calling the `utilities/create_database.py` script:

```shell
python utilities/create_database.py
```

> [!NOTE]
> This will create a database at `database/utils.db` with three fake users: `jd`, `sileht` and `aurele`.
> `aurele` is the only disabled user (i.e. he can't retrieve ressources even if he is authenticated).
> You will be prompted to set passwords for each user.

Run the app with Docker Compose:

```shell
docker compose up
```

> [!NOTE]
> This will run two containers:
>
> - A FastAPI container, listening on port 8000;
> - A Nginx container, listening on port 80.
>
> The Nginx server is used to proxy the requests to the FastAPI container. It caches responses that was generated with the help of GitHub API.

> [!TIP]
> Don't want to use Docker?
>
> 1. Install dependencies: `pip install -r requirements/prod.txt`;
> 2. Run the app: `uvicorn main:app --host 127.0.0.1 --port 8000`.
>
> In the following, use port `8000` instead of `80`.

Request a bearer token at `/token` endpoint for user `<user>` with password `<password>`:

```shell
curl -X 'POST' \
  'http://127.0.0.1:80/token' \
  -d 'grant_type=password&username=<user>&password=<password>'
```

Request the list of neighbour repositories of a GitHub repository at `/repos/<user>/<repo>/starneighbours` endpoint by passing the bearer token in the `Authorization` header:

```shell
curl -X 'GET' \
  'http://127.0.0.1:80/repos/<user>/<repo>/starneighbours' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer <token>'
```

> [!TIP]
> Don't want to ?

## Configuration

You can configure the app in the `.env` file.

## Improvements

- [ ] OpenAI docs
- Add CRUD endpoints for the users.
- Handle database better (SQLModel still creates the dabase even it it fails to connect).
  [] Create another protected Git branch for production.
