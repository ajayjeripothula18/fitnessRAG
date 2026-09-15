# FitnessRAG Architecture Document
# Synthesized Research from All Team Members

## Executive Summary

This architecture document synthesizes the research findings from all team members (Priya CPO, Arjun CTO, Ravi Tech Lead, Meera Backend Engineer, Zara UX Lead, Vikram QA/DevOps, and Karan BA/Scrum Master) for the FitnessRAG project - an AI-powered Fitness & Nutrition Guidance Platform designed as a portfolio/resume project.

The architecture balances the ambitious technical goals with the constrained timeline (1-2 weeks) and budget ($0/month), focusing on a vertical slice that demonstrates senior-level architectural thinking while remaining achievable.

## Core Architectural Principles

### 1. Modularity and Separation of Concerns
- **Backend**: FastAPI with modular structure (`app/api/v1/`, `app/core/`, `app/models/`, `app/schemas/`, `app/services/`, `app/utils/`)
- **Frontend**: React/Vite with component-based architecture
- **AI Layer**: LangGraph for stateful workflows with clear separation of concerns
- **Data**: PostgreSQL with pgvector for relational data and vector search
- **Infrastructure**: Docker containers, infrastructure as code principles

### 2. AI-First with Safety Guardrails
- **Primary Interface**: Conversational AI coach as main user interaction
- **Safety Gateway**: Pre-processing layer for medical/harmful content detection
- **Structured Outputs**: Pydantic models for LLM responses to ensure consistency
- **Tool Usage**: Controlled orchestration rather than autonomous agents

### 3. Data-Centric Design
- **Single Source of Truth**: PostgreSQL for all application data (users, plans, progress, etc.)
- **Vector Search**: pgvector for semantic search capabilities
- **Knowledge Separation**: Clear distinction between application data and RAG knowledge base
- **Versioning**: Plan versioning for auditability and rollback capabilities

### 4. Observable and Operable
- **Logging**: Structured JSON logging with correlation IDs
- **Monitoring**: Health checks, metrics, error tracking
- **Testing**: Comprehensive testing strategy (unit, integration, E2E)
- **Deployment**: CI/CD pipeline with automated testing and security scanning

### 5. Security and Privacy by Design
- **Authentication**: JWT-based with refresh tokens
- **Authorization**: Role-based access control
- **Data Protection**: Encryption at rest and in transit where appropriate
- **Privacy**: User data isolation, export/delete capabilities
- **Secrets Management**: Environment variables, never hardcoded

## Detailed Architecture Components

### Backend Architecture (FastAPI)

#### Project Structure
```
app/
├── api/
│   └── v1/
│       ├── auth.py
│       ├── users.py
│       ├── profiles.py
│       ├── plans.py
│       ├── chat.py
│       └── progress.py
├── core/
│   ├── config.py
│   ├── security.py
│   └── dependencies.py
├── models/
│   ├── user.py
│   ├── profile.py
│   ├── plan.py
│   ├── workout.py
│   └── measurement.py
├── schemas/
│   ├── auth.py
│   ├── user.py
│   ├── profile.py
│   ├── plan.py
│   ├── chat.py
│   └── progress.py
├── services/
│   ├── auth_service.py
│   ├── llm_service.py
│   ├── rag_service.py
│   ├── safety_service.py
│   └── plan_service.py
├── utils/
│   ├── database.py
│   └── helpers.py
└── main.py
```

#### Key Technical Decisions
- **Async/Await**: Throughout for I/O operations using asyncpg and httpx.AsyncClient
- **Dependency Injection**: FastAPI's built-in DI for services, database connections
- **Validation**: Pydantic v2 for request/response models with comprehensive validation
- **Authentication**: OAuth2 with JWT access/refresh tokens
- **Rate Limiting**: Using slowapi to prevent abuse
- **Security Headers**: Middleware to add CSP, HSTS, X-Frame-Options, etc.
- **CORS**: Properly configured based on environment
- **Logging**: structlog for structured JSON logging
- **Exception Handling**: Custom handlers for consistent error responses

### AI Architecture (LangGraph + LLM)

