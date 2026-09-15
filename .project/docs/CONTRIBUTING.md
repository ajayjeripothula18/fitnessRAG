# Contributing to FitnessRAG

## Created by Ravi (Tech Lead)
## Last Updated: 2026-08-31

Welcome to FitnessRAG! This guide covers everything you need to get started as a contributor.

---

## 🚀 Quick Start

### Prerequisites
- **Python 3.11+** — Backend runtime
- **Node.js 20 LTS** — Frontend runtime
- **Docker & Docker Compose** — Development environment
- **Ollama** — Local LLM inference (optional for frontend-only work)
- **Git** — Version control

### Setup

```bash
# 1. Clone the repository
git clone https://github.com/ajay/fitnessrag.git
cd fitnessrag

# 2. Copy environment configuration
cp .env.example .env
# Edit .env with your local settings

# 3. Start infrastructure (PostgreSQL + pgvector)
docker compose up -d db

# 4. Backend setup
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
pip install -r requirements.txt -r requirements-dev.txt

# 5. Run database migrations
alembic upgrade head

# 6. Seed knowledge base (optional)
python scripts/seed_knowledge.py

# 7. Frontend setup
cd frontend
npm install

# 8. Start development servers
# Terminal 1: Backend
uvicorn src.main:app --reload --port 8000

# Terminal 2: Frontend
cd frontend && npm run dev

# 9. (Optional) Start Ollama for local LLM
ollama pull llama3:8b
ollama serve
```

### Verify Setup
- **Backend API**: http://localhost:8000/docs (Swagger UI)
- **Frontend**: http://localhost:5173
- **Health Check**: `curl http://localhost:8000/api/v1/health`

---

## 📁 Project Structure

```
fitnessrag/
├── src/                          # Backend source code
│   ├── api/                      # FastAPI route handlers
│   │   ├── v1/                   # API version 1
│   │   │   ├── auth.py
│   │   │   ├── chat.py
│   │   │   ├── plans.py
│   │   │   ├── profile.py
│   │   │   └── tracking.py
│   │   └── dependencies.py       # Shared dependencies (auth, db session)
│   ├── core/                     # Core configuration
│   │   ├── config.py             # Settings (from env vars)
│   │   ├── security.py           # JWT + password hashing
│   │   └── logging.py            # Structured logging setup
│   ├── db/                       # Database layer
│   │   ├── models/               # SQLAlchemy models
│   │   ├── repositories/         # Data access layer
│   │   └── session.py            # DB session management
│   ├── services/                 # Business logic
│   │   ├── auth_service.py
│   │   ├── chat_service.py
│   │   ├── plan_service.py
│   │   ├── profile_service.py
│   │   └── tracking_service.py
│   ├── ai/                       # AI/ML components
│   │   ├── graph/                # LangGraph conversation graph
│   │   ├── rag/                  # RAG pipeline (ingest, search, retrieve)
│   │   ├── safety/               # Safety gateway
│   │   └── providers/            # LLM provider interface
│   └── main.py                   # FastAPI application entry
├── frontend/                     # React frontend
│   ├── src/
│   │   ├── components/           # Reusable UI components
│   │   ├── pages/                # Page-level components
│   │   ├── hooks/                # Custom React hooks
│   │   ├── services/             # API client
│   │   ├── stores/               # Zustand state stores
│   │   └── App.tsx               # Root component
│   └── vite.config.ts
├── tests/                        # Test suite
│   ├── unit/                     # Unit tests
│   ├── integration/              # Integration tests
│   ├── safety/                   # Safety-specific tests
│   ├── e2e/                      # End-to-end tests
│   └── conftest.py               # Shared fixtures
├── alembic/                      # Database migrations
├── docs/                         # Documentation
│   ├── agile/                    # Agile artifacts
│   ├── adr/                      # Architecture Decision Records
│   └── ...
├── scripts/                      # Utility scripts
├── docker-compose.yml
├── Dockerfile
├── .env.example
└── README.md
```

---

## 🔀 Git Workflow

### Branch Naming
```
feature/US-{ID}-{short-description}   # Feature branches
bugfix/US-{ID}-{short-description}    # Bug fixes
hotfix/{description}                   # Production hotfixes
spike/SP-{ID}-{description}           # Technical spikes
```

**Examples:**
- `feature/US-101-user-registration`
- `bugfix/US-301-safety-false-positive`
- `spike/SP-01-ollama-latency`

### Commit Messages
Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Types:** `feat`, `fix`, `docs`, `test`, `refactor`, `perf`, `chore`, `ci`

