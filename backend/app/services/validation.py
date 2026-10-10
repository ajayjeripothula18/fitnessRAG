"""
File validation service for ingestion workflow.
Handles file type, size, and content validation.
"""

import os
from typing import Tuple
from app.core.config import settings


def validate_file_extension(filename: str) -> Tuple[bool, str]:
    """
    Validate file extension against allowed list.

    Args:
        filename: Original filename from client

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not filename:
        return False, "No filename provided"

    # Extract extension and normalize to lowercase
    _, ext = os.path.splitext(filename)
    ext = ext.lower()

    if ext not in settings.INGESTION_ALLOWED_EXTENSIONS:
        allowed_list = ", ".join(sorted(settings.INGESTION_ALLOWED_EXTENSIONS))
        return False, f"File extension '{ext}' not allowed. Allowed: {allowed_list}"

    return True, ""


def validate_file_size(file_size: int) -> Tuple[bool, str]:
    """
    Validate file size against maximum limit.

    Args:
        file_size: Size of file in bytes

    Returns:
        Tuple of (is_valid, error_message)
    """
    if file_size > settings.INGESTION_MAX_FILE_SIZE:
        max_mb = settings.INGESTION_MAX_FILE_SIZE // (1024 * 1024)
        actual_mb = file_size // (1024 * 1024)
        return False, f"File size {actual_mb} MiB exceeds maximum {max_mb} MiB"

    return True, ""


def validate_file_content(file_path: str) -> Tuple[bool, str]:
    """
    Validate that file content is valid UTF-8 text without loading entire file into memory.
    Uses incremental validation to handle characters split across chunk boundaries.

    Args:
        file_path: Path to temporary file

    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        with open(file_path, "rb") as f:
            chunk_size = 8192  # 8KB chunks
            # UTF-8 decoder state - we'll keep track of incomplete bytes
            # UTF-8 can have 1-4 byte characters
            leftover_bytes = b""

            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break

                # Combine leftover bytes from previous chunk with current chunk
                data = leftover_bytes + chunk

                try:
                    # Try to decode the combined data
                    data.decode("utf-8", errors="strict")
                    # If successful, there are no leftover bytes
                    leftover_bytes = b""
                except UnicodeDecodeError as e:
                    # If we have a UnicodeDecodeError, check if it's due to incomplete character
                    if e.reason == "unexpected end of data":
                        # Keep the bytes that couldn't be decoded for the next chunk
                        leftover_bytes = data[e.start :]
                    else:
                        # Invalid UTF-8 sequence
                        return False, "File is not valid UTF-8 text"

            # After processing all chunks, there should be no leftover bytes
            if leftover_bytes:
                return False, "File is not valid UTF-8 text"

        return True, ""
    except Exception as e:
        return False, f"Error reading file: {str(e)}"