#### State Design
```python
from typing import TypedDict, Annotated, List, Optional
from langgraph.graph import StateGraph, END

class FitnessAgentState(TypedDict):
    messages: Annotated[List[BaseMessage], "The messages in the conversation"]
    user_profile: Optional[Dict]  # Structured user profile data
    active_plan: Optional[Dict]   # Current workout/nutrition plan
    progress_data: Optional[Dict] # Recent progress measurements
    user_memory: Optional[Dict]   # Persistent user preferences/facts
    safety_check: Optional[Dict]  # Results from safety gateway
    rag_context: Optional[List[Dict]] # Retrieved knowledge chunks
    tool_calls: Optional[List[Dict]] # Pending tool executions
    response: Optional[str]       # Final response to user
```

#### Workflow Design
1. **Entry Point**: User message received
2. **Safety Check**: Route to safety gateway node
3. **Intent Classification**: Determine if RAG needed, tool use required, or direct response
4. **Tool Execution**: If needed, execute appropriate tools (get_profile, search_knowledge, etc.)
5. **RAG Retrieval**: If knowledge needed, retrieve and rank relevant documents
6. **LLM Generation**: Generate response using LLM with context
7. **Validation**: Validate output against business rules
8. **Exit**: Return response to user

#### Key Components
- **Safety Gateway Node**: Pre-processes input for medical/harmful content
- **Retrieval Node**: Hybrid search (vector + lexical) with reranking
- **Tool Nodes**: Encapsulated functions for profile access, plan modification, etc.
- **LLM Node**: Handles response generation with streaming capability
- **Validation Node**: Ensures output meets structural and business requirements
- **Checkpointer**: PostgresSaver for production persistence

#### LLM Strategy
- **Primary**: Llama 3 8B via Ollama for local development ($0 cost)
- **Fallback**: Hugging Face free tier for public demo (with usage monitoring)
- **Abstraction Layer**: Provider-independent interface for easy switching
- **Quantization**: Q4_K_M for balance of quality and performance
- **Streaming**: Implemented for better perceived performance
- **Structured Output**: JSON mode used where available for reliable parsing

### Data Architecture

#### Database Schema (PostgreSQL)
Core tables as designed by Meera:
- `users`: Authentication and OAuth information
- `profiles`: Fitness profile with all personalization attributes
- `plans`: Workout and nutrition plans (template vs instance)
- `plan_versions`: Audit trail for plan modifications
- `workouts`: Scheduled and completed workouts
- `workout_logs`: Detailed exercise performance data
- `body_measurements`: Physical measurements and derived metrics
- `exercises`: Standard exercise library with metadata
- `knowledge_sources`: Provenance for RAG knowledge
- `knowledge_documents`: Source documents
- `knowledge_chunks`: Vector embeddings with metadata

#### Indexing Strategy
- **Primary Keys**: UUID with `gen_random_uuid()`
- **Foreign Keys**: Automatically indexed
- **Frequently Queried**: Indexes on email, user_id, date columns
- **Full-Text Search**: GIN indexes on tsvector columns for exercise search
- **Vector Similarity**: IVFFlat index initially (tunable lists parameter)
- **Hybrid Search**: Metadata filtering applied BEFORE vector search
- **Composite Indexes**: For common query patterns (user_id + date ranges)

#### Data Flow
1. **User Input**: Through API endpoints → Validation → Service Layer
2. **AI Processing**: Through LangGraph workflow → State updates
3. **Data Persistence**: Through SQLAlchemy ORM → PostgreSQL
4. **Cache Layer**: Application-level caching for frequently accessed data
5. **Backup Strategy**: Supabase built-in backups + manual logical backups

### Frontend Architecture (PWA)

#### Technical Stack
- **Framework**: React with Vite for fast development
- **Styling**: Tailwind CSS for utility-first approach
- **Component Library**: Chakra UI or Headless UI + Tailwind
- **State Management**: React Query/TanStack Query for server state
- **Forms**: React Hook Form with Yup validation
- **Animations**: Framer Motion for smooth transitions
- **Icons**: Heroicons for consistent iconography
- **PWA**: Manifest.json + Service Worker for offline capabilities

#### Key UI Components
- **Chat Interface**: Message bubbles with typing indicators
- **Dashboard**: Overview of today's workout, progress, quick actions
- **Plan Viewer**: Structured display of workout/nutrition plans
- **Progress Tracking**: Charts and forms for logging measurements
- **Exercise Library**: Searchable/filterable exercise catalog
- **Settings**: Profile management, preferences, connected accounts

