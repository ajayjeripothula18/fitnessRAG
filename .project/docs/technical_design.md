# FitnessRAG Technical Design Document
# Created by Arjun (CTO)

## Overview
This document outlines the technical architecture, design decisions, and implementation details for the FitnessRAG platform. It synthesizes research on FastAPI, LangGraph, pgvector, Ollama, and system design principles to create a scalable, maintainable, and secure foundation.

## System Architecture

### High-Level Components
```
+------------------+      +------------------+      +------------------+
|   Frontend (PWA) | <--> |   API Gateway    | <--> |   Backend Services|
|   (React/Vite)   |      |   (FastAPI)      |      |   (Python)       |
+------------------+      +------------------+      +------------------+
         ^                         ^                         ^
         |                         |                         |
+------------------+      +------------------+      +------------------+
|   CDN/Static     |      |   Auth Service   |      |   AI Service     |
|   Assets         |      |   (OAuth2/JWT)   |      |   (LangGraph)    |
+------------------+      +------------------+      +------------------+
         ^                         ^                         ^
         |                         |                         |
+------------------+      +------------------+      +------------------+
|   Database       | <--> |   Vector Store   | <--> |   Knowledge    |
|   (PostgreSQL)   |      |   (pgvector)     |      |   Base         |
+------------------+      +------------------+      +------------------+
```

### Core Architectural Decisions

#### 1. Technology Stack Rationale
- **Backend**: FastAPI for high performance, async support, automatic docs, and Python ecosystem
- **AI Orchestration**: LangGraph for stateful workflows with persistence and human-in-the-loop capabilities
- **Database**: PostgreSQL with pgvector extension for unified relational + vector storage
- **LLM Provider**: Ollama for local development with abstraction layer for provider independence
- **Frontend**: React with Vite for fast development, Tailwind CSS for styling
- **Deployment**: Docker containers for consistency and portability

#### 2. Separation of Concerns
- **Presentation Layer**: Handles UI rendering, user interactions, client-side state
- **API Layer**: RESTful endpoints with versioning, authentication, request/response validation
- **Service Layer**: Business logic orchestration, external service integration
- **Data Layer**: Database operations, repository patterns, transaction management
- **AI Layer**: LangGraph workflows, LLM interactions, tool usage, validation
- **Infrastructure**: Containerization, CI/CD, monitoring, logging

#### 3. Safety-First Design
- Safety gateway as a pre-processing step for all user inputs
- Deterministic validation of AI-generated outputs
- Clear escalation paths for medical/harmful content
- Audit logging of all safety decisions

## Detailed Component Design

### Backend Services (FastAPI)

#### Project Structure
```
app/
├── api/
│   └── v1/
│       ├── auth.py           # Authentication endpoints
│       ├── users.py          # User management
│       ├── profiles.py       # Profile CRUD
│       ├── plans.py          # Plan management
│       ├── chat.py           # Conversational AI endpoints
│       ├── progress.py       # Progress tracking
│       └── health.py         # Health check endpoints
├── core/
│   ├── config.py             # Environment configuration
│   ├── security.py           # Auth utilities, password hashing
│   ├── dependencies.py       # Dependency injection providers
│   └── exceptions.py         # Custom exception handlers
├── models/
│   ├── user.py               # SQLAlchemy User model
│   ├── profile.py            # Profile model
│   ├── plan.py               # Plan model
│   ├── plan_version.py       # Plan versioning
│   ├── workout.py            # Workout model
│   ├── workout_log.py        # Workout logs
│   ├── measurement.py        # Body measurements
│   └── exercise.py           # Exercise library
├── schemas/
│   ├── auth.py               # Auth request/response schemas
│   ├── user.py               # User schemas
│   ├── profile.py            # Profile schemas
│   ├── plan.py               # Plan schemas
│   ├── chat.py               # Chat request/response schemas
│   └── progress.py           # Progress schemas
├── services/
│   ├── auth_service.py       # Authentication logic
│   ├── user_service.py       # User management
│   ├── profile_service.py    # Profile operations
│   ├── plan_service.py       # Plan generation/modification
│   ├── workout_service.py    # Workout operations
│   ├── progress_service.py   # Progress tracking
│   ├── llm_service.py        # LLM provider abstraction
│   ├── rag_service.py        # Retrieval augmented generation
│   ├── safety_service.py     # Safety gateway implementation
│   └── llm_provider.py       # Provider-specific implementations
├── utils/
│   ├── database.py           # Database connection, session management
│   ├── logging.py            # Structured logging configuration
│   └── helpers.py            # Utility functions
├── migrations/               # Alembic migration scripts
└── main.py                   # Application entry point
```

