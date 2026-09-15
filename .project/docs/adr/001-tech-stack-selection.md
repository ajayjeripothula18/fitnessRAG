# ADR-001: Technology Stack Selection
## Created by Arjun (CTO)
## Status: Accepted
## Date: 2026-08-31

---

## Context

FitnessRAG is a portfolio-grade AI fitness coaching application with the following constraints:
- **Budget**: $0/month operating cost (free tiers only)
- **Timeline**: 2-week MVP (two 1-week sprints)
- **Team**: Solo developer (Ajay) with AI development assistance
- **Requirements**: RAG-based conversational AI, workout planning, progress tracking, PWA

We need to select a technology stack that balances developer productivity, portfolio impressiveness, and operational cost.

## Decision

### Backend
| Component | Choice | Rationale |
|-----------|--------|-----------|
| **Framework** | FastAPI (Python 3.11+) | Async-native, auto-generated OpenAPI docs, Pydantic validation, excellent for AI/ML integration |
| **ORM** | SQLAlchemy 2.0 (async) | Industry-standard, async support, well-documented, Alembic migrations |
| **Auth** | python-jose (JWT) + passlib (bcrypt) | Lightweight, no external auth service needed, $0 cost |
| **AI Orchestration** | LangGraph | Stateful multi-step AI workflows, built on LangChain, graph-based conversation routing |

### Database
| Component | Choice | Rationale |
|-----------|--------|-----------|
| **Primary DB** | PostgreSQL 16 | Robust, free-tier available (Supabase/Neon), pgvector for unified vector storage |
| **Vector Store** | pgvector (extension) | Eliminates separate vector DB cost, embedded in PostgreSQL, sufficient for our scale |
| **Migrations** | Alembic | De-facto standard for SQLAlchemy, reversible migrations |

### AI/ML
| Component | Choice | Rationale |
|-----------|--------|-----------|
| **LLM** | Ollama (local) / Provider-agnostic interface | $0 cost for local development, abstracted so we can swap to API providers later |
| **Default Model** | Llama 3 8B (or equivalent) | Good quality for 8B params, runs locally on consumer hardware |
| **Embeddings** | BGE-small-en-v1.5 (384d) | Lightweight, good quality, small vector size reduces storage |
| **Safety** | Detoxify (unbiased-small) + rule-based | Local inference, no API cost, deterministic rules as primary layer |

### Frontend
| Component | Choice | Rationale |
|-----------|--------|-----------|
| **Framework** | React 18 + TypeScript | Industry standard, excellent ecosystem, portfolio-credible |
| **Build Tool** | Vite | Fast HMR, optimized builds, modern defaults |
| **State Management** | TanStack Query (server state) + Zustand (client state) | TanStack for API caching/sync, Zustand for lightweight UI state |
| **Styling** | CSS Modules + CSS Custom Properties | No framework lock-in, performant, full control |
| **Charts** | Recharts | React-native, lightweight, sufficient for progress visualization |
| **PWA** | Vite PWA plugin | Easy PWA setup with workbox |

### DevOps
| Component | Choice | Rationale |
|-----------|--------|-----------|
| **CI/CD** | GitHub Actions | Free for public repos, well-integrated |
| **Containerization** | Docker (multi-stage) | Consistent environments, easy deployment |
| **Hosting** | Render (free tier) or Railway | Free tier available, Docker support |
| **Logging** | structlog (Python) | Structured JSON logs, easy to query |
| **Monitoring** | Sentry (free tier) | Error tracking, performance monitoring |

## Alternatives Considered

### Backend
- **Django REST Framework**: Heavier, batteries-included but slower for AI workloads. FastAPI's async nature is better for streaming LLM responses.
- **Express.js (Node)**: Good for frontend developers, but Python ecosystem is superior for AI/ML tooling (LangChain, Detoxify, sentence-transformers).
- **Go (Gin/Fiber)**: Excellent performance but limited AI/ML library ecosystem.

### Database
- **MongoDB + Pinecone**: Separate vector DB adds cost complexity; pgvector unifies storage in one free-tier database.
- **SQLite + ChromaDB**: Simpler but not production-grade; no concurrent access; difficult to deploy.
- **Supabase (managed)**: Considered as PostgreSQL provider — free tier includes pgvector, auth, and realtime. Strong contender for hosting.

### Frontend
- **Next.js**: SSR/SSG overhead unnecessary for a SPA that's primarily a PWA. Added complexity without clear benefit.
- **Svelte/SvelteKit**: Less ecosystem support, fewer portfolio evaluators familiar with it.
- **Vue.js**: Viable alternative but React has wider recognition in the job market.

## Consequences

### Positive
- Python unifies backend + AI/ML code (no language switching)
- pgvector eliminates a separate vector DB service and cost
- FastAPI auto-generates API documentation (portfolio-ready)
- React + TypeScript is the most recognized frontend stack by hiring managers
- Entire stack runs locally for development ($0 cost)

### Negative
- Python is slower than Go/Rust for pure API performance (mitigated by async)
- pgvector may need tuning for large-scale vector search (acceptable at MVP scale)
- Ollama local inference requires decent hardware (mitigated by provider-agnostic interface)
- Multiple Python dependencies increase container size (mitigated by multi-stage Docker builds)

### Risks
- **LLM latency**: 8B models may be slow locally → Implement streaming from day 1
- **pgvector scaling**: IVFFlat index may underperform → Monitor and plan HNSW migration
- **Free tier limits**: Render/Supabase free tiers have limits → Design for efficiency

## References
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [pgvector GitHub](https://github.com/pgvector/pgvector)
- Architecture Document: `/architecture_document.md`
- Technical Design: `/docs/technical_design.md`
