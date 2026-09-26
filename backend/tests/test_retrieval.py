"""
Unit tests for the Simplified Retrieval service (Ravi – Checkpoint 4).

All pgvector + Ollama calls are mocked so tests run without infrastructure.
"""
from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from app.services.retrieval import (
    TOP_K_FINAL,
    RetrievedChunk,
)
from app.models.document_chunk import DocumentChunk


def _make_chunk(chunk_id: int, content: str = "fitness tip content") -> DocumentChunk:
    """Factory for mock DocumentChunk objects."""
    chunk = MagicMock(spec=DocumentChunk)
    chunk.id = chunk_id
    chunk.content = content
    chunk.source_url = f"https://example.com/{chunk_id}"
    chunk.source_title = f"Source {chunk_id}"
    chunk.page_number = None
    return chunk


class TestRetrieve:
    @patch("app.services.retrieval._embed_query", return_value=[0.1] * 768)
    @patch("app.services.retrieval._vector_search")
    def test_retrieve_returns_top_k(self, mock_vector, mock_embed):
        # mock_vector should return a list of tuples: (DocumentChunk, float)
        candidates = [
            (_make_chunk(i, f"fitness content for chunk {i}"), 0.9 - (0.01 * i))
            for i in range(10)
        ]
        mock_vector.side_effect = (
            lambda query_embedding, db, top_k=TOP_K_FINAL: candidates[:top_k]
        )

        from app.services.retrieval import retrieve

        results = retrieve("how to build muscle", db=MagicMock(), top_k=TOP_K_FINAL)

        assert len(results) <= TOP_K_FINAL
        assert all(isinstance(r, RetrievedChunk) for r in results)
        assert (
            results[0].vector_score > results[-1].vector_score
        )  # Assuming sorted by score

    @patch("app.services.retrieval._embed_query", return_value=[0.0] * 768)
    @patch("app.services.retrieval._vector_search", return_value=[])
    def test_retrieve_returns_empty_when_no_results(self, _vs, _eq):
        from app.services.retrieval import retrieve

        results = retrieve("anything", db=MagicMock())
        assert results == []

    @patch(
        "app.services.retrieval._embed_query",
        side_effect=ConnectionError("Ollama down"),
    )
    def test_retrieve_raises_on_embed_failure(self, _):
        from app.services.retrieval import retrieve

        with pytest.raises(ConnectionError):
            retrieve("test query", db=MagicMock())
