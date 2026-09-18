# FitnessRAG Current-State Assessment Snapshot

**Assessment Date:** 2026-09-18
**Repository:** ajayjeripothula18/fitnessRAG
**Branch Assessed:** main
**Exact Assessed Commit SHA:** a8eb9e15d0734fc5b7d7b7ea460a4f5aea18858f
**Document Status:** ASSESSMENT SNAPSHOT
**Purpose:** To establish a trusted, evidence-based record of the state of FitnessRAG at this point in the project lifecycle, answering: "What did we establish about the state of FitnessRAG at this point?"
**Scope:** This snapshot covers the repository state at commit `a8eb9e15d0734fc5b7d7b7ea460a4f5aea18858f` (implementation baseline, documentation-vs-code differences) and the runtime/environment verification performed on 2026-09-18 (environment/database state, verified findings, unresolved decisions, evidence gaps). It does not repeat expensive investigations already performed.
**Limitations:** This is a historical snapshot and is not intended to be continuously maintained. It does not include future plans, backlog items, or speculative architecture. Findings are based on evidence available up to the assessed commit and the verification date; later changes are not reflected.

---

## 1. Repository Baseline (at commit a8eb9e15d0734fc5b7d7b7ea460a4f5aea18858f)

- **Default Branch:** `main` (default branch; currently NOT protected)
- **Remote Branch State:** `origin/main` exists and is at commit `bc594f6e06cf79b7ad3a8f25f29b3c434158a329`. Local `main` is ahead of `origin/main` by four commits:
  - `a8eb9e15d0734fc5b7d7b7ea460a4f5aea18858f` (adoption of the Engineering Operating Model v1.0)
  - `d7e9338` (docs: add 2026-09-18 current-state assessment)
  - `5156560` (docs: add 2026-09-18 current-state assessment (WIP))
  - `f671bd6` (docs: finalize current-state assessment snapshot)
- **Repository Visibility:** Public (as of assessment).
- **Migration State:** The repository has undergone a migration to a single-mainline model (`main` as the sole long-lived branch), with feature/fix/chore branches being short-lived. No `develop` branch is present.
- **Current Documentation Structure:** The `docs/` directory contains durable engineering documentation, including:
  - `ENGINEERING_OPERATING_MODEL.md` (adopted v1.0)
  - `api_contracts.md`, `architecture_document.md`, `database_design.md`, `product_requirements.md`, `safety_gateway_spec.md`, `testing_strategy.md`
  - `adr/` directory with three ADRs (001–003)
- **Presence of `.project/`:** The `.project/` directory exists and contains historical material (research docs, onboarding, templates, etc.). It is retained for context but does not govern current execution.
- **Relevant Untracked/Local-only Material:**
  - Alembic migration file `backend/alembic/versions/ae2a53256191_initial_migration.py` exists locally but is ignored by `.gitignore` (see Section 9).
  - The approved Engineering Operating Model v1.0 source (`FitnessRAG_Engineering_Operating_Model_v1.0_APPROVED.md`) is present in the repository root as an untracked file (used for adoption).
  - No other significant untracked files affecting the baseline.

---

## 2. Engineering Process Baseline

The approved v1.0 Engineering Operating Model has been adopted into the repository (commit `a8eb9e15d0734fc5b7d7b7ea460a4f5aea18858f`).
- **Adoption Commit:** `a8eb9e15d0734fc5b7d7b7ea460a4f5aea18858f` (`docs: adopt approved engineering operating model v1.0`)
- **Reference:** `docs/ENGINEERING_OPERATING_MODEL.md`
The assessment does not duplicate the Operating Model; it confirms its presence and adoption.

---

## 3. Application Implementation Baseline (at commit a8eb9e15d0734fc5b7d7b7ea460a4f5aea18858f)

