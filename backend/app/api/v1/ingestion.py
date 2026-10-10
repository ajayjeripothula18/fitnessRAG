"""
File ingestion API endpoints.
"""
from __future__ import annotations

import logging
import os
import tempfile
from typing import Any

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status

from app.core.config import settings
from app.core.dependencies import get_ingestion_admin_user
from app.db.session import get_sync_session
from app.models.user import User
from app.services import ingestion as ingestion_service
from app.services.validation import (
    validate_file_content,
    validate_file_extension,
    validate_file_size,
)

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post(
    "/file",
    status_code=status.HTTP_200_OK,
    response_model=dict[str, Any],
)
async def upload_file(
    file: UploadFile = File(...),
    current_user: User = Depends(get_ingestion_admin_user),
):
    """
    Upload and ingest a file.

    Accepts only .txt, .md, and .csv files up to 5 MiB in size.
    Validates file extension, size, MIME type, and UTF-8 encoding.
    Uses the existing ingestion service to process the file.
    """
    # Validate file extension
    is_valid_ext, ext_error = validate_file_extension(file.filename or "")
    if not is_valid_ext:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=ext_error,
        )

    # Validate MIME type as a secondary check
    raw_content_type = file.content_type or ""
    filename = file.filename or ""
    _, ext = os.path.splitext(filename)
    ext = ext.lower()

    # Define expected MIME types for each extension
    expected_mime_types = {
        ".txt": "text/plain",
        ".md": "text/markdown",
        ".csv": "text/csv",
    }

    if ext in expected_mime_types:
        expected_type = expected_mime_types[ext]
        # Extract the media type before any ';' parameters, trim whitespace, and normalize case
        media_type = raw_content_type.split(";")[0].strip().lower()
        if media_type != expected_type:
            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                detail=f"MIME type '{raw_content_type}' not allowed for extension '{ext}'. Expected: {expected_type}",
            )

    # Create a temporary file to store the uploaded content
    # Using delete=False so we can manually control deletion
    temp_file = None
    temp_file_path: str | None = None
    try:
        # Create temporary file
        temp_file = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=ext,
        )
        temp_file_path = temp_file.name

        # Read and write the file in chunks to enforce size limit
        max_size = settings.INGESTION_MAX_FILE_SIZE
        total_size = 0
        chunk_size = 8192  # 8KB chunks

        while True:
            chunk = await file.read(chunk_size)
            if not chunk:
                break

            total_size += len(chunk)
            if total_size > max_size:
                raise HTTPException(
                    status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                    detail=f"File size {total_size} bytes exceeds maximum {max_size} bytes",
                )

            temp_file.write(chunk)

        temp_file.close()  # Close so we can reopen for validation
        file_size = total_size

        # Validate file size (redundant check for safety)
        is_valid_size, size_error = validate_file_size(file_size)
        if not is_valid_size:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=size_error,
            )

        # Validate file content (UTF-8)
        is_valid_content, content_error = validate_file_content(temp_file_path)
        if not is_valid_content:
            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                detail=content_error,
            )

        # Ingest using the synchronous database session
        session_gen = get_sync_session()
        try:
            sync_session = next(session_gen)
            try:
                # Ingest the file using the existing service
                chunks_ingested = ingestion_service.ingest_file(
                    file_path=temp_file_path,
                    db=sync_session,
                    source_title=file.filename or "Uploaded File",
                )

                # Commit the transaction
                sync_session.commit()

                logger.info(
                    f"Ingested file '{file.filename}' by user '{current_user.email}'. "
                    f"Chunks created: {chunks_ingested}"
                )

                return {
                    "message": "Ingestion complete",
                    "chunks_ingested": chunks_ingested,
                }

            except Exception as e:
                sync_session.rollback()
                logger.error(f"Failed to ingest file '{file.filename}': {str(e)}")
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail="Ingestion service temporarily unavailable",
                ) from e
        finally:
            session_gen.close()

    finally:
        # Guarantee temporary-file handle closure and unlink
        if temp_file is not None:
            try:
                if not temp_file.closed:
                    temp_file.close()
            except Exception as e:
                logger.warning(f"Failed to close temporary file handle: {str(e)}")

        if temp_file_path is not None and os.path.exists(temp_file_path):
            try:
                os.unlink(temp_file_path)
            except OSError as e:
                logger.warning(f"Failed to delete temporary file {temp_file_path}: {str(e)}")