#### Key Implementation Details

##### Async/Await Pattern
- All I/O operations use async/await (database queries, HTTP requests, file operations)
- Database driver: asyncpg for full PostgreSQL async support
- External API calls: httpx.AsyncClient
- Background tasks: FastAPI BackgroundTasks for non-critical operations

##### Dependency Injection
- FastAPI's built-in DI system for:
  - Database sessions
  - Service instances
  - Configuration objects
  - External clients (LLM, vector store)
- Providers defined in `core/dependencies.py`
- Automatic lifecycle management

##### Validation & Serialization
- Pydantic v2 for all request/response models
- Field-level validation (ranges, formats, constraints)
- Custom validators for complex business rules
- Response model exclusion to prevent sensitive data leakage
- Examples included for OpenAPI documentation

##### Security Implementation
- Authentication: OAuth2 with JWT (access token 15min, refresh token 7 days)
- Password hashing: bcrypt via passlib
- Rate limiting: slowapi on auth endpoints (5 attempts/minute)
- Security headers middleware: CSP, HSTS, X-Frame-Options, etc.
- CORS: Restrictive configuration based on environment
- Input sanitization: Validation at API boundary
- Secrets management: Environment variables via pydantic-settings

##### Logging & Observability
- Structured logging with structlog (JSON format)
- Correlation IDs for request tracing
- Performance middleware: request timing, slow query logging
- Health endpoints: `/health/live` (liveness), `/health/ready` (readiness)
- Metrics endpoint: Prometheus format at `/metrics`

### AI Architecture (LangGraph + LLM)

#### State Design
```python
from typing import TypedDict, Annotated, List, Optional, Dict
from langchain_core.messages import BaseMessage

class FitnessAgentState(TypedDict):
    messages: Annotated[List[BaseMessage], "Conversation messages"]
    user_profile: Optional[Dict]  # Structured profile data
    active_plan: Optional[Dict]   # Current plan details
    progress_data: Optional[Dict] # Recent measurements
    user_memory: Optional[Dict]   # Persistent preferences/facts
    safety_result: Optional[Dict] # Safety gateway output
    rag_context: Optional[List[Dict]] # Retrieved knowledge
    tool_calls: PendingToolExecutions  # Pending tool invocations
    response: Optional[str]       # Final user response
    error: Optional[str]          # Error state if any
```

#### Workflow Nodes

1. **Input Validation Node**
   - Sanitizes input, checks length, basic profanity
   - Returns validated input or error state

2. **Safety Gateway Node**
   - Rule-based medical content detection
   - Toxicity/harmful content scanning (Detoxify)
   - Fitness-specific contraindication checking
   - Returns SAFE, MEDICAL_CONSULTATION_REQUIRED, HARMFUL_CONTENT, or OUT_OF_SCOPE

3. **Intent Classification Node**
   - Determines if RAG needed, tool use required, or direct response
   - Based on query patterns and state analysis

4. **Tool Execution Node** (Conditional)
   - Executes required tools: get_profile, search_knowledge, get_plan, etc.
   - Updates state with tool results

5. **RAG Retrieval Node** (Conditional)
   - Hybrid search: vector similarity + lexical (BM25/ts_rank)
   - Metadata filtering applied before vector search
   - Reranking with CrossEncoder for relevance
   - Returns top-k relevant chunks with source metadata

6. **LLM Generation Node**
   - Constructs prompt from state: user context + retrieved knowledge + chat history
   - Uses LLM with streaming capability for better UX
   - Supports structured output (JSON mode) when available
   - Implements timeout and retry mechanisms

7. **Validation & Formatting Node**
   - Validates LLM output against expected formats
   - Applies deterministic rules (exercise validity, intensity constraints)
   - Adds source citations and disclaimers
   - Formats final response

8. **Response Node**
   - Returns final state with response ready for user

#### Persistence Strategy
- **Development**: MemorySaver for rapid iteration
- **Production**: PostgresSaver for persistent conversation state
- **TTL Implementation**: Automatic cleanup of old conversations (>30 days)
- **State Minimization**: Only essential data persisted to reduce storage

