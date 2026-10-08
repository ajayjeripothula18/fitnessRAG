"""
Unit tests for content_tsv trigger functionality in DocumentChunk model.
"""
from __future__ import annotations

import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.document_chunk import DocumentChunk


@pytest.mark.asyncio
async def test_content_tsv_populated_on_insert(db_session: AsyncSession):
    """Test that content_tsv is populated when inserting a DocumentChunk."""
    # Create a test DocumentChunk
    chunk = DocumentChunk(
        source_url="https://example.com/test",
        source_title="Test Source",
        content="This is a test content for full-text search",
        embedding=[0.1] * 768,  # Dummy embedding
    )

    db_session.add(chunk)
    await db_session.flush()

    # Verify content_tsv was populated
    assert chunk.content_tsv is not None
    # Check that it contains expected lexemes (stop words removed, stemmed)
    # The exact format depends on the to_tsvector('english', ...) output
    # but we can verify it's not empty and contains relevant terms
    content_tsv_str = str(chunk.content_tsv)
    assert len(content_tsv_str) > 0
    # Should contain stemmed forms of content words
    assert "'test'" in content_tsv_str or "test" in content_tsv_str
    assert "'content'" in content_tsv_str or "content" in content_tsv_str


@pytest.mark.asyncio
async def test_content_tsv_updated_on_content_change(db_session: AsyncSession):
    """Test that content_tsv is updated when content is modified."""
    # Create a test DocumentChunk
    chunk = DocumentChunk(
        source_url="https://example.com/test",
        source_title="Test Source",
        content="Original content",
        embedding=[0.1] * 768,  # Dummy embedding
    )

    db_session.add(chunk)
    await db_session.flush()

    original_content_tsv = chunk.content_tsv

    # Update the content
    chunk.content = "Updated content with different words"
    await db_session.flush()

    # Verify content_tsv was updated
    assert chunk.content_tsv is not None
    assert chunk.content_tsv != original_content_tsv

    # The new content_tsv should reflect the updated content
    content_tsv_str = str(chunk.content_tsv)
    assert len(content_tsv_str) > 0
    assert "'updat'" in content_tsv_str or "update" in content_tsv_str  # stemmed form
    assert "'different'" in content_tsv_str or "different" in content_tsv_str
    assert "'word'" in content_tsv_str or "word" in content_tsv_str


@pytest.mark.asyncio
async def test_content_tsv_unchanged_on_non_content_update(db_session: AsyncSession):
    """Test that content_tsv is not updated when non-content fields are modified."""
    # Create a test DocumentChunk
    chunk = DocumentChunk(
        source_url="https://example.com/test",
        source_title="Test Source",
        content="Test content",
        embedding=[0.1] * 768,  # Dummy embedding
    )

    db_session.add(chunk)
    await db_session.flush()

    original_content_tsv = chunk.content_tsv

    # Update a non-content field
    chunk.source_title = "Updated Source Title"
    await db_session.flush()

    # Verify content_tsv was NOT updated
    assert chunk.content_tsv == original_content_tsv


@pytest.mark.asyncio
async def test_content_tsv_matches_to_tsvector_function(db_session: AsyncSession):
    """Test that content_tsv matches the output of to_tsvector('english', content)."""
    test_content = "This is a test sentence with some words for full-text search"

    # Create a test DocumentChunk
    chunk = DocumentChunk(
        source_url="https://example.com/test",
        source_title="Test Source",
        content=test_content,
        embedding=[0.1] * 768,  # Dummy embedding
    )

    db_session.add(chunk)
    await db_session.flush()

    # Verify content_tsv matches to_tsvector output
    result = await db_session.execute(
        text("SELECT to_tsvector('english', :content)"), {"content": test_content}
    )
    expected_tsv = result.scalar()

    assert str(chunk.content_tsv) == str(expected_tsv)


