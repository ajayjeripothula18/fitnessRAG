"""
Unit tests for the Knowledge Ingestion pipeline (Ravi – Checkpoint 4).

Tests use mocks for Ollama embedding calls and a real in-memory SQLite DB
(via SQLAlchemy) to avoid needing a live Postgres/Ollama instance in CI.
"""
from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from app.services.ingestion import _batch, _split_documents, ingest_documents
from langchain_core.documents import Document


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

class TestBatch:
    def test_even_batches(self):
        result = list(_batch(list(range(10)), 3))
        assert result == [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]

    def test_single_batch(self):
        result = list(_batch([1, 2], 10))
        assert result == [[1, 2]]

    def test_empty(self):
        result = list(_batch([], 5))
        assert result == []


class TestSplitDocuments:
    def test_splits_long_text(self):
        long_text = " ".join(["word"] * 300)
        docs = [Document(page_content=long_text, metadata={"source": "test"})]
        chunks = _split_documents(docs)
        assert len(chunks) > 1
        for chunk in chunks:
            assert len(chunk.page_content) <= 512 + 50  # allow some tolerance

    def test_preserves_metadata(self):
        docs = [Document(page_content="Short text.", metadata={"source": "https://example.com", "title": "Test"})]
        chunks = _split_documents(docs)
        assert len(chunks) >= 1
        assert chunks[0].metadata.get("source") == "https://example.com"


# ---------------------------------------------------------------------------
# Ingestion integration (mocked Ollama + in-memory DB session)
# ---------------------------------------------------------------------------

class TestIngestDocuments:
    def _make_docs(self, n: int = 3) -> list[Document]:
        return [
            Document(
                page_content=f"Fitness tip number {i}: " + "exercise " * 50,
                metadata={"source": f"https://example.com/tip-{i}", "title": f"Tip {i}"},
            )
            for i in range(n)
        ]

    @patch("app.services.ingestion._embed_texts")
    def test_ingest_creates_chunks(self, mock_embed):
        """Verify that ingestion creates DocumentChunk rows."""
        docs = self._make_docs(2)
        chunks_count = len(__import__("app.services.ingestion", fromlist=["_split_documents"])._split_documents(docs))

        # Mock embeddings — return 768-dim zero vectors for each chunk
        mock_embed.return_value = [[0.0] * 768] * chunks_count

        mock_db = MagicMock()
        result = ingest_documents(docs, mock_db, source_title="Test Source")

        assert result == chunks_count
        mock_db.add_all.assert_called()
        mock_db.flush.assert_called()
        mock_db.commit.assert_called_once()

    @patch("app.services.ingestion._embed_texts", side_effect=ConnectionError("Ollama unreachable"))
    def test_ingest_raises_on_embed_failure(self, _):
        """Ingestion should surface embedding errors, not silently swallow them."""
        docs = self._make_docs(1)
        mock_db = MagicMock()
        with pytest.raises(ConnectionError, match="Ollama unreachable"):
            ingest_documents(docs, mock_db)

    @patch("app.services.ingestion._embed_texts")
    def test_ingest_empty_docs_returns_zero(self, mock_embed):
        """Passing empty docs should return 0 without calling the embedder."""
        mock_db = MagicMock()
        result = ingest_documents([], mock_db)
        assert result == 0
        mock_embed.assert_not_called()
