"""Utility script to create a simple database with fake users.

This script creates a simple database with fake users to test the app. It is not
intended for production use.
"""

import sys
from importlib.util import module_from_spec, spec_from_file_location
from os import chdir, makedirs, path
from types import ModuleType

from sqlmodel import Session, SQLModel, create_engine


def import_module(module_name: str, file_path: str) -> ModuleType:
    """Dynamically imports a Python module from a file path.

    Dynamically imports a Python module from a given file path. If the module
    cannot be imported, the script exits with a code 1.

    Args:
        module_name (str): The name of the module to import.
        file_path (str): The path to the Python file containing the module.

    Returns:
        The imported module.
    """
    spec = spec_from_file_location(module_name, file_path)
    if spec is None or spec.loader is None:
        print(f"Unable to import the '{module_name}' module.")
        sys.exit(1)
    module = module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


parent_dir = path.abspath(path.join(path.dirname(__file__), ".."))

# Import dynamically 'User' model (ORM) and 'get_password_hash' function
_ = import_module("stargazer", path.join(parent_dir, "stargazer/__init__.py"))
_ = import_module("apps", path.join(parent_dir, "apps/__init__.py"))
models = import_module("apps.auth.models", path.join(parent_dir, "apps/auth/models.py"))
utils = import_module("apps.auth.utils", path.join(parent_dir, "apps/auth/utils.py"))
User = models.User
get_password_hash = utils.get_password_hash

# Change the working directory to the script's parent directory
# Thus the script can be executed from anywhere
chdir(parent_dir)

# Create the 'database' folder if not present
makedirs("database", exist_ok=True)

# Check if 'database/user.db' already exists
DATABASE_FILE = "database/user.db"
if path.exists(DATABASE_FILE):
    print("Database already exists.")
    sys.exit(1)

# Create the 'database/user.db' database
# Here we create a simple database (SQLite) for the development environment
# In production, we should use a better database (e.g. PostgreSQL)
engine = create_engine(f"sqlite:///{DATABASE_FILE}")
SQLModel.metadata.create_all(engine)

# Fake user list
fake_users = [
    {
        "username": "jd",
        "email": "jd@stargazer.com",
        "disabled": False,
    },
    {
        "username": "sileht",
        "email": "sileht@stargazer.com",
        "disabled": False,
    },
    {
        "username": "aurele",
        "email": "aurele@stargazer.com",
        "disabled": True,
    },
]

# Insert fake users into the 'database/users.db' database
with Session(engine) as session:

    for i, fake_user in enumerate(fake_users):
        print(f"Creating fake user {i + 1}/{len(fake_users)}...")
        password = input(f"Enter the password for '{fake_user['username']}': ")
        fake_user["hashed_password"] = get_password_hash(password)
        session.add(User(**fake_user))
    session.commit()

print("Database and fake users created successfully.")