#### Mobile-First Features
- **Responsive Breakpoints**: 640px, 768px, 1024px
- **Touch Optimization**: Minimum 48x48px touch targets
- **Bottom Navigation**: Primary app sections (Dashboard, Coach, Plan, Progress)
- **Floating Action Button**: Contextual primary actions
- **Gesture Support**: Swipe navigation between days in plan
- **Offline Capabilities**: Service worker caching for static assets
- **Installability**: Manifest.json for "Add to Home Screen"

#### Accessibility Implementation
- **WCAG 2.1 AA**: Target compliance level
- **Color Contrast**: Minimum 4.5:1 for normal text
- **Keyboard Navigation**: Full functionality via keyboard
- **Screen Reader Support**: Proper ARIA labels and landmarks
- **Focus Management**: Logical tab order with visible indicators
- **Text Scaling**: Support up to 200% without breaking layout
- **Motion Sensitivity**: Respect prefers-reduced-motion media query

### Infrastructure and DevOps

#### Containerization
- **Multi-stage Docker Build**:
  - Builder stage: Install dependencies, run tests
  - Runtime stage: Copy only necessary artifacts
  - Non-root user for security
  - Healthcheck implementation
  
#### CI/CD Pipeline (GitHub Actions)
1. **Continuous Integration**:
   - Trigger: Pull requests and pushes to main
   - Steps:
     - Checkout code
     - Setup Python/node environments
     - Install dependencies
     - Run linters (ruff, flake8, mypy, eslint)
     - Run test suite (pytest, Jest)
     - Security scanning (safety, bandit, pip-audit)
     - Build Docker image
     - Container scanning (trivy)
     - Upload artifacts
     - Comment on PR with results
   
2. **Continuous Deployment**:
   - Trigger: Push to main branch (staging), tags (production)
   - Steps:
     - Deploy to staging environment
     - Run database migrations
     - Smoke tests
     - Manual approval for production
     - Deploy to production
     - Post-deployment validation
     - Notification on success/failure

#### Monitoring and Observability
- **Logging**: Structured JSON logs forwarded to log aggregation
- **Metrics**: Prometheus metrics endpoint (request counts, latency, error rates)
- **Health Checks**: `/health/live` and `/health/ready` endpoints
- **Error Tracking**: Sentry for exception monitoring
- **Uptime Monitoring**: UptimeRobot for endpoint availability
- **Performance Monitoring**: Browser metrics via web-vitals library
- **Distributed Tracing**: OpenTelemetry for cross-service tracing (if needed)

#### Backup and Disaster Recovery
- **Primary**: Supabase built-in backups (daily, point-in-time recovery)
- **Secondary**: Manual monthly logical backups (pg_dump) to encrypted storage
- **Application**: Container images in registry, code in git
- **Configuration**: Environment-specific configs in repo (secrets in vault/manager)
- **Testing**: Quarterly restore tests to validate backup integrity
- **Documentation**: Runbooks for common recovery scenarios

## Cross-Cutting Concerns

### Safety Architecture
1. **Pre-processing Layer**:
   - Input sanitization and validation
   - Length and character set limits
   - Basic profanity filtering
   
2. **Safety Classification**:
   - Rule-based checks (medical keywords, harmful patterns)
   - ML-based toxicity detection (Detoxify or Perspective API)
   - Medical content detection (spaCy + custom rules)
   - Fitness-specific contraindication checking
   
3. **Decision Engine**:
   - SAFE: Normal processing
   - MEDICAL_CONSULTATION_REQUIRED: Disclaimer + professional suggestion
   - HARMFUL_CONTENT: Block + educational response
   - OUT_OF_SCOPE: Polite redirection to fitness/nutrition
   
4. **Post-processing Validation**:
   - Validate generated content against safety rules
   - Check for unintended medical advice
   - Ensure exercise recommendations match user profile
   - Verify nutritional guidance is general, not prescriptive

### Performance Optimization
- **Database**: 
  - Connection pooling (SQLAlchemy)
  - Proper indexing strategy
  - Query optimization with EXPLAIN ANALYZE
  - Consider read replicas for read-heavy workloads
  
- **API**:
  - Response compression (gzip)
  - Caching headers where appropriate
  - Pagination for large datasets
  - Async/await throughout for concurrency
  
