# FitnessRAG Current-State Assessment

**Assessment date:** 2026-09-28
**Repository:** `ajayjeripothula18/fitnessRAG`
**Baseline branch:** `main`
**Baseline commit:** `98f5a10`
**Assessment type:** Post-recovery engineering and product current-state assessment

## 1. Purpose

This assessment establishes the current state of FitnessRAG after the repository recovery work was merged into `main`.

The assessment is intended to provide the evidence-backed baseline for the next backlog-recovery and Sprint-planning cycle. It distinguishes implemented infrastructure from end-to-end product capabilities and separates confirmed defects/discrepancies from future product work.

## 2. Evidence Sources

The assessment was established using:

- `docs/product_requirements.md` as the product target.
- The repository at commit `98f5a10` on `main`.
- Independent read-only repository audits performed by Claude Code and Antigravity.
- Direct cross-verification of material findings against the committed GitHub source at `98f5a10`.

The earlier `docs/assessments/2026-09-18-current-state-assessment.md` is treated as a historical snapshot. It is not used as the current-state authority when it conflicts with evidence from `98f5a10`.

## 3. Executive Summary

FitnessRAG has a functioning application foundation covering authentication, user/profile persistence, a FastAPI API, a LangGraph-based AI pipeline, safety checks, pgvector-backed retrieval, document-ingestion services, PostgreSQL persistence, and automated CI configuration.

The current product is not yet an end-to-end implementation of the MVP described in the PRD. Several important user-facing capabilities are absent, including the profile UI, workout-plan management, progress tracking, body-composition estimation, and a user-facing knowledge-ingestion workflow.

In addition, the current `main` branch contains confirmed frontend/backend API contract mismatches in authentication and chat. These are defects in the current implementation rather than future product features and should be addressed before relying on the application as a coherent end-to-end flow.

The RAG implementation currently uses dense vector retrieval only. The repository contains a `TSVECTOR` column and GIN index, but the migration history contains no trigger that automatically populates `content_tsv`, and the retrieval service does not implement hybrid vector + keyword fusion.

## 4. Capability Matrix

| Capability | Status | Evidence | Notes |
|---|---|---|---|
| Email/password registration | Implemented | `backend/app/api/v1/auth.py` | Backend registration endpoint exists and is tested. |
| Email/password login | Implemented backend; frontend integration has a contract mismatch | `backend/app/api/v1/auth.py`, `frontend/src/services/authService.ts` | Backend login exists; frontend current-user lookup uses a different path. |
| JWT access/refresh tokens | Implemented | `backend/app/api/v1/auth.py`, `backend/app/core/security.py` | Access and refresh token endpoints exist. |
| Current-user endpoint | Implemented | `GET /api/v1/auth/me` | Backend endpoint exists. |
| Profile persistence | Implemented | `backend/app/models/profile.py`, `backend/app/api/v1/users.py` | One-to-one profile model and GET/PUT endpoints exist. |
| Profile UI | Not implemented | `frontend/src/App.tsx` | No profile page; UI routes currently consist of dashboard/chat/auth plus placeholders. |
| AI chat backend | Implemented foundation | `backend/app/api/v1/chat.py`, `backend/app/ai/graph.py` | Chat endpoint invokes the LangGraph pipeline and persists messages. |
| AI chat frontend integration | Defective / contract mismatch | `frontend/src/services/chatService.ts`, `backend/app/api/v1/chat.py` | Frontend uses `/api/v1/chat`; backend exposes `/api/v1/chat/message`; response shapes also differ. |
| Conversation persistence | Implemented | `backend/app/api/v1/chat.py`, `backend/app/models/conversation.py`, `backend/app/models/message.py` | User and assistant messages are persisted. |
| Conversation history endpoint | Implemented | `GET /api/v1/chat/history/{conversation_id}` | Backend history retrieval exists. |
| History integrated into current chat UI | Not implemented | `frontend/src/components/chat/ChatContainer.tsx` | UI does not load history and does not send `history` in the current request. |
| Safety gateway | Implemented | `backend/app/middleware/safety.py`, `backend/app/services/safety_gateway.py`, `backend/app/ai/graph.py` | Rule/keyword-based medical and dangerous-content handling. |
| Vector retrieval | Implemented | `backend/app/services/retrieval.py` | pgvector cosine-distance retrieval. |
| Hybrid retrieval | Not implemented | `backend/app/services/retrieval.py` | No vector + keyword fusion/RRF/BM25 implementation. |
| `TSVECTOR` storage/indexing | Implemented infrastructure | `backend/app/models/document_chunk.py`, Alembic migration | Column and GIN index exist. |
| `TSVECTOR` automatic population | Not implemented / discrepancy | Alembic migration and model comment | Model comment states DB-trigger population, but no trigger exists in committed migrations. |
| Document-ingestion service | Implemented | `backend/app/services/ingestion.py` | URL/text-file loading, chunking, embeddings, persistence. |
| User-facing ingestion API/UI | Not implemented | `backend/app/api/v1`, `frontend/src` | No ingestion API route or document-management UI. |
| Workout plans | Not implemented | `docs/product_requirements.md`, `frontend/src/App.tsx` | Placeholder route only. |
| Progress tracking | Not implemented | `docs/product_requirements.md`, `frontend/src/App.tsx` | Placeholder route only. |
| Body-composition calculator | Not implemented | `docs/product_requirements.md`, `frontend/src/App.tsx` | No implementation identified. |
| CI workflow | Implemented | `.github/workflows/ci.yml` | Backend lint/type/test, frontend lint, Docker build/smoke workflow configured. |
| PostgreSQL test database | Implemented | `backend/tests/conftest.py` | Tests configure PostgreSQL and create the vector extension. |

