"""
DocumentChunk model — stores ingested knowledge as vector-embedded text chunks.

Each row represents a single chunk from a source document, with:
- `embedding`: 768-dim nomic-embed-text vector stored in pgvector
- `content_tsv`: tsvector for BM25 full-text search (populated by DB trigger)
- `source_url`, `source_title`, `page_number`: provenance for citation rendering
"""
from pgvector.sqlalchemy import Vector  # type: ignore[import]
from sqlalchemy import Column, Index, Integer, String, Text
from sqlalchemy.dialects.postgresql import TSVECTOR
from sqlalchemy.sql import func

from app.models.base import BaseModel

EMBEDDING_DIM = 768  # nomic-embed-text output dimension


class DocumentChunk(BaseModel):
    """A single chunk of a fitness knowledge document with its vector embedding."""

    __tablename__ = "document_chunks"

    # Source provenance
    source_url = Column(String(2048), nullable=False, index=True)
    source_title = Column(String(512), nullable=False)
    page_number = Column(Integer, nullable=True)  # For PDFs; null for web pages

    # Content
    content = Column(Text, nullable=False)

    # Full-text search (BM25 proxy) — auto-populated via DB trigger in migration
    content_tsv = Column(TSVECTOR, nullable=True)

    # Vector embedding (768-dim from nomic-embed-text via Ollama)
    embedding: Column[Vector] = Column(Vector(EMBEDDING_DIM), nullable=True)

    __table_args__ = (
        # HNSW index for fast approximate nearest-neighbour search on embeddings
        Index(
            "ix_document_chunks_embedding_hnsw",
            "embedding",
            postgresql_using="hnsw",
            postgresql_with={"m": 16, "ef_construction": 64},
            postgresql_ops={"embedding": "vector_cosine_ops"},
        ),
        # GIN index for fast full-text search on tsvector column
        Index(
            "ix_document_chunks_content_tsv_gin",
            "content_tsv",
            postgresql_using="gin",
        ),
    )