- **Frontend**:
  - Code splitting and lazy loading
  - Image optimization and compression
  - Efficient rendering (React.memo, useMemo)
  - Virtual scrolling for long lists
  
- **AI/LLM**:
  - Response caching for non-personalized queries
  - Request batching where applicable
  - Model quantization (Q4_K_M)
  - Streaming responses for better UX
  - Context window management

### Scalability Considerations
- **Horizontal Scaling**: Stateless backend services behind load balancer
- **Database Read Scaling**: Read replicas if using managed PostgreSQL
- **Caching**: Redis for session storage and frequent queries
- **Queueing**: Background job processing for non-urgent tasks
- **CDN**: For static assets if needed
- **Microservices**: Path to evolution if monolith becomes limiting

## Implementation Roadmap

### Phase 1: Walking Skeleton (Days 1-3)
- Project setup and repo initialization
- Basic CI/CD pipeline with linting
- Authentication system (signup/login/JWT)
- Basic FastAPI structure with health endpoints
- Simple React/Vite frontend with routing

### Phase 2: Core MVP (Days 4-7)
- User profile management
- Basic chat interface with LLM integration
- Safety gateway implementation
- Exercise library and basic plan structures
- Initial data models and database schema

### Phase 3: Feature Enhancement (Days 8-10)
- LangGraph workflow implementation
- Personalized plan generation
- Plan modification functionality
- Progress tracking and measurement logging
- Body-fat calculator implementation

### Phase 4: Polish and Demo Preparation (Days 11-14)
- UI/UX refinements and mobile responsiveness
- Accessibility improvements
- Comprehensive testing (unit, integration, E2E)
- Security scanning and vulnerability remediation
- Performance optimization and monitoring setup
- Demo preparation and documentation

## Risk Mitigation

### Technical Risks
1. **LLM Performance/Cost**:
   - Mitigation: Local-first design with Ollama, usage monitoring, fallback to smaller models
   
2. **Vector Search Performance**:
   - Mitigation: Start with IVFFlat, monitor, migrate to HNSW if needed, implement metadata filtering
   
3. **Integration Complexity**:
   - Mitigation: Modular design, clear interfaces, contract testing, spike solutions
   
4. **Security Vulnerabilities**:
   - Mitigation: Regular scanning, dependency updates, penetration testing, security headers
   
5. **Scope Creep**:
   - Mitigation: Strict adherence to MVP definition, backlog grooming, stakeholder alignment

### Schedule Risks
1. **Underestimation**:
   - Mitigation: Buffer time in estimates, focus on vertical slice, prioritize ruthlessly
   
2. **Dependencies**:
   - Mitigation: Minimize external dependencies, use timeouts and fallbacks, circuit breakers
   
3. **Technical Debt**:
   - Mitigation: Track intentionally incurred debt, plan for repayment, maintain quality bar

## Success Metrics

### Technical Success
1. Application deploys successfully to free tier services
2. Core features (chat, profiles, plans, progress) functional
3. Testing coverage meets minimums (70% unit test coverage)
4. Security scans show no critical/high vulnerabilities
5. Performance meets basic thresholds (<3s page load, <2s API response)
6. Application is responsive and accessible

### Portfolio Success
1. Demonstrates senior-level architectural thinking
2. Shows clear separation of concerns and modularity
3. Includes observable practices (logging, monitoring, testing)
4. Implements security best practices
5. Features clean, maintainable code
6. Documents decisions and tradeoffs
7. Shows ability to deliver working software in constrained timeline

### User Success (Founder/Family/Friends)
1. Founder can use for personal fitness/nutrition guidance
2. Basic conversational interaction works reliably
3. Plan generation and modification provides value
4. Progress tracking shows meaningful data
5. Interface is intuitive and usable
6. Safety mechanisms prevent harmful advice
7. Application installs and works on mobile devices

## Conclusion

This architecture provides a solid foundation for a portfolio-quality Fitness & Nutrition Guidance Platform that demonstrates sophisticated technical capabilities while remaining achievable within the 1-2 week, $0/month constraints. The design emphasizes modularity, safety, observability, and maintainability—all hallmarks of senior-level engineering—while delivering tangible value through a conversation-first AI coach with personalized fitness features.

By following this architecture and the recommended implementation approach, the team can deliver a meaningful portfolio piece that showcases their abilities in full-stack development, AI integration, system design, and professional software practices.