**Examples:**
```
feat(auth): implement user registration with email validation
fix(safety): reduce false positives for supplement queries
test(rag): add integration tests for hybrid search
docs(adr): add ADR-004 for caching strategy
refactor(chat): extract message formatting to utility
```

### Pull Request Process

1. **Create branch** from `main`
2. **Implement** changes following DoD
3. **Self-review** using the PR checklist below
4. **Open PR** with description template
5. **Pass CI** — all checks must be green
6. **Code review** — minimum 1 approval
7. **Merge** via squash merge

### PR Description Template
```markdown
## What
Brief description of what this PR does.

## Why
Context on why this change is needed. Link to user story.

## How
Key implementation decisions and approach.

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated (if API changes)
- [ ] Safety tests pass (if AI-related)
- [ ] Manual testing done

## Screenshots/Recordings
(If UI changes)

## Checklist
- [ ] Code follows project style guidelines
- [ ] Docstrings on all public functions
- [ ] No hardcoded secrets or debug code
- [ ] Migrations are reversible
- [ ] API documentation updated (auto-generated)
```

---

## 📏 Coding Standards

### Python (Backend)

- **Style**: PEP 8 (enforced by Ruff)
- **Formatter**: Ruff format
- **Type Hints**: Required on all public functions
- **Docstrings**: Google-style on all public functions/classes
- **Imports**: Sorted by Ruff (isort-compatible)

```python
# Good
async def create_user(
    email: str,
    password: str,
    full_name: str,
) -> User:
    """Create a new user account.
    
    Args:
        email: User's email address (must be unique).
        password: Plain text password (will be hashed).
        full_name: User's display name.
    
    Returns:
        The created User model instance.
    
    Raises:
        DuplicateEmailError: If email already exists.
        ValidationError: If input validation fails.
    """
    ...
```

### TypeScript (Frontend)

- **Style**: ESLint + Prettier
- **Components**: Functional components with TypeScript interfaces
- **Naming**: PascalCase for components, camelCase for functions/variables
- **Props**: Explicit interface (not inline types)

```typescript
// Good
interface ChatMessageProps {
  message: Message;
  isStreaming: boolean;
  onRetry?: () => void;
}

export function ChatMessage({ message, isStreaming, onRetry }: ChatMessageProps) {
  // ...
}
```

### SQL/Migrations

- **Table names**: snake_case, plural (`users`, `workout_logs`)
- **Column names**: snake_case (`created_at`, `user_id`)
- **Migrations**: Always include `downgrade()` function
- **Indexes**: Named explicitly (`ix_users_email`, `ix_messages_conversation_id`)

---

## 🧪 Testing Guide

### Run Tests

```bash
# All backend tests
pytest

# Specific test suite
pytest tests/unit/
pytest tests/integration/
pytest tests/safety/

# With coverage
pytest --cov=src --cov-report=html

# Frontend tests
cd frontend && npm test

# Watch mode (development)
pytest --watch
cd frontend && npm run test:watch
```

### Writing Tests

- Test file mirrors source: `src/services/auth_service.py` → `tests/unit/services/test_auth_service.py`
- Use descriptive test names: `test_login_with_invalid_password_returns_401`
- One assertion per test when possible
- Use fixtures for shared setup
- Mock external dependencies in unit tests

---

## 🔐 Security Guidelines

1. **Never commit secrets** — Use `.env` files (in `.gitignore`)
2. **Validate all inputs** — Pydantic models for every API endpoint
3. **Parameterized queries** — Always use ORM or parameterized SQL
4. **Auth on every endpoint** — Except explicitly public routes
5. **No `eval()` or `exec()`** — Ever
6. **Pin dependencies** — Exact versions in `requirements.txt`
7. **Run security scans** — `bandit` and `pip-audit` before every PR

---

## 📖 Documentation

### When to Write Documentation
- New API endpoint → Auto-documented via FastAPI (add docstrings to route functions)
- Architectural decision → Create ADR in `docs/adr/`
- New environment variable → Add to `.env.example` with comment
- New script or tool → Add to README or relevant doc
- Complex business logic → Inline comments explaining "why" (not "what")

### ADR Format
Use the template in `docs/adr/` — every significant technical decision gets an ADR.

---

## 🆘 Getting Help

- **Check existing docs**: Start with `docs/` directory and README
- **Search issues**: Look for similar problems in GitHub Issues
- **Ask questions**: Open a Discussion or comment on the relevant Issue
- **Architecture questions**: Reference ADRs in `docs/adr/`

---

## 📋 Definition of Done

Before marking any work as complete, verify against the [Definition of Done](docs/agile/definition_of_done.md) checklist. Safety-related criteria are **never** exempt.