### Backend
- **Framework/Runtime:** FastAPI 0.109.0+, Uvicorn, Python 3.11+
- **Authentication/Profile:** JWT-based authentication (`python-jose`, `passlib`); `Profile` model exists but no endpoints implemented.
- **Chat:** Endpoint `/api/v1/chat` integrates with LangGraph RAG pipeline; includes input/output safety checks.
- **RAG Orchestration:** LangGraph state graph (`app/ai/graph.py`) managing flow: safety check → retrieve → generate → output safety.
- **Retrieval Approach:** Vector search via `pgvector` cosine similarity (`app/services/retrieval.py`); top-k configurable (default 5). No hybrid search or BM25 implemented.
- **Safety Implementation:** Keyword-based classification (safe/medical/dangerous) via middleware and LangGraph nodes; keyword lists in `app/services/safety_gateway.py`.
- **Database Integration:** SQLAlchemy 2.0 with asyncpg driver; Alembic for migrations; `document_chunks` table with `content`, `content_tsv` (TSVECTOR), and `embedding` (pgvector) columns.

### Frontend
- **Framework:** React 19.2.8+, Vite, TypeScript
- **Implemented Areas:**
  - Authentication flow (login, register, refresh) via Zod and Axios
  - Chat interface (`ChatPage.tsx`, `ChatContainer.tsx`) with message sending, display of citations, and typing indicator
  - Route protection for authenticated pages
- **Incomplete/Placeholder Areas:**
  - User profile, settings, exercise library, workout plans, progress tracking (render `PlaceholderPage` components)
  - No persistence of chat history across page reloads (frontend state in memory only)
  - No document management UI for ingestion

### Database
- **Implemented Tables/Entities:**
  - `users`, `conversations`, `messages`, `document_chunks` (verified via `pg_attribute` and migrations)
  - `document_chunks` includes: `id` (PK), `source_url`, `source_title`, `page_number`, `content`, `content_tsv` (TSVECTOR), `embedding` (vector)
- **Important Schema Characteristics:**
  - `embedding` column is of type `vector(768)` (confirmed via `pg_attribute.atttypmod`)
  - HNSW index on `embedding` for cosine similarity (`vector_cosine_ops`)
  - GIN index on `content_tsv` for full-text search
- **Known Implementation/Documentation Differences:**
  - `docs/database_design.md` documents `VECTOR(384)` for `embedding` (see CSA-001)
  - No additional database-table mismatch was confirmed during this assessment beyond CSA-001.

---

## 4. RAG / Retrieval Baseline (at commit a8eb9e15d0734fc5b7d7b7ea460a4f5aea18858f)

- **Current Retrieieval Architecture:**
  - Embedding model: `nomic-embed-text` via Ollama (768 dimensions)
  - Retrieval: Vector search only (cosine distance) using `pgvector` (`<=>` operator)
  - Top-K: Default 5 (`TOP_K_FINAL` in `app/services/retrieval.py`)
  - No hybrid search, BM25, RRF, reranking, or metadata filtering is implemented.
- **Important Characteristics:**
  - Retrieval service (`app/services/retrieval.py`) exposes `_vector_search` and `_embed_query` functions.
  - The LangGraph pipeline includes a safety check node before retrieval and an output safety node after generation.
  - No caching layer (e.g., Redis) for retrieval results.
- **Verification:** The assessment does not claim features beyond what is verified in the codebase and database schema.

---

## 5. Database / Environment Baseline (verified 2026-09-18)

- **Docker Database Container:**
  - Service name: `db` (image: `ankane/pgvector:latest`)
  - Container port: `5432` (PostgreSQL)
  - Host-exposed port: `5433` (mapping: `5433:5432` in `docker-compose.yml`)
- **PostgreSQL Version:** `PostgreSQL 15.4 (Debian 15.4-2.pgdg120+1)`
- **pgvector Version:** `0.5.1`
- **Backend Container Connection Target:** `db:5432` (via environment variables `POSTGRES_SERVER=db`, `POSTGRES_PORT=5432`)
- **Database Name:** `fitnessrag`
- **`public.document_chunks` Table:** Exists
- **Current Row Count:** `0` rows (verified via `SELECT COUNT(*)`)
- **Embedding Schema Dimension:** `vector(768)` (verified via `pg_attribute.atttypmod = 768`)
- **Host PostgreSQL Removal:** The host PostgreSQL instance that previously occupied `localhost:5432` has been stopped/removed; no listener on port 5432.
- **Host Access Path:** `localhost:5433 → db:5432` (verified via `psql -h localhost -p 5433 -d fitnessrag`)
- **Important Distinction:**
  - Container-internal connection uses `db:5432` (service name and container port)
  - Host access uses `localhost:5433` (mapped port); `5433` is **not** the internal PostgreSQL service port.

