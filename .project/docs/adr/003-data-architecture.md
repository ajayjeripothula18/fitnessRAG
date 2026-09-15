# ADR-003: Data Architecture — Unified PostgreSQL with pgvector
## Created by Arjun (CTO)
## Status: Accepted
## Date: 2026-08-31

---

## Context

FitnessRAG requires three categories of data storage:
1. **Application Data**: Users, profiles, conversations, plans, measurements, workout logs
2. **Vector Embeddings**: Knowledge base chunks for RAG retrieval (semantic search)
3. **Audit Data**: Safety gateway decisions, AI interaction logs

We must choose between separate specialized databases or a unified approach, with a hard constraint of $0/month operating cost.

## Decision

### Unified PostgreSQL with pgvector Extension

We will use a **single PostgreSQL 16 database** with the **pgvector** extension for all data storage needs.

### Key Design Decisions

#### 1. UUIDs as Primary Keys
```sql
id UUID PRIMARY KEY DEFAULT gen_random_uuid()
```
- **Why**: Prevents ID enumeration attacks, safe for client-side generation, no sequential leakage
- **Trade-off**: Slightly larger than integer PKs (16 bytes vs 4 bytes), but negligible at our scale

#### 2. Soft Deletes via `deleted_at`
```sql
deleted_at TIMESTAMPTZ DEFAULT NULL
```
- **Why**: GDPR compliance — data is recoverable during grace period, then hard-deleted by scheduled job
- **Convention**: All queries include `WHERE deleted_at IS NULL` by default (enforced by SQLAlchemy mixin)

#### 3. JSONB for Flexible Structured Data
```sql
plan_data JSONB NOT NULL  -- Stores full plan structure
metadata JSONB DEFAULT '{}'  -- Extensible metadata
```
- **Why**: Plan structures are semi-structured (varying exercises, sets, reps per day) — JSONB avoids explosion of normalized tables while maintaining query capability
- **When**: Used for `plan_data`, `exercise_data`, `metadata` fields
- **When NOT**: Used for fields that need indexing, foreign keys, or strict validation — those remain as typed columns

#### 4. pgvector for Embeddings
```sql
embedding vector(384) NOT NULL  -- BGE-small-en-v1.5 produces 384d vectors
```
- **Why**: Eliminates separate vector database, unified in one free-tier PostgreSQL instance
- **Index**: IVFFlat initially (simpler, sufficient for <10K chunks), HNSW if performance requires

#### 5. Full-Text Search via tsvector
```sql
search_vector tsvector GENERATED ALWAYS AS (
    setweight(to_tsvector('english', coalesce(title, '')), 'A') ||
    setweight(to_tsvector('english', coalesce(content, '')), 'B')
) STORED
```
- **Why**: Hybrid search (vector + lexical) improves RAG retrieval quality
- **How**: Combined with vector search via Reciprocal Rank Fusion (RRF)

### Schema Overview

```
┌─────────────────────────────────────────────────────────┐
│                     PostgreSQL 16                        │
│                                                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │   users      │  │   profiles  │  │conversations│     │
│  │   (auth)     │──│  (fitness)  │  │  (threads)  │     │
│  └──────┬───────┘  └─────────────┘  └──────┬──────┘     │
│         │                                   │           │
│  ┌──────┴───────┐                   ┌──────┴──────┐     │
│  │   plans      │                   │  messages   │     │
│  │  (workouts)  │                   │  (chat)     │     │
│  └──────┬───────┘                   └─────────────┘     │
│         │                                               │
│  ┌──────┴───────┐  ┌─────────────┐  ┌─────────────┐     │
│  │plan_versions │  │workout_logs │  │   body_     │     │
│  │  (history)   │  │ (tracking)  │  │measurements │     │
│  └──────────────┘  └─────────────┘  └─────────────┘     │
│                                                         │
│  ┌─────────────────────────────────────────────────┐     │
│  │           knowledge_chunks (RAG)                │     │
│  │  content TEXT + embedding VECTOR(384)            │     │
│  │  + search_vector TSVECTOR                       │     │
│  └─────────────────────────────────────────────────┘     │
│                                                         │
│  ┌─────────────────────────────────────────────────┐     │
│  │        safety_audit_logs (audit)                │     │
│  │  input_hash + category + action + scores        │     │
│  └─────────────────────────────────────────────────┘     │
│                                                         │
│  Extensions: pgvector, pg_trgm                          │
└─────────────────────────────────────────────────────────┘
```

