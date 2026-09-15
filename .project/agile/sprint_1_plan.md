# FitnessRAG — Sprint 1 Plan: "Walking Skeleton"
## Created by Karan (BA/Scrum Master)
## Last Updated: 2026-08-31

---

## Sprint Overview

| Field | Value |
|-------|-------|
| **Sprint Number** | 1 |
| **Sprint Name** | Walking Skeleton |
| **Duration** | 1 Week (7 days) |
| **Sprint Goal** | Authenticated users can have safe, personalized fitness conversations backed by RAG with source citations, in a mobile-first PWA shell |
| **Team Velocity** | ~57 SP (estimated — first sprint, no historical data) |
| **Capacity** | Full team × 7 days = 35 person-days |

---

## Sprint Goal Validation

> **Done when**: A user can sign up, log in, complete their profile, ask a fitness question, receive a safety-checked RAG response with source citations, and use it on a mobile device as a PWA.

This is a **vertical slice** — touching every layer from frontend to database to AI pipeline.

---

## Sprint Backlog

### Day 1-2: Foundation Layer

| Story | Owner | SP | Dependencies | Day |
|-------|-------|-----|-------------|-----|
| **INFRA-01**: Project scaffolding (FastAPI + Vite/React + Docker) | Ravi + Vikram | - | None | D1 |
| **INFRA-02**: CI/CD pipeline (GitHub Actions: lint, test, build) | Vikram | - | INFRA-01 | D1 |
| **INFRA-03**: Database setup (PostgreSQL + pgvector + Alembic) | Meera | - | INFRA-01 | D1 |
| US-101: User registration | Meera | 3 | INFRA-03 | D1-D2 |
| US-102: User login (JWT) | Meera | 2 | US-101 | D2 |
| US-105: User logout | Meera | 1 | US-102 | D2 |
| US-104: Profile view/edit | Meera + Zara | 3 | US-102 | D2-D3 |

### Day 2-4: AI & Knowledge Layer

| Story | Owner | SP | Dependencies | Day |
|-------|-------|-----|-------------|-----|
| US-601: Knowledge ingestion pipeline | Ravi | 5 | INFRA-03 | D2-D3 |
| US-602: Hybrid search (vector + lexical) | Ravi | 5 | US-601 | D3-D4 |
| US-603: Source attribution in responses | Ravi | 2 | US-602 | D4 |
| US-301: Safety gateway — input classification | Meera + Vikram | 5 | INFRA-01 | D2-D3 |
| US-302: Medical disclaimer responses | Meera | 3 | US-301 | D3-D4 |
| US-303: Output safety validation | Meera | 3 | US-301 | D4 |

### Day 3-5: Chat Interface Layer

| Story | Owner | SP | Dependencies | Day |
|-------|-------|-----|-------------|-----|
| US-201: Conversational AI coach | Ravi + Meera | 8 | US-301, US-602 | D3-D5 |
| US-202: Conversation persistence | Meera | 3 | US-201 | D5 |
| US-701: PWA shell | Zara | 5 | INFRA-01 | D2-D4 |
| US-702: App navigation | Zara | 3 | US-701 | D4-D5 |
| US-703: Accessibility compliance | Zara | 3 | US-702 | D5-D6 |

### Day 6-7: Integration & Polish

| Task | Owner | Day |
|------|-------|-----|
| End-to-end integration testing | Vikram + All | D6 |
| Performance testing (API latency, Lighthouse) | Vikram | D6 |
| Safety gateway spike — edge case testing | Vikram + Meera | D6 |
| Bug fixes and polish | All | D7 |
| Sprint demo preparation | Karan | D7 |
| Sprint review + retrospective | All | D7 |

---

## Story Dependency Graph

```
INFRA-01 (Scaffolding)
├── INFRA-02 (CI/CD)
├── INFRA-03 (Database)
│   ├── US-101 (Registration)
│   │   └── US-102 (Login/JWT)
│   │       ├── US-105 (Logout)
│   │       └── US-104 (Profile)
│   └── US-601 (Knowledge Ingestion)
│       └── US-602 (Hybrid Search)
│           └── US-603 (Source Citations)
├── US-301 (Safety Input Classification)
│   ├── US-302 (Medical Disclaimers)
│   ├── US-303 (Output Validation)
│   └── US-201 (AI Coach) ← also depends on US-602
│       └── US-202 (Conversation Persistence)
└── US-701 (PWA Shell)
    └── US-702 (Navigation)
        └── US-703 (Accessibility)
```

---

## Technical Spikes (10% Budget)

| Spike | Owner | Time Box | Question |
|-------|-------|----------|----------|
| SP-01: Ollama model latency benchmarking | Ravi | 4 hours | Is 8B model fast enough for <5s p95? Do we need streaming fallback from day 1? |
| SP-02: pgvector IVFFlat vs HNSW performance | Meera | 2 hours | Which index type gives better recall/latency for our expected data size (1k-10k chunks)? |
| SP-03: LangGraph state management validation | Ravi | 3 hours | Validate the planned graph state design handles multi-turn conversations with safety checkpoints |

---

## Risks & Mitigations

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| LLM latency exceeds 5s target | High | High | Implement streaming from Day 1; have provider-agnostic interface to swap models |
| Knowledge base quality issues | Medium | High | Start with 3-5 high-quality sources; add validation step in ingestion pipeline |
| Integration complexity between safety gateway + RAG + chat | Medium | High | Build safety gateway as middleware (independent of RAG); integration test early (Day 4) |
| Sprint overcommitment (first sprint, no velocity data) | Medium | Medium | Identify flex stories (US-703 accessibility can slip to S2 if needed); daily standup monitoring |

---

## Daily Standup Schedule

| Day | Focus | Key Check |
|-----|-------|-----------|
| D1 | Scaffolding kickoff | Is the project structure ready? Docker Compose running? |
| D2 | Auth + Pipeline starts | Can we register/login? Is ingestion pipeline running? |
| D3 | Safety + Search | Is safety gateway classifying inputs? Vector search returning results? |
| D4 | Integration begins | Can we send a question through safety → RAG → LLM → safety → response? |
| D5 | Chat UI + Polish | Is the full user flow working E2E in the browser? |
| D6 | Testing + Fixes | Are all acceptance criteria verified? Performance targets met? |
| D7 | Demo + Retro | Sprint review ready? Retrospective insights captured? |

---

## Sprint 1 Success Criteria

**The sprint is successful if:**
1. ✅ A new user can sign up, log in, and set up their fitness profile
2. ✅ User can ask a fitness question and receive a RAG-powered response
3. ✅ Safety gateway blocks medical advice requests with appropriate disclaimers
4. ✅ Responses include source citations from the knowledge base
5. ✅ The entire flow works in a mobile-first PWA
6. ✅ Code coverage ≥ 70% across all new code
7. ✅ CI/CD pipeline passing on main branch
8. ✅ No critical security findings in static analysis