#### LLM Provider Abstraction
```python
from abc import ABC, abstractmethod

class LLMProvider(ABC):
    @abstractmethod
    async def generate(self, prompt: str, **kwargs) -> str:
        pass
    
    @abstractmethod
    async def generate_structured(self, prompt: str, schema: Dict, **kwargs) -> Dict:
        pass

class OllamaProvider(LLMProvider):
    # Implementation for local Ollama
    
class HuggingFaceProvider(LLMProvider):
    # Implementation for HF Inference API
    
class OpenAIProvider(LLMProvider):
    # Implementation for OpenAI API
```
- Configuration via environment variables
- Easy switching between providers for testing/deployment

#### Embedding Strategy
- **Model**: BGE-small-en-v1.5 (384 dimensions) or Snowflake-arctic-embed-m
- **Local-first**: Ollama embeddings for development
- **Abstraction**: EmbeddingService interface for provider independence
- **Batch Processing**: Efficient embedding of knowledge base updates
- **Normalization**: L2 normalization for cosine similarity

### Data Architecture

#### Database Schema Design
See Meera's Database Design Document for complete schema.
Key aspects:
- UUID primary keys for all tables (security, distribution)
- Proper indexing strategy for query performance
- JSONB fields for flexible data (plan data, preferences)
- Audit trails for critical entities (plan_versions)
- Constraints for data integrity (check, foreign key)
- Soft deletes where appropriate (is_deleted flag)

#### Vector Search Implementation
- **Extension**: pgvector for PostgreSQL
- **Index Type**: IVFFlat initially (tunable via `lists` parameter)
- **Monitoring**: Query performance tracking, recall measurement
- **Migration Path**: Procedure to migrate IVFFlat → HNSW if needed
- **Hybrid Search**: 
  - Vector search: `SELECT * FROM chunks ORDER BY embedding <=> query_embedding LIMIT k`
  - Lexical search: Full-text search with `ts_rank`
  - Combination: Weighted sum or Reciprocal Rank Fusion
  - Metadata filtering: WHERE clauses applied BEFORE vector search to reduce search space

#### Connection & Transaction Management
- **Pooling**: SQLAlchemy connection pool (size based on expected concurrency)
- **Session Management**: Request-scoped sessions with automatic cleanup
- **Transactions**: Explicit transaction boundaries for data consistency
- **Read Replicas**: Configuration ready for future read scaling

### Frontend Architecture (PWA)

#### Technology Choices
- **Framework**: React 18 with Vite (fast HMR, optimized builds)
- **Styling**: Tailwind CSS (utility-first, responsive design)
- **Components**: Chakra UI (accessible, composable) or Headless UI + Tailwind
- **State Management**: 
  - Server state: React Query/TanStack Query
  - Client state: Zustand/Jotai for complex interactions
- **Forms**: React Hook Form with Yup validation
- **Animation**: Framer Motion for performant animations
- **Icons**: Heroicons for consistency
- **Internationalization**: react-i18n ready (English MVP)

#### Project Structure
```
frontend/
├── public/
│   ├── manifest.json       # PWA manifest
│   └── sw.js               # Service worker
├── src/
│   ├── assets/             # Images, icons, fonts
│   ├── components/         # Reusable UI components
│   │   ├── layout/         # Layout components (Header, Footer, etc.)
│   │   ├── ui/             # Primitive UI elements (Button, Input, etc.)
│   │   ├── chat/           # Chat-specific components
│   │   ├── plan/           # Plan viewing/modification components
│   │   └── progress/       # Progress tracking components
│   ├── hooks/              # Custom React hooks
│   ├── pages/              # Page components (routes)
│   │   ├── HomePage.jsx
│   │   ├── LoginPage.jsx
│   │   ├── ProfilePage.jsx
│   │   ├── ChatPage.jsx
│   │   ├── PlansPage.jsx
│   │   └── ProgressPage.jsx
│   ├── services/           # API service layers
│   │   ├── api.js          # Base API client
│   │   ├── authService.js
│   │   ├── profileService.js
│   │   ├── planService.js
│   │   ├── chatService.js
│   │   └── progressService.js
│   ├── store/              # Global state (if using Zustand/Jotai)
│   ├── utils/              # Utility functions
│   ├── styles/             # Tailwind configuration, global styles
│   └── main.jsx            # Application entry point
├── tailwind.config.js      # Tailwind configuration
├── postcss.config.js       # PostCSS setup
└── vite.config.js          # Vite configuration
```

#### PWA Implementation
- **manifest.json**: Name, icons, theme colors, display: standalone
- **Service Worker**: 
  - Precaching of static assets (Workbox or manual)
  - Runtime caching for API responses (stale-while-revalidate)
  - Background sync for offline actions
  - Push notification framework (future)
