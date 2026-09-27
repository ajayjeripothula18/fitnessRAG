"""
Retrieval Service — Vector Search (Checkpoint 4 - Simplified MVP)

Strategy:
1. Dense retrieval: pgvector cosine distance on embeddings
"""
from __future__ import annotations

import logging
import time
from dataclasses import dataclass
from typing import Sequence

import ollama
from sqlalchemy import text
from sqlalchemy.sql.elements import Label
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.document_chunk import EMBEDDING_DIM, DocumentChunk

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
TOP_K_VECTOR = 20  # Candidates retrieved from vector search
TOP_K_FINAL = 5  # Results returned to the LangGraph agent


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------
@dataclass
class RetrievedChunk:
    """A retrieved document chunk with provenance metadata and score."""

    id: int
    content: str
    source_url: str
    source_title: str
    page_number: int | None
    vector_score: float


# ---------------------------------------------------------------------------
# Embedding helper (reuse from ingestion)
# ---------------------------------------------------------------------------
def _embed_query(query: str) -> Sequence[float]:
    """Generate a single embedding vector for a search query."""
    response = ollama.Client(host=settings.OLLAMA_BASE_URL).embed(
        model=settings.OLLAMA_EMBEDDING_MODEL,
        input=[query],
    )
    return response.embeddings[0]


# ---------------------------------------------------------------------------
# Vector retrieval
# ---------------------------------------------------------------------------
def _vector_search(
    query_embedding: Sequence[float], db: Session, top_k: int = TOP_K_VECTOR
) -> list[tuple[DocumentChunk, float]]:
    """Retrieve top-k document chunks by cosine similarity."""
    embedding_literal = "[" + ",".join(str(v) for v in query_embedding) + "]"
    distance_expr: Label = text(f"embedding <=> '{embedding_literal}'::vector").label(
        "distance"
    )

    # Use pgvector operator (<=> = cosine distance) for ordering
    rows = (
        db.query(DocumentChunk, distance_expr)
        .order_by(distance_expr)
        .limit(top_k)
        .all()
    )
    # Convert distance to similarity score
    return [(chunk, 1.0 - distance) for chunk, distance in rows]


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------
def retrieve(query: str, db: Session, top_k: int = TOP_K_FINAL) -> list[RetrievedChunk]:
    """
    Run vector retrieval and return the top-k most relevant DocumentChunks.

    Steps:
    1. Embed the query with nomic-embed-text
    2. Vector search (pgvector cosine similarity)
    3. Return top-k RetrievedChunk objects

    Args:
        query:  The user's natural-language question.
        db:     Active SQLAlchemy session.
        top_k:  Number of results to return.

    Returns:
        Sorted list of RetrievedChunk (best match first).
    """
    start_time = time.time()
    try:
        query_embedding = _embed_query(query)
    except Exception as exc:
        logger.error("Failed to embed query '%s': %s", query, exc)
        raise

    vector_results = _vector_search(query_embedding, db, top_k=top_k)

    latency = time.time() - start_time
    logger.info(
        "Retrieval completed in %.3f seconds, found %d results",
        latency,
        len(vector_results),
    )

    if not vector_results:
        logger.warning("Vector search returned no results for query: %s", query)
        return []

    return [
        RetrievedChunk(
            id=int(chunk.id),
            content=str(chunk.content),
            source_url=str(chunk.source_url),
            source_title=str(chunk.source_title),
            page_number=int(chunk.page_number)
            if chunk.page_number is not None
            else None,
            vector_score=float(score),
        )
        for chunk, score in vector_results
    ]
