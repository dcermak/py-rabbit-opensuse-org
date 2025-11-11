"""Pytest configuration for py_rodo tests."""

import os

import pytest


@pytest.fixture(scope="session", autouse=True)
def configure_backend():
    """Configure backend before running tests."""
    import py_rodo.config

    backend = os.environ.get("PY_RODO_TEST_BACKEND", "pydantic")
    py_rodo.config.set_backend(backend)