- **Responsive Design**: Mobile-first breakpoints (640px, 768px, 1024px)
- **Touch Optimization**: Minimum 48x48px touch targets, proper gesture handling

#### Key UI Components
1. **Chat Interface**
   - Message bubbles with clear user/assistant distinction
   - Typing indicator with animation
   - Scroll-to-bottom behavior for new messages
   - Message actions (copy, reply)
   - Timestamps and status indicators
   - Support for rich messages (cards, buttons, quick replies)

2. **Plan Viewer**
   - Structured display of workout/nutrition plans
   - Day-by-day breakdown with exercise details
   - Equipment substitution suggestions
   - Intensity scaling options
   - Print/share functionality

3. **Progress Dashboard**
   - Weight and measurement trends (charts)
   - Workout frequency and volume statistics
   - Goal progress visualization
   - Body composition tracking
   - Manual logging forms with validation

4. **Exercise Library**
   - Searchable/filterable exercise catalog
   - Detailed exercise cards with form tips
   - Equipment requirements display
   - Difficulty level filtering
   - Favorite/bookmark functionality

#### Accessibility Implementation
- **WCAG 2.1 AA Compliance Target**
- **Color Contrast**: Minimum 4.5:1 for normal text, 3:1 for large text
- **Keyboard Navigation**: Full functionality via keyboard (tab order, shortcuts)
- **Screen Reader Support**: Proper ARIA labels, roles, live regions
- **Focus Management**: Logical focus order with visible indicators
- **Text Scaling**: Support up to 200% without breaking layout or functionality
- **Motion Sensitivity**: Respect prefers-reduced-motion media query
- **Form Labels**: Explicit labels for all inputs, error identification
- **Accessible Rich Messages**: Chat cards with proper ARIA attributes

### Infrastructure and DevOps

#### Containerization Strategy
- **Multi-stage Docker Build**:
  ```
  # Backend Dockerfile
  FROM python:3.11-slim AS builder
  WORKDIR /app
  COPY requirements.txt .
  RUN pip install --user -r requirements.txt
  COPY . .
  RUN pytest  # Run tests in build stage
  
  FROM python:3.11-slim
  WORKDIR /app
  COPY --from=builder /root/.local /root/.local
  ENV PATH=/root/.local/bin:$PATH
  COPY . .
  EXPOSE 8000
  HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health/live || exit 1
  CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
  ```
  
- **Frontend Dockerfile** (similar multi-stage approach with Node builder)
- **Non-root User**: Security best practice
- **Resource Limits**: CPU/memory constraints defined

#### CI/CD Pipeline (GitHub Actions)
- **Continuous Integration**:
  - Trigger: Pull requests, pushes to main
  - Jobs:
    1. Setup (Python/Node environments)
    2. Dependency installation with caching
    3. Linting (ruff, flake8, mypy, eslint)
    4. Testing (pytest, Jest with coverage)
    5. Security scanning (safety, bandit, pip-audit, trivy)
    6. Docker build and scan
    7. Artifact storage (test reports, coverage)
    8. PR commenting with results
    
- **Continuous Deployment**:
  - Staging: Auto-deploy on main branch push after CI passes
  - Production: Manual approval gate on version tags
  - Steps:
    1. Deploy to environment (Render/Heroku/VPS)
    2. Run database migrations
    3. Smoke tests (health checks, basic endpoints)
    4. Post-deployment validation
    5. Notification on success/failure (Slack/email)

#### Monitoring and Observability
- **Logging**: Structured JSON logs sent to stdout (captured by platform)
- **Metrics**: Prometheus endpoint (`/metrics`) with:
  - Request counts, latency, error rates by endpoint
  - Database connection pool usage
  - LLM invocation statistics (latency, token usage)
  - Safety gateway decisions distribution
- **Health Checks**: 
  - Liveness: Application responsiveness
  - Readiness: Database connectivity, external service availability
- **Error Tracking**: Sentry for exception monitoring and performance tracing
- **Uptime Monitoring**: UptimeRobot for endpoint availability alerts
- **Distributed Tracing**: OpenTelemetry instrumentation (future enhancement)

#### Backup and Disaster Recovery
- **Primary**: Supabase built-in backups (daily, point-in-time recovery)
- **Secondary**: 
  - Manual monthly logical backups (pg_dump) to encrypted personal storage
  - Container images stored in registry (GitHub Packages/Docker Hub)
  - Source code in git repository
- **Recovery Procedure**:
  1. Restore database from latest backup
  2. Redeploy application from container image
  3. Validate health checks and basic functionality
  4. Notify stakeholders of restoration