@pytest.mark.asyncio
async def test_backfill_existing_null_content_tsv(db_session: AsyncSession):
    """Test that existing rows with NULL content_tsv get backfilled."""
    # First, disable the trigger to simulate inserting legacy data
    await db_session.execute(
        text(
            "ALTER TABLE document_chunks DISABLE TRIGGER document_chunks_content_tsv_trigger"
        )
    )

    try:
        # Insert a DocumentChunk with NULL content_tsv (simulating legacy data)
        await db_session.execute(
            text(
                """
                INSERT INTO document_chunks 
                (source_url, source_title, content, embedding, content_tsv)
                VALUES (:source_url, :source_title, :content, :embedding, NULL)
            """
            ),
            {
                "source_url": "https://example.com/test",
                "source_title": "Test Source",
                "content": "Test content for backfill",
                "embedding": [0.1] * 768,
            },
        )
        await db_session.flush()

        # Verify the row was inserted with NULL content_tsv
        result = await db_session.execute(
            text(
                """
                SELECT content_tsv FROM document_chunks 
                WHERE source_url = :source_url
            """
            ),
            {"source_url": "https://example.com/test"},
        )
        content_tsv_before = result.scalar()
        assert content_tsv_before is None, "Content_tsv should be NULL after insert"

        # Now apply the backfill (same operation as in migration)
        await db_session.execute(
            text(
                """
                UPDATE document_chunks
                SET content_tsv = to_tsvector('english', content)
                WHERE content_tsv IS NULL
            """
            )
        )
        await db_session.flush()

        # Verify the row now has content_tsv populated
        result = await db_session.execute(
            text(
                """
                SELECT content_tsv FROM document_chunks 
                WHERE source_url = :source_url
            """
            ),
            {"source_url": "https://example.com/test"},
        )
        content_tsv_after = result.scalar()

        assert content_tsv_after is not None
        assert str(content_tsv_after) != ""
        # Should contain relevant lexemes from the content
        content_tsv_str = str(content_tsv_after)
        assert "'test'" in content_tsv_str or "test" in content_tsv_str
        assert "'content'" in content_tsv_str or "content" in content_tsv_str
        assert "'backfill'" in content_tsv_str or "backfill" in content_tsv_str

        # Verify it matches the expected to_tsvector output
        expected_result = await db_session.execute(
            text("SELECT to_tsvector('english', :content)"),
            {"content": "Test content for backfill"},
        )
        expected_tsv = expected_result.scalar()
        assert str(content_tsv_after) == str(expected_tsv)
    finally:
        # Re-enable the trigger for other tests
        await db_session.execute(
            text(
                "ALTER TABLE document_chunks ENABLE TRIGGER document_chunks_content_tsv_trigger"
            )
        )


@pytest.mark.asyncio
async def test_content_tsv_gin_index_usable(db_session: AsyncSession):
    """Test that the GIN index on content_tsv can be used for queries."""
    # Insert test data
    chunks_data = [
        {
            "source_url": "https://example.com/fitness1",
            "source_title": "Fitness Source 1",
            "content": "How to build muscle strength",
            "embedding": [0.1] * 768,
        },
        {
            "source_url": "https://example.com/fitness2",
            "source_title": "Fitness Source 2",
            "content": "Cardio exercises for endurance",
            "embedding": [0.2] * 768,
        },
        {
            "source_url": "https://example.com/fitness3",
            "source_title": "Fitness Source 3",
            "content": "Nutrition tips for weight loss",
            "embedding": [0.3] * 768,
        },
    ]

    for chunk_data in chunks_data:
        chunk = DocumentChunk(**chunk_data)
        db_session.add(chunk)

    await db_session.flush()

    # Test a full-text search query using the content_tsv column
    result = await db_session.execute(
        text(
            """
            SELECT id, source_title, content
            FROM document_chunks
            WHERE content_tsv @@ plainto_tsquery('english', :query)
            ORDER BY id
        """
        ),
        {"query": "muscle strength"},
    )

    rows = result.fetchall()

    # Should find the first chunk that contains "muscle strength"
    assert len(rows) >= 1
    # Check that we found the relevant chunk
    found_muscle_chunk = False
    for row in rows:
        if "muscle strength" in row.content:
            found_muscle_chunk = True
            break

    assert found_muscle_chunk, "Should find chunk containing 'muscle strength'"
