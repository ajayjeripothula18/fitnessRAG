# Sprint 1 Tracker — "Walking Skeleton"

**Sprint Goal:** Authenticated users can have safe, personalized fitness conversations backed by RAG with source citations, in a mobile-first PWA shell.
**Start Date:** 2026-08-31
**End Date:** 2026-09-07

## TODO (Sprint Backlog)

### Checkpoint 1: 🏗️ Vikram (DevOps/QA) - Scaffolding & Infrastructure
- [x] INFRA-01: Project scaffolding (FastAPI + React/Vite + Docker Compose)
- [x] INFRA-02: CI/CD pipeline (GitHub Actions: lint, test, build)
- [x] INFRA-03: Database setup (PostgreSQL + pgvector + Alembic)

### Checkpoint 2: ⚙️ Meera (Backend) - Core API & Auth
- [x] US-101: User registration endpoint & schema
- [x] US-102: User login & JWT authentication
- [x] US-105: User logout endpoint
- [x] US-104: Profile view and edit API
- [x] US-301: Safety gateway — input classification middleware
- [x] US-302: Medical disclaimer responses
- [x] US-303: Output safety validation

### Checkpoint 3: 🎨 Zara (Frontend) - PWA Shell & Navigation
- [x] US-701: React/Vite PWA shell setup
- [x] US-702: App navigation & layout
- [x] US-703: Mobile-first responsive design & accessibility

### Checkpoint 4: 🧠 Ravi (Tech Lead) - AI & Knowledge Retrieval
- [x] US-601: Knowledge ingestion pipeline (parsing & chunking)
- [x] US-602: Hybrid search implementation (vector + lexical)
- [x] US-603: Source attribution in responses
- [x] US-201: LangGraph conversational AI coach orchestration
- [x] US-202: Conversation state persistence

### Integration & Polish
- [x] End-to-end integration testing & verification

## IN PROGRESS
- [ ] 

## REVIEW / VALIDATE (Testing Phase)
- [ ] 

## DONE
- [x] Checkpoint 1: Vikram (DevOps/QA) - Scaffolding & Infrastructure completed
- [x] Checkpoint 2: Meera (Backend) - Core API & Auth completed
- [x] Checkpoint 3: Zara (Frontend) - PWA Shell & Navigation completed
- [x] Checkpoint 4: Ravi (Tech Lead) - AI & Knowledge Retrieval completed

---
*Note for AI Agents: Execute one persona checkpoint at a time. Move items to IN PROGRESS when active, and to DONE upon successful validation.*
