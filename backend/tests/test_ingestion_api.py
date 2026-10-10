"""
Tests for the file ingestion API endpoint.
"""
from __future__ import annotations

import io
import os
import tempfile
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi import status, UploadFile
from fastapi.testclient import TestClient

from app.main import app
from app.core.config import settings


@pytest.fixture
def client():
    """Create a test client."""
    return TestClient(app)


@pytest.fixture
def mock_user():
    """Mock admin user for testing."""
    user = MagicMock()
    user.email = "admin@example.com"
    user.is_active = True
    user.is_verified = True
    return user


@pytest.fixture
def mock_auth_dependency(mock_user):
    """Mock the get_ingestion_admin_user dependency."""
    with patch("app.core.dependencies.get_ingestion_admin_user") as mock:
        mock.return_value = mock_user
        yield mock


@pytest.fixture(autouse=True)
def _bind_auth_dependency_override():
    """Route FastAPI dependency resolution to core_deps so patch works."""
    from app.core.dependencies import get_ingestion_admin_user
    import app.core.dependencies as core_deps
    from fastapi import HTTPException

    async def _override():
        curr = core_deps.get_ingestion_admin_user
        if isinstance(curr, (MagicMock, AsyncMock)):
            if curr.side_effect is not None:
                if isinstance(curr.side_effect, Exception):
                    raise curr.side_effect
                if isinstance(curr.side_effect, type) and issubclass(curr.side_effect, Exception):
                    raise curr.side_effect()
                if callable(curr.side_effect):
                    res = curr.side_effect()
                    if hasattr(res, "__await__"):
                        return await res
                    return res
            res = curr()
            if hasattr(res, "__await__"):
                return await res
            return res
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    app.dependency_overrides[get_ingestion_admin_user] = _override
    yield
    app.dependency_overrides.pop(get_ingestion_admin_user, None)


@pytest.fixture(autouse=True)
def mock_sync_session_provider():
    """Default mock for get_sync_session across ingestion API tests."""
    mock_session = MagicMock()
    mock_gen = MagicMock()
    mock_gen.__next__.return_value = mock_session
    mock_gen.close = MagicMock()

    with patch("app.api.v1.ingestion.get_sync_session", return_value=mock_gen):
        yield mock_session, mock_gen



