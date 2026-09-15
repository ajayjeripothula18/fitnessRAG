# Product Backlog

**Project**: Fitness & Nutrition Guidance Platform (MVP)
**Status**: Backlog Refinement Required

## Epics

### Epic 1: Knowledge Ingestion & RAG Foundation
**Description**: Establish the pipeline for ingesting authoritative fitness/nutrition data (WHO, CDC, etc.) and serving it via vector search.
**Priority**: High
- [ ] Story 1.1: Setup PostgreSQL + pgvector database schema.
- [ ] Story 1.2: Create Python script to parse and chunk initial PDF/HTML data sources.
- [ ] Story 1.3: Implement text embeddings pipeline (SentenceTransformers) and ingest data to pgvector.
- [ ] Story 1.4: Implement retrieval endpoint (`/retrieve`) with hybrid search capabilities.

### Epic 2: Core LLM & Orchestration (LangGraph)
**Description**: Build the backend orchestration layer that receives user queries, applies safety guardrails, and coordinates RAG with the LLM.
**Priority**: High
- [ ] Story 2.1: Integrate Local LLM (Ollama) and cloud fallback via LangChain.
- [ ] Story 2.2: Implement the Safety Gateway classifier (block medical diagnosis/high-risk queries).
- [ ] Story 2.3: Build the main conversational LangGraph state machine.
- [ ] Story 2.4: Connect LangGraph agent to the pgvector retrieval tool.

### Epic 3: User State & Profiles
**Description**: Allow users to maintain state (goals, physical stats, preferences) so advice is personalized.
**Priority**: Medium
- [ ] Story 3.1: Design and deploy User Profile database tables in PostgreSQL.
- [ ] Story 3.2: Build CRUD endpoints in FastAPI for managing user profiles.
- [ ] Story 3.3: Inject user profile context into the LLM prompt dynamically.

### Epic 4: Mobile-First Frontend PWA
**Description**: Create the user interface for chatting with the AI and viewing structured plans.
**Priority**: Medium
- [ ] Story 4.1: Setup frontend scaffolding (React/Vite or Next.js) with PWA support.
- [ ] Story 4.2: Implement Chat UI component.
- [ ] Story 4.3: Implement User Profile settings page.

### Epic 5: Deterministic Planning & Calculations
**Description**: Implement hard-coded rules and calculations (TDEE, Body Fat) that shouldn't rely on LLM hallucinations.
**Priority**: Low
- [ ] Story 5.1: Create Python utility functions for standard fitness formulas (TDEE, BMI, macros).
- [ ] Story 5.2: Expose formulas as tools to the LangGraph agent.
