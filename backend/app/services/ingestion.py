"""
Knowledge Ingestion Pipeline (Ravi – Checkpoint 4)

Responsibilities:
- Load documents from URLs or local files
- Split into appropriately-sized chunks with overlap
- Generate 768-dim embeddings via nomic-embed-text (Ollama)
- Persist DocumentChunk rows into PostgreSQL / pgvector
"""
from __future__ import annotations

import logging
from typing import Generator, Sequence

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import (
    TextLoader,
    WebBaseLoader,
)
from langchain_core.documents import Document
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.document_chunk import DocumentChunk

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Splitter config — tuned for fitness Q&A content
# ---------------------------------------------------------------------------
CHUNK_SIZE = 512
CHUNK_OVERLAP = 64

_splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
    separators=["\n\n", "\n", ".", " ", ""],
)


# ---------------------------------------------------------------------------
# Embedding helper (calls local Ollama)
# ---------------------------------------------------------------------------


def _embed_texts(texts: list[str]) -> list[list[float]]:
    """
    Generate embeddings for a list of texts using the configured Ollama model.

    Returns a list of float vectors (one per input text).
    """
    import ollama  # lazy import – not needed at module load

    response = ollama.embed(
        model=settings.OLLAMA_EMBEDDING_MODEL,
        input=texts,
        host=settings.OLLAMA_BASE_URL,
    )
    return response.embeddings


# ---------------------------------------------------------------------------
# Chunk generators
# ---------------------------------------------------------------------------


def _split_documents(docs: list[Document]) -> list[Document]:
    """Split a list of LangChain documents into smaller chunks."""
    return _splitter.split_documents(docs)


def load_from_url(url: str) -> list[Document]:
    """Load a web page and return LangChain Documents."""
    loader = WebBaseLoader(url)
    return loader.load()


def load_from_file(file_path: str) -> list[Document]:
    """Load a local text file and return LangChain Documents."""
    loader = TextLoader(file_path)
    return loader.load()


# ---------------------------------------------------------------------------
# Batch ingestion
# ---------------------------------------------------------------------------


def _batch(seq: Sequence, n: int) -> Generator[Sequence, None, None]:
    """Yield successive n-sized batches from seq."""
    for i in range(0, len(seq), n):
        yield seq[i : i + n]


def ingest_documents(
    docs: list[Document],
    db: Session,
    source_title: str = "Unknown",
    batch_size: int = 32,
) -> int:
    """
    Chunk, embed, and persist a list of LangChain Documents.

    Args:
        docs: Raw LangChain documents (one per source page/file).
        db:   Active SQLAlchemy session.
        source_title: Display name used in citations.
        batch_size:   How many chunks to embed per Ollama request.

    Returns:
        Number of DocumentChunk rows written to the DB.
    """
    chunks = _split_documents(docs)
    if not chunks:
        logger.warning("No chunks produced from provided documents.")
        return 0

    total = 0
    for batch in _batch(chunks, batch_size):
        texts = [c.page_content for c in batch]
        try:
            embeddings = _embed_texts(texts)
        except Exception as exc:
            logger.error("Embedding failed for batch: %s", exc)
            raise

        db_objs = [
            DocumentChunk(
                source_url=chunk.metadata.get("source", ""),
                source_title=chunk.metadata.get("title", source_title),
                page_number=chunk.metadata.get("page", None),
                content=chunk.page_content,
                embedding=embedding,
            )
            for chunk, embedding in zip(batch, embeddings)
        ]
        db.add_all(db_objs)
        db.flush()  # batch write; caller commits
        total += len(db_objs)
        logger.info(
            "Ingested batch of %d chunks (total so far: %d).", len(db_objs), total
        )

    db.commit()
    logger.info("Ingestion complete. Total chunks stored: %d", total)
    return total


def ingest_url(url: str, db: Session, source_title: str | None = None) -> int:
    """Convenience wrapper: load a URL and ingest all its content."""
    docs = load_from_url(url)
    return ingest_documents(docs, db, source_title=source_title or url)


def ingest_file(file_path: str, db: Session, source_title: str | None = None) -> int:
    """Convenience wrapper: load a local file and ingest its content."""
    docs = load_from_file(file_path)
    return ingest_documents(docs, db, source_title=source_title or file_path)