## 5. Product Capability Findings

### 5.1 Authentication and Profile

**Implemented:**

- Email/password registration.
- Email/password login.
- JWT access and refresh tokens.
- Current-user backend endpoint.
- Persistent profile model.
- Profile retrieval and update endpoints.
- Frontend registration and login forms.

**Partial at product level:**

- The PRD calls for user-facing profile management, but no frontend profile management page is currently implemented.
- Google sign-in is not present in the current codebase.

**Confirmed defect:**

The frontend `authService.me()` calls `GET /api/v1/users/me`, while the backend exposes `GET /api/v1/auth/me`. The current frontend login and registration flows depend on `authService.me()`, so the frontend/backend contract is inconsistent.

### 5.2 Conversational AI Coach

The backend chat path has a real implementation:

1. Resolve or create a conversation.
2. Persist the user message.
3. Invoke LangGraph.
4. Persist the assistant response.
5. Return the response and citations.

The LangGraph implementation contains input safety, retrieval, generation, and output-safety stages.

However, the current end-to-end chat path is not contract-consistent.

**Confirmed defects/discrepancies:**

- Frontend calls `POST /api/v1/chat` while backend exposes `POST /api/v1/chat/message`.
- Frontend expects `response` to be a message object with fields such as `id`, `content`, and `created_at`; backend returns `response` as a string and exposes `message_id` separately.
- Frontend does not currently call the backend history endpoint.
- Frontend does not currently send its visible conversation history in `ChatRequest.history`.

The backend therefore contains conversation persistence infrastructure, but the current frontend does not yet provide a fully wired persistent conversational experience.

### 5.3 Plan Generation and Management

No implementation was identified for the PRD's plan-generation and plan-management requirements. Frontend routes currently render placeholders for `/plans`.

### 5.4 Progress Tracking

No implementation was identified for workout logging, streaks, body measurements, subjective feedback, or progress visualisation. The `/progress` route currently renders a placeholder.

### 5.5 Body Composition Calculator

No implementation was identified for the PRD's deterministic anthropometric estimator or historical tracking.

### 5.6 Knowledge and Source Attribution

The current RAG response path supports citations and document provenance fields. However, the repository does not currently provide the broader knowledge-management workflow described by the product requirements.

The current retrieval service is dense-vector-only.

### 5.7 Safety

The safety implementation is rule/keyword-based and exists in both HTTP middleware and the LangGraph pipeline. Medical content receives a disclaimer, while configured dangerous content is blocked/redacted.

The current implementation does not provide database-backed safety audit logging or a more sophisticated contextual classifier.

These are implementation boundaries, not automatically defects, unless a specific product or safety requirement makes them necessary.

## 6. Backend Findings

### 6.1 API Surface

The committed backend exposes:

```text
POST /api/v1/auth/register
POST /api/v1/auth/login
POST /api/v1/auth/refresh
GET  /api/v1/auth/me
POST /api/v1/auth/logout

GET  /api/v1/users/me/profile
PUT  /api/v1/users/me/profile
GET  /api/v1/users/{user_id}

POST /api/v1/chat/message
GET  /api/v1/chat/history/{conversation_id}
```