- **Testing**: Quarterly restore drills to verify backup integrity

## Cross-Cutting Concerns

### Performance Optimization
- **Database**: 
  - Proper indexing on query patterns
  - Connection pooling tuning
  - Query optimization with EXPLAIN ANALYZE
  - Consider partitioning for large time-series tables
  
- **API**: 
  - Response compression (gzip)
  - Caching headers for static data
  - Pagination for list endpoints
  - Async/await throughout for concurrency
  
- **Frontend**: 
  - Code splitting and lazy loading
  - Image optimization and compression
  - Virtual scrolling for long lists (chat, exercise library)
  - Efficient rendering (React.memo, useMemo)
  
- **AI/LLM**: 
  - Response caching for non-personalized queries
  - Request batching where applicable
  - Model quantization (Q4_K_M) for local inference
  - Streaming responses for better perceived performance
  - Context window management (sliding window)

### Security Considerations
- **Authentication**: 
  - Brute force protection (rate limiting, account lockout)
  - Secure password reset implementation
  - Session management best practices
  
- **Data Protection**: 
  - Encryption at rest (managed by Supabase/PostgreSQL)
  - Encryption in transit (TLS 1.3 everywhere)
  - Field-level encryption for sensitive PII if needed
  
- **Application Security**: 
  - Regular dependency updates (dependabot)
  - SAST in CI (bandit, semgrep)
  - DAST scanning (OWASP ZAP) periodically
  - Penetration testing scope definition
  
- **API Security**: 
  - Input validation and sanitization
  - Output encoding where applicable
  - Request size limits
  - Timeout middleware
  
- **AI Safety**: 
  - Continuous monitoring of safety gateway effectiveness
  - Regular updates to safety rules and patterns
  - User feedback mechanism for false positives/negatives
  - Audit trail for all safety decisions

### Scalability Planning
- **Horizontal Scaling**: 
  - Stateless backend services behind load balancer
  - Redis for session storage and distributed caching
  
- **Database Scaling**: 
  - Read replicas for read-heavy workloads (future)
  - Connection pooling optimization
  - Consider Citus or similar for horizontal partitioning
  
- **Caching Strategy**: 
  - Redis for frequently accessed data (profiles, plans)
  - CDN for static assets (frontend)
  
- **Queueing System**: 
  - Background job processing for non-urgent tasks (image processing, reports)
  - Dead letter queue for failed jobs
  
- **Observability for Scale**: 
  - Distributed tracing implementation
  - Log aggregation and analysis (ELK stack or similar)
  - Custom business metrics dashboard

## Implementation Guidelines

### Coding Standards
- **Python**: PEP 8 compliance, enforced by ruff/flake8
- **TypeScript/JavaScript**: ESLint with Airbnb config, Prettier formatting
- **Commit Messages**: Conventional Commits format
- **Branching Strategy**: GitFlow or GitHub Flow
- **Code Review**: Mandatory pull request reviews
- **Testing**: Test-driven development where practicable

### Documentation Requirements
- **API Documentation**: Auto-generated OpenAPI/Swagger UI
- **Architecture Decisions**: ADR (Architecture Decision Record) format
- **Database Schema**: ER diagrams and data dictionary
- **User Guide**: End-user documentation for features
- **Developer Guide**: Setup, contribution, and deployment instructions
- **Runbooks**: Operational procedures for common tasks

### Quality Gates
- **Code Coverage**: Minimum 70% for new code
- **Security Scanning**: No critical/high vulnerabilities in CI
- **Performance Budgets**: Page load <3s, API response <2s (95th percentile)
- **Accessibility**: Automated axe-core testing in CI
- **Compatibility**: Cross-browser testing (Chrome, Firefox, Safari)

## Conclusion

This technical design provides a comprehensive blueprint for implementing the FitnessRAG platform. It balances sophisticated architectural patterns with practical constraints of a 1-2 week, $0/month MVP. The design emphasizes:

1. **Modularity and Separation of Concerns**: Clear boundaries between layers for maintainability
2. **Safety and Responsibility**: AI development with proper guardrails and auditability
3. **Observability and Operability**: Built-in monitoring, logging, and health checks
4. **Security and Privacy**: Protection by design throughout the stack
5. **Scalability and Performance**: Foundations ready for future growth
6. **Developer Experience**: Consistent tooling, testing, and deployment practices

By following this technical design, the team can deliver a robust, portfolio-quality platform that demonstrates senior-level architectural thinking while remaining achievable within the stated constraints.