---

## 6. Important Verified Findings

### CSA-001 — Embedding dimension documentation mismatch
- **Evidence:**
  - `docs/database_design.md`: `embedding VECTOR(384)`
  - `backend/app/models/document_chunk.py`: `EMBEDDING_DIM = 768`
  - Live Docker database: `embedding` column type `vector(768)` (from `pg_attribute.atttypmod`)
- **Classification:** `STALE DOCUMENTATION`
- **Important Limitation:** Docker `document_chunks` currently has 0 rows; actual stored-vector dimensionality has not been sampled.
- **Note:** No ingestion bug has been established. The Docker `document_chunks` table currently contains zero rows, so actual persisted embeddings and ingestion output have not been validated.
- **Audit Note:** This finding was also identified in the earlier large read-only current-state audit.

### CSA-002 — Alembic migration not tracked
- **Evidence:**
  - Local migration file: `backend/alembic/versions/ae2a53256191_initial_migration.py` (exists, size 6.9 KB)
  - Not tracked by Git (`git status --porcelain` shows no entry)
  - Absent from `origin/main` (`git show origin/main:<path>` → fatal: path … exists on disk, but not in 'origin/main')
  - `.gitignore` rule: `backend/**/alembic/versions/*.py` (line 167) with exception for `__init__.py` (line 168)
- **Classification:** `DECISION REQUIRED`
- **Decision Question:** Is intentionally ignoring Alembic migration files the desired repository policy, or is this an accidental repository-configuration defect?
- **Audit Note:** This finding was also identified in the earlier large read-only current-state audit.

### CSA-003 — Docker database is the intended development database
- **Evidence:**
  - Docker service `db` is defined in `docker-compose.yml`
  - Backend configuration uses `POSTGRES_SERVER=db` and `POSTGRES_PORT=5432` (`.env`)
  - Docker maps host `5433` to container `5432`
  - Docker database is healthy and reachable (`psql -h localhost -p 5433 -d fitnessrag` succeeds)
- **Classification:** `VERIFIED ENVIRONMENT STATE`
- **Note:** The `5433:5432` mapping is intentional and not a defect.

### CSA-004 — Docker database currently contains zero document chunks
- **Evidence:**
  - `public.document_chunks` table exists
  - Row count: `0` (`SELECT COUNT(*) FROM document_chunks`)
- **Classification:** `EVIDENCE GAP`
- **Impact:** The database schema can be validated, but actual persisted embedding rows cannot currently be inspected.
- **Note:** Do not manufacture test data solely to remove this observation.

### CSA-005 — pgvector version difference
- **Evidence:**
  - Previously installed host PostgreSQL (observed on `localhost:5432` earlier): `pgvector 0.8.6`
  - Current Docker PostgreSQL (`fitnessrag_db`): `pgvector 0.5.1`
- **Classification:** `ENVIRONMENT OBSERVATION`
- **Note:** Only the pgvector extension version differs; the schema (`vector(768)`) is identical. No action required for this task.

---

## 7. Important Distinction: Assessment vs Backlog

This document is a **historical snapshot**, not a living backlog or reconciliation system. Each actionable finding ends with one of the following:

- CSA-001: Documentation correction likely required
- CSA-002: Requires decision
- CSA-003: No action established yet (environment is verified and healthy)
- CSA-004: Evidence gap — no action until data is ingested
- CSA-005: No action established yet (version difference noted)

No GitHub Issues are created during this task.

---

## 8. Decision Register

### Decisions Required

