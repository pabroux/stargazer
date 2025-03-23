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

Stargazer is developed in Python and uses the [FastAPI](https://fastapi.tiangolo.com/) framework. Underneath, it queries [GitHub API](https://docs.github.com/en/rest).

## Table of contents

- [Requirements](#requirements)
- [Usage](#usage)
- [Configuration](#configuration)
- [Structure](#structure)
- [Improvements](#improvements)

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
> This will create a database at `database/utils.db` with three fake users with the following usernames: `jd`, `sileht` and `aurele`. `aurele` is the only disabled user (i.e. he can't retrieve ressources even if he is authenticated). You will be prompted to set passwords for each user.

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
> The Nginx server is used to proxy the requests to the FastAPI container, the Stargazer app. It caches responses that was generated with the help of GitHub API.

> [!TIP]
> Don't want to use Docker?
>
> 1. Install dependencies: `pip install -r requirements/prod.txt`;
> 2. Run the app: `uvicorn main:app --host 127.0.0.1 --port 8000`.
>
> In the following, use port `8000` instead of `80`.

Request a bearer token at `/token` endpoint for a user with a username `<username>` and a password `<password>`:

```shell
curl -X 'POST' \
  'http://127.0.0.1:80/token' \
  -d 'grant_type=password&username=<username>&password=<password>'
```

Request the list of neighbour repositories of a GitHub repository at `/repos/<owner>/<repo>/starneighbours` endpoint by passing the bearer token in the `Authorization` header:

```shell
curl -X 'GET' \
  'http://127.0.0.1:80/repos/<user>/<repo>/starneighbours' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer <token>'
```

> [!TIP]
> Want to try on a repository with few stargazers? Test on `/repos/pabroux/unvX/starneighbours`. [unvX](https://github.com/pabroux/unvX) is a repository starred by [pabroux](http://github.com/pabroux) and [Sulfyderz](https://github.com/Sulfyderz).

## Configuration

You can configure the app by creating a `.env` file and setting the following environment variables:

| Variable                      | Description                                                                                               |
| ----------------------------- | --------------------------------------------------------------------------------------------------------- |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | The number of minutes the access token to the app remains valid (defaults to 30)                          |
| `DATABASE_URL`                | The URL of the database used by the app                                                                   |
| `DOCS_ACTIVATE`               | Whether to make the documentation available (defaults to True)                                            |
| `GITHUB_TOKEN`                | A GitHub API access token                                                                                 |
| `GITHUB_MAX_PAGE_REPO`        | The maximum number of pages to fetch for the requested repository (defaults to 1)                         |
| `GITHUB_MAX_PAGE_STARGAZER`   | The maximum number of pages to fetch for a stargazer of the requested repository (defaults to 1)          |
| `JWT_ALGORITHM`               | The algorithm used to sign JSON Web Tokens (JWT). Possible values: "HS256" (default), "HS384" and "HS512" |
| `JWT_SECRET_KEY`              | The secret key used to sign JSON Web Tokens (JWT)                                                         |

> [!NOTE]
> If you run the app without Docker, create these environment variables in your terminal instead (e.g. `export JWT_ALGORITHM="HS256"`).

## Structure

The app is structured as follows:

```text
.
├── .github                               # Directory containing GitHub Actions workflows
│   └── workflows
│       ├── auto-assigner.yml                 # Issue auto-assigner
│       ├── ci-tester.yml                     # CI tester
│       ├── code-quality-checker.yml          # Code quality checker
│       └── code-security-checker.yml         # Code security checker
├── apps                                  # Directory containing the apps used by the Stargazer app
│   ├── __init__.py
│   ├── auth                                  # Directory containing the auth app
│   │   ├── tests                                 # Directory containing the tests for the auth app
│   │   ├── __init__.py
│   │   ├── models.py                             # Models for the auth app
│   │   ├── router.py                             # Router for the auth app
│   │   └── utils.py                              # Utils for the auth app
│   ├── github                                # Directory containing the github app
│   │   ├── tests                                 # Directory containing the tests for the github app
│   │   ├── __init__.py
│   │   ├── exceptions.py                         # Exceptions for the github app
│   │   ├── router.py                             # Router for the github app
│   │   └── utils.py                              # Utils for the github app
│   ├── shared                                # Directory containing the shared app
│   │   ├── tests                                 # Directory containing the tests for the status app
│   │   ├── __init__.py
│   │   ├── exceptions.py                         # Exceptions for the shared app
│   │   └── utils.py                              # Utils for the github app
│   └─ status                                 # Directory containing the status app
│       ├── tests                                 # Directory containing the tests for the status app
│       ├── __init__.py
│       └── routers.py                            # Router for the status app
├── config                                # Directory containing the configuration files non specific to the Stargazer app
│   └── nginx.conf                            # Nginx configuration
├── stargazer                             # Directory containing high-level settings for the Stargazer app
│   ├── __init__.py
│   └── settings.py                           # Settings for the Stargazer app
├── utilities                             # Directory containing utility scripts
│   └── create_database.py                    # Script to create a fake database
├── requirements                          # Directory containing the requirements files
│   ├── dev.txt                               # Development requirements
│   └── prod.txt                              # Production requirements
├── CHANGELOG.md                          # CHANGELOG
├── docker-compose.yml                    # Docker Compose configuration
├── Dockerfile                            # Dockerfile
├── LICENSE                               # MIT license
├── main.py                               # Entry point of the Stargazer app
└── README.md                             # README
```

> [!NOTE]
> The structure is much inspired by [Django](https://www.djangoproject.com)'s one.

## Improvements

- [ ] CRUD endpoints for managing users;
- [ ] Protected Git branch dedicated to production;
- [ ] CI/CD pipeline;
- [ ] Real database (e.g. PostgreSQL);
- [ ] Cached database (e.g. Redis);
- [ ] Schema examples of each endpoint for the generated [OpenAPI](https://www.openapis.org) documentation;
- [ ] Containers on separate machines, load balancing and auto scaling (Kubernetes);
- [ ] Better database handling when not existing (currently, SQLModel with SQLite raises an error if the database does not exist, but still creates an empty database file). SQLAlchemy-Utils offers a solution but that package has some known vulnerabilities.
