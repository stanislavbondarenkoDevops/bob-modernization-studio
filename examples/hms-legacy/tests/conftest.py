"""Characterization-test fixtures for the legacy HMS (S0 baseline).

The legacy module creates the Flask app at import time and reads DATABASE_URL,
so the environment is set before the import.
"""
from __future__ import annotations

import os
import sys
from collections.abc import Iterator
from pathlib import Path

import pytest
from flask import Flask
from flask.testing import FlaskClient

PROJECT_DIR = Path(__file__).resolve().parents[1] / "PROJECT"


@pytest.fixture(scope="session")
def legacy_app(tmp_path_factory: pytest.TempPathFactory) -> Iterator[Flask]:
    db_file = tmp_path_factory.mktemp("db") / "hms.db"
    os.environ["DATABASE_URL"] = f"sqlite:///{db_file}"
    sys.path.insert(0, str(PROJECT_DIR))
    import main  # noqa: E402  (legacy module, import has side effects)

    # Legacy code leaves db.engine.execute() cursors open (passed straight to templates),
    # which deadlocks SQLite across pooled connections. A single shared connection mimics
    # the MySQL behaviour the app was written against. Engine is created lazily, so this
    # must be set before the first DB access.
    from sqlalchemy.pool import StaticPool

    main.app.config.update(
        TESTING=True,
        SQLALCHEMY_ENGINE_OPTIONS={"poolclass": StaticPool, "connect_args": {"check_same_thread": False}},
    )
    with main.app.app_context():
        main.db.create_all()
    yield main.app


@pytest.fixture()
def client(legacy_app: Flask) -> FlaskClient:
    return legacy_app.test_client()


@pytest.fixture()
def patient_client(client: FlaskClient) -> FlaskClient:
    """A client logged in as a Patient-type user."""
    client.post(
        "/signup",
        data={"username": "pat", "usertype": "Patient", "email": "pat@example.com", "password": "pw"},
    )
    client.post("/login", data={"email": "pat@example.com", "password": "pw"})
    return client


@pytest.fixture()
def doctor_client(client: FlaskClient) -> FlaskClient:
    """A client logged in as a Doctor-type user."""
    client.post(
        "/signup",
        data={"username": "doc", "usertype": "Doctor", "email": "doc@example.com", "password": "pw"},
    )
    client.post("/login", data={"email": "doc@example.com", "password": "pw"})
    return client