### 6.2 Database Access

The application uses both asynchronous and synchronous SQLAlchemy sessions:

- Async session/engine for FastAPI request handling.
- Synchronous session/engine for the synchronous LangGraph invocation and retrieval path.

This is an architectural characteristic of the current implementation. It should be monitored for correctness and operational complexity, but it is not by itself evidence of a defect.

### 6.3 Configuration

Configuration is managed through Pydantic Settings. The backend requires database/security configuration and at least one LLM path (`OLLAMA_BASE_URL` or `OPENAI_API_KEY`).

## 7. Database and RAG Findings

The database model/migration foundation contains:

- `users`
- `profiles`
- `conversations`
- `messages`
- `document_chunks`
- pgvector extension creation
- `vector(768)` embeddings
- HNSW vector index
- `TSVECTOR` column
- GIN full-text index

### TSVECTOR discrepancy

`backend/app/models/document_chunk.py` states that `content_tsv` is auto-populated by a DB trigger in migration. The committed Alembic migration contains the column and GIN index, but no trigger creation and no other trigger-related SQL.

Therefore the current repository should **not** be described as having a functioning automatically populated full-text-search field.

### RAG retrieval boundary

`backend/app/services/retrieval.py` performs pgvector cosine retrieval. No hybrid vector/keyword fusion or reranking was found in the committed retrieval implementation.

## 8. Frontend Findings

Implemented frontend areas include:

- Login.
- Registration.
- Protected routes.
- Dashboard.
- Chat UI.
- Auth state persistence through Zustand/local storage.
- API client with JWT request handling.
- Lazy route loading.
- PWA configuration.

Placeholder routes remain for:

- Plans.
- Progress.
- Exercise library.
- Settings.

The current frontend/backend contract inconsistencies in authentication and chat are the most important implementation issues found in the cross-check.

## 9. Testing and Quality Findings

The committed backend test fixture uses PostgreSQL through `asyncpg`, with `fitnessrag_test` as the default test database target and creation of the `vector` extension during test-database setup.

The ingestion unit/integration-style tests mock the database session and Ollama embedding calls; they do not establish a real PostgreSQL-backed ingestion integration test.

The frontend Cypress chat test uses MSW to mock the chat API. The test's mocked endpoint currently matches the frontend's `/api/v1/chat` path, not the backend's `/api/v1/chat/message` path. Consequently, the test does not verify the real frontend/backend API contract.

The repository also contains a confirmed test-environment configuration defect: the async test fixture and the synchronous LangGraph database session are configured to target different PostgreSQL databases. Current chat tests mock the graph invocation, so this disconnected path is not exercised. These are important to distinguish from ordinary failing tests.

## 10. CI and Repository Engineering State

The committed `.github/workflows/ci.yml` is configured to run:

- Backend linting/type checks.
- Backend tests.
- Frontend linting.
- Docker image builds.
- Docker Compose smoke setup.

The recovery work that preceded this assessment established the Alembic migration chain in version control and restored the intended formatting/type/test/CI baseline.

The current assessment does not claim a fresh green status check attached specifically to `98f5a10`; that status was not independently established during this assessment.

## 11. Confirmed Engineering Findings

The following findings are sufficiently supported to consider for engineering work:

### DEF-001 — Frontend/backend authentication contract mismatch

Frontend current-user lookup uses `/api/v1/users/me`, while backend exposes `/api/v1/auth/me`.

**Type:** Defect
**Evidence:** `frontend/src/services/authService.ts`, `frontend/src/pages/LoginPage.tsx`, `frontend/src/pages/RegisterPage.tsx`, `backend/app/api/v1/auth.py`

### DEF-002 — Frontend/backend chat contract mismatch

The frontend calls `/api/v1/chat` and expects a different response structure from the backend's `/api/v1/chat/message` response.

**Type:** Defect
**Evidence:** `frontend/src/services/chatService.ts`, `frontend/src/components/chat/ChatContainer.tsx`, `backend/app/api/v1/chat.py`, `backend/app/schemas/chat.py`

### DEF-003 — Chat persistence/history is not wired through the current UI

The backend persists messages and exposes a history endpoint, but the current ChatContainer neither loads history nor passes its visible history to the backend request.