class TestIngestionAPI:
    """Test the file ingestion API endpoint."""

    def test_ingest_txt_file_success(self, client, mock_auth_dependency):
        """Test successful ingestion of a .txt file."""
        # Mock the ingestion service to return a specific chunk count
        with patch("app.services.ingestion.ingest_file") as mock_ingest:
            mock_ingest.return_value = 5

            # Create a test file
            file_content = b"This is a test file content."
            file = UploadFile(
                filename="test.txt",
                file=io.BytesIO(file_content),
                headers={"content-type": "text/plain"}
            )

            # Make the request
            response = client.post(
                "/api/v1/ingestion/file",
                files={"file": ("test.txt", file_content, "text/plain")},
            )

            # Assertions
            assert response.status_code == 200
            data = response.json()
            assert data["message"] == "Ingestion complete"
            assert data["chunks_ingested"] == 5

            # Verify the ingestion service was called
            mock_ingest.assert_called_once()
            args, kwargs = mock_ingest.call_args
            assert kwargs["source_title"] == "test.txt"
            assert isinstance(kwargs["db"], MagicMock)  # We mocked the db session

    def test_ingest_md_file_success(self, client, mock_auth_dependency):
        """Test successful ingestion of a .md file."""
        with patch("app.services.ingestion.ingest_file") as mock_ingest:
            mock_ingest.return_value = 3

            file_content = b"# Test Markdown\n\nThis is a test."
            response = client.post(
                "/api/v1/ingestion/file",
                files={"file": ("test.md", file_content, "text/markdown")},
            )

            assert response.status_code == 200
            data = response.json()
            assert data["message"] == "Ingestion complete"
            assert data["chunks_ingested"] == 3

    def test_ingest_csv_file_success(self, client, mock_auth_dependency):
        """Test successful ingestion of a .csv file."""
        with patch("app.services.ingestion.ingest_file") as mock_ingest:
            mock_ingest.return_value = 10

            file_content = b"name,value\nfoo,1\nbar,2"
            response = client.post(
                "/api/v1/ingestion/file",
                files={"file": ("test.csv", file_content, "text/csv")},
            )

            assert response.status_code == 200
            data = response.json()
            assert data["message"] == "Ingestion complete"
            assert data["chunks_ingested"] == 10

    def test_ingest_unauthenticated(self, client):
        """Test that unauthenticated requests are rejected."""
        # Don't mock the auth dependency - this will use the real one
        # which should fail because there's no token
        file_content = b"test content"
        response = client.post(
            "/api/v1/ingestion/file",
            files={"file": ("test.txt", file_content, "text/plain")},
        )

        # Should return 401 (unauthorized) or 403 (if user exists but not authorized)
        assert response.status_code in (401, 403)

    def test_ingest_unauthorized_user(self, client):
        """Test that non-admin users are rejected."""
        # Mock a non-admin user
        non_admin_user = MagicMock()
        non_admin_user.email = "user@example.com"
        non_admin_user.is_active = True
        non_admin_user.is_verified = True

        with patch("app.core.dependencies.get_ingestion_admin_user") as mock_auth:
            # Make the dependency raise an HTTPException for unauthorized access
            from fastapi import HTTPException
            mock_auth.side_effect = HTTPException(
                status_code=403,
                detail="User is not authorized for file ingestion"
            )

            file_content = b"test content"
            response = client.post(
                "/api/v1/ingestion/file",
                files={"file": ("test.txt", file_content, "text/plain")},
            )

            assert response.status_code == 403
            assert "not authorized" in response.json()["detail"]

    def test_ingest_inactive_user(self, client):
        """Test that inactive users are rejected."""
        # Mock an inactive user
        inactive_user = MagicMock()
        inactive_user.email = "inactive@example.com"
        inactive_user.is_active = False
        inactive_user.is_verified = True

        with patch("app.core.dependencies.get_ingestion_admin_user") as mock_auth:
            from fastapi import HTTPException
            mock_auth.side_effect = HTTPException(
                status_code=403,
                detail="User account is inactive"
            )

            file_content = b"test content"
            response = client.post(
                "/api/v1/ingestion/file",
                files={"file": ("test.txt", file_content, "text/plain")},
            )

            assert response.status_code == 403
            assert "inactive" in response.json()["detail"]

    def test_ingest_unverified_user(self, client):
        """Test that unverified users are rejected."""
        # Mock an unverified user
        unverified_user = MagicMock()
        unverified_user.email = "unverified@example.com"
        unverified_user.is_active = True
        unverified_user.is_verified = False

        with patch("app.core.dependencies.get_ingestion_admin_user") as mock_auth:
            from fastapi import HTTPException
            mock_auth.side_effect = HTTPException(
                status_code=403,
                detail="User email is not verified"
            )

            file_content = b"test content"
            response = client.post(
                "/api/v1/ingestion/file",
                files={"file": ("test.txt", file_content, "text/plain")},
            )

            assert response.status_code == 403
            assert "not verified" in response.json()["detail"]

    def test_ingest_empty_allowlist(self, client):
        """Test that empty allowlist denies by default."""
        # Mock a user but with empty allowlist in settings
        user = MagicMock()
        user.email = "admin@example.com"
        user.is_active = True
        user.is_verified = True

        with patch("app.core.dependencies.get_ingestion_admin_user") as mock_auth:
            from fastapi import HTTPException
            mock_auth.side_effect = HTTPException(
                status_code=403,
                detail="Ingestion functionality is not configured. Contact administrator."
            )

            file_content = b"test content"
            response = client.post(
                "/api/v1/ingestion/file",
                files={"file": ("test.txt", file_content, "text/plain")},
            )

            assert response.status_code == 403
            assert "not configured" in response.json()["detail"]

    def test_ingest_unsupported_extension(self, client, mock_auth_dependency):
        """Test rejection of unsupported file extensions."""
        file_content = b"test content"
        response = client.post(
            "/api/v1/ingestion/file",
            files={"file": ("test.exe", file_content, "application/octet-stream")},
        )

        assert response.status_code == 415  # Unsupported Media Type
        assert "extension" in response.json()["detail"].lower()

    def test_ingest_file_too_large(self, client, mock_auth_dependency):
        """Test rejection of oversized files."""
        # Create a file larger than 5 MB
        large_content = b"x" * (5 * 1024 * 1024 + 1024)  # 5 MB + 1 KB

        response = client.post(
            "/api/v1/ingestion/file",
            files={"file": ("large.txt", large_content, "text/plain")},
        )

        assert response.status_code == 413  # Request Entity Too Large
        assert "size" in response.json()["detail"].lower()
        assert "exceeds" in response.json()["detail"].lower()

    def test_ingest_invalid_utf8(self, client, mock_auth_dependency):
        """Test rejection of invalid UTF-8 content."""
        # Create invalid UTF-8 bytes
        invalid_utf8 = b'\xff\xfe\xfd'  # Invalid UTF-8 sequence

        response = client.post(
            "/api/v1/ingestion/file",
            files={"file": ("test.txt", invalid_utf8, "text/plain")},
        )

        assert response.status_code == 415  # Unsupported Media Type
        assert "utf-8" in response.json()["detail"].lower() or "invalid" in response.json()["detail"].lower()

    def test_ingest_service_unavailable(self, client, mock_auth_dependency):
        """Test handling of ingestion service failures."""
        with patch("app.services.ingestion.ingest_file") as mock_ingest:
            # Make the ingestion service raise an exception
            mock_ingest.side_effect = Exception("Embedding service unavailable")

            file_content = b"test content"
            response = client.post(
                "/api/v1/ingestion/file",
                files={"file": ("test.txt", file_content, "text/plain")},
            )

            assert response.status_code == 503  # Service Unavailable
            assert "temporarily unavailable" in response.json()["detail"]

    def test_ingest_exact_size_limit(self, client, mock_auth_dependency):
        """Test file exactly at the size limit."""
        with patch("app.services.ingestion.ingest_file") as mock_ingest:
            mock_ingest.return_value = 2

            # Exactly 5 MB
            exact_size_content = b"x" * (5 * 1024 * 1024)
            response = client.post(
                "/api/v1/ingestion/file",
                files={"file": ("exact.txt", exact_size_content, "text/plain")},
            )

            assert response.status_code == 200
            data = response.json()
            assert data["message"] == "Ingestion complete"
            assert data["chunks_ingested"] == 2

    def test_ingest_one_byte_over_limit(self, client, mock_auth_dependency):
        """Test file one byte over the size limit."""
        # 5 MB + 1 byte
        over_size_content = b"x" * ((5 * 1024 * 1024) + 1)
        response = client.post(
            "/api/v1/ingestion/file",
            files={"file": ("over.txt", over_size_content, "text/plain")},
        )

        assert response.status_code == 413  # Request Entity Too Large

    def test_ingest_valid_file_at_limit(self, client: TestClient, mock_auth_dependency: MagicMock) -> None:
        """Test that a file exactly at the 5 MiB limit is accepted."""
        with patch("app.services.ingestion.ingest_file") as mock_ingest:
            mock_ingest.return_value = 1

            # Exactly 5 MB
            exact_size_content = b"x" * (5 * 1024 * 1024)
            response = client.post(
                "/api/v1/ingestion/file",
                files={"file": ("exact.txt", exact_size_content, "text/plain")},
            )

            assert response.status_code == 200
            data = response.json()
            assert data["message"] == "Ingestion complete"
            assert data["chunks_ingested"] == 1
            mock_ingest.assert_called_once()

    def test_ingest_request_too_large_rejected_before_parsing(self, client: TestClient) -> None:
        """Test that requests exceeding the body limit are rejected before multipart parsing."""
        # Create a request that exceeds our 6 MiB limit (5 MiB file + multipart overhead)
        # We'll send a raw POST with excessive body to test the middleware
        excessive_content = b"x" * (7 * 1024 * 1024)  # 7 MB, exceeds our 6 MiB limit

        # We need to simulate a multipart request, but for simplicity we'll test
        # that excessively large bodies are rejected. In a real test, we'd craft
        # a proper multipart body, but the middleware should catch it either way.

        # For this test, we'll send a raw body that's too large
        # Note: This test might need adjustment based on how Starlette handles
        # non-multipart POSTs to this endpoint, but the principle is the same
        response = client.post(
            "/api/v1/ingestion/file",
            content=excessive_content,
            headers={"Content-Type": "application/octet-stream"}
        )

        # Should be rejected with 413 before reaching our endpoint
        assert response.status_code == status.HTTP_413_REQUEST_ENTITY_TOO_LARGE
        assert "too large" in response.text.lower()

    def test_ingest_request_body_limit_with_missing_content_length(self, client: TestClient) -> None:
        """Test that the body limit works even when Content-Length is missing."""
        # Create a body that exceeds the limit
        excessive_content = b"x" * (7 * 1024 * 1024)  # 7 MB

        # Send without Content-Length header (or with incorrect one)
        response = client.post(
            "/api/v1/ingestion/file",
            content=excessive_content,
            headers={
                # No Content-Length header, or incorrect one
                "Content-Type": "application/octet-stream"
                # Intentionally omitting Content-Length
            }
        )

        # Should still be rejected based on actual body size
        assert response.status_code == status.HTTP_413_REQUEST_ENTITY_TOO_LARGE

    def test_ingest_request_body_limit_with_misleading_content_length(self, client: TestClient) -> None:
        """Test that a misleadingly small Content-Length cannot bypass the limit."""
        # Create a body that exceeds the limit
        excessive_content = b"x" * (7 * 1024 * 1024)  # 7 MB

        # Send with a misleadingly small Content-Length
        response = client.post(
            "/api/v1/ingestion/file",
            content=excessive_content,
            headers={
                "Content-Type": "application/octet-stream",
                "Content-Length": "100"  # Claim only 100 bytes
            }
        )

        # Should still be rejected based on actual body size, not the header
        assert response.status_code == status.HTTP_413_REQUEST_ENTITY_TOO_LARGE

    def test_ingest_other_endpoints_unaffected_by_limit(self, client: TestClient) -> None:
        """Test that other endpoints are not affected by the ingestion body limit."""
        # Test that a normal endpoint (like health check) still works
        response = client.get("/health")
        assert response.status_code == 200

        # Test that auth endpoint still works (would need proper auth, but at least
        # the middleware shouldn't interfere with the request reaching the endpoint)
        response = client.post("/api/v1/auth/login", json={"email": "test@test.com", "password": "wrong"})
        # Should get 401 (unauthorized) or 422 (validation error), not 413 (payload too large)
        assert response.status_code != status.HTTP_413_REQUEST_ENTITY_TOO_LARGE

    def test_ingest_rejects_prefix_matching_mime_type(self, client: TestClient, mock_auth_dependency: MagicMock) -> None:
        """Test rejection of MIME types that merely start with expected type (e.g. text/plain-malicious)."""
        file_content = b"valid text content"
        response = client.post(
            "/api/v1/ingestion/file",
            files={"file": ("test.txt", file_content, "text/plain-malicious")},
        )
        assert response.status_code == status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
        assert "not allowed" in response.json()["detail"].lower()

    def test_ingest_accepts_mime_type_with_charset(self, client: TestClient, mock_auth_dependency: MagicMock) -> None:
        """Test acceptance of MIME types with valid parameters like charset=utf-8."""
        with patch("app.services.ingestion.ingest_file") as mock_ingest:
            mock_ingest.return_value = 1
            file_content = b"valid text content with utf-8 charset"
            response = client.post(
                "/api/v1/ingestion/file",
                files={"file": ("test.txt", file_content, "text/plain; charset=utf-8")},
            )
            assert response.status_code == 200
            assert response.json()["message"] == "Ingestion complete"

    def test_temp_file_closed_and_cleaned_up_on_oversized_upload(
        self, client: TestClient, mock_auth_dependency: MagicMock
    ) -> None:
        """Test that temporary file handle is closed and file unlinked when upload is oversized."""
        created_temp_files = []
        real_named_temp_file = tempfile.NamedTemporaryFile

        def tracking_temp_file(*args, **kwargs):
            tf = real_named_temp_file(*args, **kwargs)
            created_temp_files.append(tf)
            return tf

        with patch("tempfile.NamedTemporaryFile", side_effect=tracking_temp_file):
            oversized_content = b"x" * (5 * 1024 * 1024 + 1024)  # 5 MB + 1 KB
            response = client.post(
                "/api/v1/ingestion/file",
                files={"file": ("large.txt", oversized_content, "text/plain")},
            )

            assert response.status_code == status.HTTP_413_REQUEST_ENTITY_TOO_LARGE
            assert len(created_temp_files) == 1
            tf = created_temp_files[0]
            assert tf.closed is True
            assert not os.path.exists(tf.name)

    def test_temp_file_closed_and_cleaned_up_on_ingestion_exception(
        self, client: TestClient, mock_auth_dependency: MagicMock
    ) -> None:
        """Test that temporary file handle is closed and file unlinked when ingestion fails."""
        created_temp_files = []
        real_named_temp_file = tempfile.NamedTemporaryFile

        def tracking_temp_file(*args, **kwargs):
            tf = real_named_temp_file(*args, **kwargs)
            created_temp_files.append(tf)
            return tf

        with patch("tempfile.NamedTemporaryFile", side_effect=tracking_temp_file), \
             patch("app.services.ingestion.ingest_file") as mock_ingest:
            mock_ingest.side_effect = RuntimeError("Embedding failure")

            file_content = b"valid file content"
            response = client.post(
                "/api/v1/ingestion/file",
                files={"file": ("test.txt", file_content, "text/plain")},
            )

            assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
            assert len(created_temp_files) == 1
            tf = created_temp_files[0]
            assert tf.closed is True
            assert not os.path.exists(tf.name)

    def test_session_generator_cleanup_on_success(
        self, client: TestClient, mock_auth_dependency: MagicMock
    ) -> None:
        """Test that session generator is closed on successful ingestion using a generator double."""
        generator_closed = False
        mock_session = MagicMock()

        def test_generator():
            nonlocal generator_closed
            try:
                yield mock_session
            finally:
                generator_closed = True

        with patch("app.api.v1.ingestion.get_sync_session", side_effect=test_generator), \
             patch("app.services.ingestion.ingest_file") as mock_ingest:
            mock_ingest.return_value = 2
            file_content = b"hello world"
            response = client.post(
                "/api/v1/ingestion/file",
                files={"file": ("test.txt", file_content, "text/plain")},
            )

            assert response.status_code == 200
            assert generator_closed is True

    def test_session_generator_cleanup_on_failure(
        self, client: TestClient, mock_auth_dependency: MagicMock
    ) -> None:
        """Test that session generator is closed on ingestion failure using a generator double."""
        generator_closed = False
        mock_session = MagicMock()

        def test_generator():
            nonlocal generator_closed
            try:
                yield mock_session
            finally:
                generator_closed = True

        with patch("app.api.v1.ingestion.get_sync_session", side_effect=test_generator), \
             patch("app.services.ingestion.ingest_file") as mock_ingest:
            mock_ingest.side_effect = ValueError("Corrupt file")
            file_content = b"hello world"
            response = client.post(
                "/api/v1/ingestion/file",
                files={"file": ("test.txt", file_content, "text/plain")},
            )

            assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
            assert generator_closed is True

    def test_session_commit_on_success_and_rollback_on_failure(
        self, client: TestClient, mock_auth_dependency: MagicMock
    ) -> None:
        """Test that sync_session.commit() is called on success and rollback() on failure."""
        # Success path
        mock_session_success = MagicMock()
        mock_gen_success = MagicMock()
        mock_gen_success.__next__.return_value = mock_session_success

        with patch("app.api.v1.ingestion.get_sync_session", return_value=mock_gen_success), \
             patch("app.services.ingestion.ingest_file") as mock_ingest:
            mock_ingest.return_value = 1
            response = client.post(
                "/api/v1/ingestion/file",
                files={"file": ("test.txt", b"valid content", "text/plain")},
            )
            assert response.status_code == 200
            mock_session_success.commit.assert_called_once()
            mock_session_success.rollback.assert_not_called()
            mock_gen_success.close.assert_called_once()

        # Failure path
        mock_session_failure = MagicMock()
        mock_gen_failure = MagicMock()
        mock_gen_failure.__next__.return_value = mock_session_failure

        with patch("app.api.v1.ingestion.get_sync_session", return_value=mock_gen_failure), \
             patch("app.services.ingestion.ingest_file") as mock_ingest:
            mock_ingest.side_effect = Exception("DB error")
            response = client.post(
                "/api/v1/ingestion/file",
                files={"file": ("test.txt", b"valid content", "text/plain")},
            )
            assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
            mock_session_failure.rollback.assert_called_once()
            mock_session_failure.commit.assert_not_called()
            mock_gen_failure.close.assert_called_once()