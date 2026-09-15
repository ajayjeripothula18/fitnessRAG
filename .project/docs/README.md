# 🏋️ FitnessRAG — AI-Powered Fitness Coach

> An intelligent fitness coaching application powered by Retrieval-Augmented Generation (RAG), providing personalized workout plans, nutrition guidance, and progress tracking with safety-first AI design.

[![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-2088FF?logo=github-actions)](https://github.com/ajay/fitnessrag/actions)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?logo=fastapi)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18-61DAFB?logo=react)](https://react.dev)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791?logo=postgresql)](https://postgresql.org)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

---

## ✨ Features

### 🤖 AI Fitness Coach
- **Conversational AI** powered by RAG for evidence-based fitness and nutrition guidance
- **Source citations** on every response — know where advice comes from
- **Multi-turn conversations** with context awareness and user memory
- **Streaming responses** for real-time interaction

### 🛡️ Safety-First Design
- **Deterministic safety gateway** — medical queries get disclaimers, harmful content is blocked
- **Input & output validation** — dual-layer protection before and after LLM processing
- **Exercise contraindication checks** — prevents recommending unsafe exercises based on user profile
- **Full audit trail** — every safety decision is logged for review

### 📋 Personalized Workout Plans
- **AI-generated plans** tailored to your goals, equipment, and schedule
- **Curated templates** for quick-start routines
- **Plan versioning** — track modifications and rollback if needed
- **Chat-based modifications** — adjust your plan through natural conversation

### 📊 Progress Tracking
- **Body composition** — weight, measurements, body fat estimation (Navy method)
- **Workout logging** — track sets, reps, weight via chat or manual entry
- **Trend visualization** — charts showing progress over time
- **Statistics** — volume, frequency, and adherence metrics

### 📱 Mobile-First PWA
- **Progressive Web App** — install on any device
- **Responsive design** — optimized for gym use on mobile
- **Offline-capable** — static assets cached for fast access
- **Accessible** — WCAG 2.1 AA compliant

---

## 🏗️ Architecture

```
┌─────────────┐     ┌──────────────────────────────────────────┐
│  React PWA  │────▶│              FastAPI Backend              │
│  (Vite)     │     │                                          │
└─────────────┘     │  ┌────────┐  ┌──────────┐  ┌─────────┐  │
                    │  │ Safety  │  │ LangGraph│  │   RAG   │  │
                    │  │Gateway  │──│  Router  │──│Pipeline │  │
                    │  └────────┘  └──────────┘  └─────────┘  │
                    │                                          │
                    │  ┌──────────────────────────────────┐    │
                    │  │   PostgreSQL + pgvector           │    │
                    │  │   (App Data + Vectors + Audit)    │    │
                    │  └──────────────────────────────────┘    │
                    └──────────────────────────────────────────┘
                                       │
                              ┌────────┴────────┐
                              │  Ollama (Local)  │
                              │  Llama 3 8B      │
                              └─────────────────┘
```

### Key Technical Decisions
- **[ADR-001](docs/adr/001-tech-stack-selection.md)**: FastAPI + React + PostgreSQL — balanced for AI workloads and portfolio value
- **[ADR-002](docs/adr/002-ai-architecture.md)**: LangGraph orchestration with deterministic safety gateway
- **[ADR-003](docs/adr/003-data-architecture.md)**: Unified PostgreSQL with pgvector — single DB for app data, vectors, and audit

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 20 LTS
- Docker & Docker Compose
- Ollama (for local LLM)

### Setup

```bash
# Clone and configure
git clone https://github.com/ajay/fitnessrag.git
cd fitnessrag
cp .env.example .env

# Start database
docker compose up -d db

# Backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
alembic upgrade head

# Frontend
cd frontend && npm install

# Start development
# Terminal 1: uvicorn src.main:app --reload --port 8000
# Terminal 2: cd frontend && npm run dev

# (Optional) Local LLM
ollama pull llama3:8b && ollama serve
```

**Verify**: Open http://localhost:5173 (frontend) or http://localhost:8000/docs (API docs)

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [Product Requirements](docs/product_requirements.md) | MVP scope, user stories, and boundaries |
| [Technical Design](docs/technical_design.md) | Component architecture, LangGraph state design |
| [Database Design](docs/database_design.md) | Schema, indexes, and migration strategy |
| [API Contracts](docs/api_contracts.md) | All endpoints with request/response schemas |
| [Safety Gateway Spec](docs/safety_gateway_spec.md) | Safety classification and audit system |
| [Testing Strategy](docs/testing_strategy.md) | Test pyramid, CI/CD pipeline, coverage targets |
| [User Flows](docs/user_flows.md) | User journeys and wireframes |
| [Architecture Document](architecture_document.md) | Executive summary of all decisions |
| [Contributing Guide](CONTRIBUTING.md) | Developer setup and coding standards |

### Agile Artifacts
| Document | Description |
|----------|-------------|
| [Product Backlog](docs/agile/product_backlog.md) | Prioritized user stories with story points |
| [Definition of Done](docs/agile/definition_of_done.md) | Quality criteria at story, sprint, and release levels |
| [Sprint 1 Plan](docs/agile/sprint_1_plan.md) | "Walking Skeleton" — auth, chat, safety, RAG |
| [Sprint 2 Plan](docs/agile/sprint_2_plan.md) | "Feature Complete MVP" — plans, tracking, polish |

---

## 🧪 Testing

```bash
# Backend tests
pytest                           # All tests
pytest tests/safety/ -v          # Safety tests (mandatory)
pytest --cov=src --cov-report=html  # With coverage

# Frontend tests
cd frontend && npm test

# Security scan
bandit -r src/ -ll
pip-audit
```

**Coverage Target**: ≥ 70% overall, ≥ 95% for safety gateway

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | FastAPI, Python 3.11+, SQLAlchemy 2.0, Alembic |
| **AI/ML** | LangGraph, LangChain, Ollama, BGE-small-en-v1.5, Detoxify |
| **Database** | PostgreSQL 16, pgvector |
| **Frontend** | React 18, TypeScript, Vite, TanStack Query, Zustand |
| **DevOps** | Docker, GitHub Actions, structlog, Sentry |

---

## 📄 License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgments

- Built with evidence-based fitness knowledge from WHO, ACE, ACSM, and NSCA guidelines
- AI safety patterns inspired by responsible AI frameworks
- Designed following Agile best practices with industry-standard documentation

---

*Built by [Ajay](https://github.com/ajay) — Demonstrating full-stack AI engineering with responsible design.*