| Decision ID | Question | Evidence | Why It Matters | Possible Directions | Current Status |
|-------------|----------|----------|----------------|---------------------|----------------|
| DEC-001 | Is intentionally ignoring Alembic migration files the desired repository policy, or is this an accidental repository-configuration defect? | Local migration file exists; `.gitignore` excludes `backend/**/alembic/versions/*.py`; file absent from `origin/main` | Determines whether migration history is preserved in the repository. If intentional, the policy should be documented; if accidental, the `.gitignore` should be corrected and the migration file added. | 1. Keep current policy (ignore migrations) and document it.<br>2. Remove the ignore rule, commit the migration file, and version future migrations. | Under review; no option selected yet. |

---

## 9. Evidence Gaps

- **No stored embeddings:** The Docker `document_chunks` table is empty (`0` rows), so actual stored-vector dimensions cannot be sampled.
- **Runtime application behavior:** The backend is not currently running (no uvicorn/FastAPI processes detected), so live API behavior, RAG pipeline execution, and safety checks cannot be observed at this moment.
- **Any other material gaps:** None identified beyond the above.

---

## 10. No Process Duplication

This assessment does not duplicate:
- The Engineering Operating Model (`docs/ENGINEERING_OPERATING_MODEL.md`) — referenced, not copied.
- Product Requirements document (`docs/product_requirements.md`) — not duplicated.
- Architecture document (`docs/architecture_document.md`) — not duplicated.
- Database Design document (`docs/database_design.md`) — referenced for CSA-001, not copied.
- API contract (`docs/api_contracts.md`) — not duplicated.
- Safety Gateway specification (`docs/safety_gateway_spec.md`) — not duplicated.
- Testing Strategy (`docs/testing_strategy.md`) — not duplicated.
- Historical `.project/` material — referenced for context, not preserved as process authority.

---

## 11. Historical Role of `.project/`

The `.project/` directory is historical/context material. It contains:
- Research documents (e.g., `ravi_tech_lead_research.md`, `priya_cpo_research.md`)
- Onboarding guides (`CLAUDE_PM_ONBOARDING.md`)
- Templates and legacy process files (RRPAI workflow)

Current work belongs in GitHub (Issues, Projects). Durable engineering knowledge belongs in `docs/`. Historical information may be retained for context, but old process/persona/checkpoint material does not govern current execution. No cleanup of `.project/` is performed in this task.

---

## 12. Quality Check

Before committing, we verified:
- This is a snapshot, not a living reconciliation system.
- Facts are separated from assumptions; classifications are justified by evidence.
- No secrets are included in the document.
- No application code, documentation, database, Docker configuration, `.gitignore`, backlog files, or unrelated docs were changed during this assessment.
- The only change is the addition of this assessment file.

We confirmed with:
```
git status --short
git diff -- docs/assessments/2026-09-18-current-state-assessment.md
```
(Only the new file appears.)

---

## 13. Commit

Commit SHA: [omitted per instruction — see Git history]

---

## 14. Final Report

- **Assessment file path:** `docs/assessments/2026-09-18-current-state-assessment.md`
- **Assessed commit SHA:** `a8eb9e15d0734fc5b7d7b7ea460a4f5aea18858f`
- **Assessment document commit SHA:** [omitted]
- **Number of findings:** 5 (CSA-001, CSA-002, CSA-003, CSA-004, CSA-005)
- **Number of confirmed bugs:** 0
- **Number of stale documentation findings:** 1 (CSA-001)
- **Number of decision-required findings:** 1 (CSA-002)
- **Number of evidence gaps:** 1 (CSA-004)
- **Unresolved decisions:** 1 (DEC-001: Alembic migration tracking policy)
- **Changes made:** Only the assessment file was added and later updated; no application code, documentation, database, Docker configuration, `.gitignore`, backlog files, or unrelated docs were modified during this assessment.

This assessment is a **historical snapshot** and is not intended to be continuously maintained. The next phase after this document is:
Assessment → Decisions → GitHub Issues → Backlog Ordering → Sprint Planning