**Type:** Defect / integration gap
**Evidence:** `frontend/src/components/chat/ChatContainer.tsx`, `frontend/src/services/chatService.ts`, `backend/app/api/v1/chat.py`, `backend/app/schemas/chat.py`

### DEF-004 — TSVECTOR population contract is inconsistent with the schema implementation

The model comment claims trigger-based automatic population, but no corresponding trigger exists in the committed Alembic migrations.

**Type:** Defect / data-model discrepancy
**Evidence:** `backend/app/models/document_chunk.py`, `backend/alembic/versions/ae2a53256191_initial_migration.py`

### TEST-002 — Synchronous and asynchronous test database configurations are disconnected

The test fixture creates its async test database engine from `TEST_DATABASE_URL` (falling back to `fitnessrag_test` with `postgres/postgres`), while the application settings loaded from `backend/.env.test` configure the synchronous SQLAlchemy session used by LangGraph with a different database (`test_db`) and credentials (`test_user/test_password`). The current chat tests mock `get_graph()`, so they do not exercise the real synchronous database path and therefore do not expose the mismatch.

**Type:** Test-environment defect / integration-coverage gap
**Evidence:** `backend/tests/conftest.py`, `backend/app/db/session.py`, `backend/.env.test`, `backend/tests/test_chat.py`

### TEST-001 — Frontend chat E2E test does not validate the production backend contract

The current Cypress/MSW test mocks `/api/v1/chat`, matching the frontend implementation rather than the backend's `/api/v1/chat/message` route and response contract.

**Type:** Test coverage gap
**Evidence:** `frontend/cypress/e2e/chat.cy.ts`, `frontend/src/mocks/handlers.ts`, `backend/app/api/v1/chat.py`, `backend/app/schemas/chat.py`

### PROD-001 — Profile UI is missing

The backend profile API exists, but the PRD requires user-facing profile management and the frontend does not implement it.

**Type:** Product capability gap
**Evidence:** `docs/product_requirements.md`, `backend/app/api/v1/users.py`, `frontend/src/App.tsx`

### PROD-002 — Workout plan capability is missing

No plan generation/management implementation was identified.

**Type:** Product capability gap
**Evidence:** `docs/product_requirements.md`, `frontend/src/App.tsx`

### PROD-003 — Progress tracking capability is missing

No workout/progress logging or progress visualisation implementation was identified.

**Type:** Product capability gap
**Evidence:** `docs/product_requirements.md`, `frontend/src/App.tsx`

### PROD-004 — Body composition calculator is missing

No deterministic anthropometric estimator or historical tracking implementation was identified.

**Type:** Product capability gap
**Evidence:** `docs/product_requirements.md`

### PROD-005 — User-facing document ingestion workflow is missing

The backend ingestion service exists, but no ingestion API route or document-management UI was identified.

**Type:** Product capability gap
**Evidence:** `backend/app/services/ingestion.py`, `backend/app/api/v1`, `frontend/src`

## 12. Findings Not Promoted to Issues Yet

The following observations were intentionally not promoted to current Issues solely because they are generic future engineering possibilities rather than confirmed product or implementation defects:

- Read replicas.
- Database partitioning.
- External secrets-management platforms.
- Chaos engineering.
- Mutation testing.
- Multi-modal AI.
- WebSocket real-time synchronization.
- External error-monitoring platforms.
- Large-scale database performance optimisation.

These may become relevant later, but they do not belong in the immediate backlog merely because they are absent today.

## 13. Historical Assessment Changes

Compared with the 2026-09-18 assessment:

- Alembic migration version control is now established in `main`.
- The backend formatting baseline was restored.
- The related test, MyPy, frontend CI, database-service, vector-extension, and Docker smoke issues uncovered during recovery were addressed through the recovery sequence.
- The current assessment corrects earlier uncertainty around profile endpoints: backend profile retrieval/update is implemented.
- The current assessment identifies frontend/backend contract mismatches that were not the focus of the recovery assessment.
- The current assessment confirms the PostgreSQL test-database setup rather than the AI-audit claim of SQLite-based testing.

## 14. Planning Baseline

The repository is now ready to move from current-state assessment into backlog recovery.

The next planning step should be to convert the **confirmed findings** above into GitHub Issues, classify them as defects, test-quality gaps, or product capability gaps, and then apply the Engineering Operating Model's Ready criteria and one-issue WIP limit.

No implementation work is implied by this document. It is a baseline for planning and acceptance decisions.