### Indexing Strategy

| Table | Index | Type | Rationale |
|-------|-------|------|-----------|
| `users` | `email` | UNIQUE B-tree | Login lookup |
| `users` | `deleted_at` | Partial B-tree (`WHERE deleted_at IS NULL`) | Soft delete filtering |
| `knowledge_chunks` | `embedding` | IVFFlat (lists=100) | Vector similarity search |
| `knowledge_chunks` | `search_vector` | GIN | Full-text search |
| `knowledge_chunks` | `source_id, evidence_tier` | B-tree | Metadata filtering before vector search |
| `messages` | `conversation_id, created_at` | B-tree | Conversation history pagination |
| `plans` | `user_id, status` | B-tree | Active plan lookup |
| `workout_logs` | `user_id, date` | B-tree | Workout history queries |
| `body_measurements` | `user_id, date` | UNIQUE B-tree | One measurement per day, trend queries |
| `safety_audit_logs` | `created_at, safety_category` | B-tree | Audit queries by date/category |

### Migration Strategy
- **Tool**: Alembic (integrated with SQLAlchemy)
- **Convention**: Every migration must be reversible (`upgrade` + `downgrade`)
- **Naming**: `{timestamp}_{description}.py` (e.g., `20260901_add_user_memory_table.py`)
- **Testing**: Run `upgrade` + `downgrade` + `upgrade` in CI to verify reversibility

## Alternatives Considered

### Separate Vector Database (Pinecone/Qdrant/Weaviate)
- **Pro**: Purpose-built for vector operations, potentially better performance at scale
- **Con**: Additional service to manage, separate free-tier to track
- **Con**: Data synchronization between application DB and vector DB
- **Con**: Increased deployment complexity
- **Decision**: Not needed at our scale (<10K vectors); pgvector sufficient

### MongoDB + Atlas Search
- **Pro**: Flexible schema for varied plan structures, built-in vector search
- **Con**: No free tier with vector search
- **Con**: Loss of relational integrity for user/conversation/plan relationships
- **Con**: Less familiar for portfolio evaluators expecting SQL skills

### SQLite + ChromaDB
- **Pro**: Simplest possible setup, zero configuration
- **Con**: No concurrent access (problematic for web application)
- **Con**: No free-tier cloud hosting for SQLite
- **Con**: ChromaDB adds separate dependency

### Supabase (Managed PostgreSQL)
- **Pro**: Free tier includes PostgreSQL + pgvector + Auth + Realtime + REST API
- **Con**: Vendor lock-in for some features
- **Decision**: Strong candidate for **hosting** the PostgreSQL instance we've designed. We use standard PostgreSQL/pgvector — Supabase is just the managed provider.

## Consequences

### Positive
- Single database simplifies deployment, backup, and monitoring
- Unified transactions across application data and vector operations
- PostgreSQL's maturity provides excellent tooling and documentation
- pgvector's cosine similarity is sufficient for 384d embeddings at <10K scale
- JSONB provides flexible schema without abandoning relational integrity
- Soft deletes enable GDPR compliance without data architecture changes

### Negative
- pgvector performance may degrade at >100K vectors (unlikely for MVP)
- IVFFlat requires periodic re-indexing as data grows
- JSONB queries are less optimized than normalized table joins
- Single database is a single point of failure (mitigated by managed hosting with backups)

### Risks
- **pgvector IVFFlat recall degradation**: Monitor query quality; plan HNSW migration if needed
- **Free tier storage limits**: Neon (0.5 GB free), Supabase (500 MB free) — sufficient for MVP but monitor growth
- **JSONB schema drift**: Enforce Pydantic validation at application layer to maintain consistency

## References
- Database Design: `/docs/database_design.md`
- Technical Design: `/docs/technical_design.md` (Section 6: Database Layer)
- pgvector Performance: https://github.com/pgvector/pgvector#indexing
