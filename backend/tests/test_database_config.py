import os
import pytest
from urllib.parse import urlparse

# Import the function from conftest
from .conftest import _get_test_database_url


def test_explicit_valid_test_database_url(monkeypatch):
    """Explicit TEST_DATABASE_URL pointing to fitnessrag_test should be accepted."""
    monkeypatch.setenv(
        "TEST_DATABASE_URL",
        "postgresql+asyncpg://postgres:postgres@localhost:5432/fitnessrag_test",
    )
    # Should not raise
    url = _get_test_database_url()
    assert (
        url == "postgresql+asyncpg://postgres:postgres@localhost:5432/fitnessrag_test"
    )
    parsed = urlparse(url.replace("+asyncpg", ""))
    assert parsed.path.lstrip("/") == "fitnessrag_test"


def test_default_docker_local_configuration(monkeypatch):
    """When TEST_DATABASE_URL is not set, values from .env.test should be used."""
    # Ensure no explicit override
    monkeypatch.delenv("TEST_DATABASE_URL", raising=False)
    # Set .env.test-like values
    monkeypatch.setenv("POSTGRES_USER", "postgres")
    monkeypatch.setenv("POSTGRES_PASSWORD", "postgres")
    monkeypatch.setenv("POSTGRES_SERVER", "db")
    monkeypatch.setenv("POSTGRES_PORT", "5432")
    monkeypatch.setenv("POSTGRES_DB", "fitnessrag_test")
    # Should not raise
    url = _get_test_database_url()
    assert url == "postgresql+asyncpg://postgres:postgres@db:5432/fitnessrag_test"
    parsed = urlparse(url.replace("+asyncpg", ""))
    assert parsed.path.lstrip("/") == "fitnessrag_test"


def test_explicit_invalid_database_name_is_rejected(monkeypatch):
    """Explicit TEST_DATABASE_URL pointing to fitnessrag should raise RuntimeError."""
    monkeypatch.setenv(
        "TEST_DATABASE_URL",
        "postgresql+asyncpg://postgres:postgres@db:5432/fitnessrag",
    )
    with pytest.raises(RuntimeError) as excinfo:
        _get_test_database_url()
    assert "Test database must be 'fitnessrag_test'" in str(excinfo.value)
    assert "fitnessrag" in str(excinfo.value)


def test_invalid_default_database_name_is_rejected(monkeypatch):
    """If .env.test specifies a wrong database name, it should be rejected."""
    monkeypatch.delenv("TEST_DATABASE_URL", raising=False)
    monkeypatch.setenv("POSTGRES_USER", "postgres")
    monkeypatch.setenv("POSTGRES_PASSWORD", "postgres")
    monkeypatch.setenv("POSTGRES_SERVER", "db")
    monkeypatch.setenv("POSTGRES_PORT", "5432")
    monkeypatch.setenv("POSTGRES_DB", "fitnessrag")  # wrong name
    with pytest.raises(RuntimeError) as excinfo:
        _get_test_database_url()
    assert "Test database must be 'fitnessrag_test'" in str(excinfo.value)
    assert "fitnessrag" in str(excinfo.value)
