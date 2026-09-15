# Sprint 2 Decisions Log

| ID | Question | Research | Decision | Implementation |
|----|----------|----------|----------|----------------|
| D1 | Should we use Google OAuth only or also include other providers? | Reviewed PRODUCT_BACKLOG.md and Sprint 2 plan - specifies Google OAuth | **Google OAuth only** for MVP to keep scope manageable | Implement Google OAuth2 flow using authlib library |
| D2 | What level of AI memory should we implement for US-203? | Reviewed Sprint 1 chat system and US-203 description | **Short-term memory + explicit user preferences** - store key facts user explicitly tells us to remember | Extend conversation context with user-specific memory fields |
| D3 | How sophisticated should the safety audit log dashboard be? | Reviewed US-304 description and safety_gateway_spec.md | **Basic dashboard** showing safety decisions, timestamps, and tiers - no advanced analytics initially | Simple table view with filtering capabilities |
| D4 | Should plan templates be hardcoded or configurable? | Reviewed US-401 and Sprint 1 database setup | **Configurable via database** - allow admin to add/modify templates without code changes | Create plan_templates table with CRUD endpoints |
| D5 | What charting library should we use for progress charts? | Reviewed frontend tech stack (React, TypeScript, Vite) and US-503 | **Recharts** - lightweight, React-compatible, good for simple trend charts | Install recharts library and create reusable chart components |
| D6 | How should we handle plan versioning for US-404? | Reviewed US-404 description and Sprint 1 foundation | **Simple version numbering** with rollback capability - each modification creates new version | Add version_number column to plans table, keep history |
| D7 | Should workout logging support different types of workouts? | Reviewed US-206 and Sprint 1 chat system | **Free-form workout logging** initially - user describes workout in chat, we extract sets/reps/weight | Parse natural language for workout details, store as structured data |
| D8 | What's the approach for performance optimization in Day 5-6? | Reviewed Sprint 2 plan and technical constraints | **Focus on API latency and frontend Lighthouse score** - target <2s API response, Lighthouse ≥70 | Add response caching, optimize database queries, lazy load frontend components |
| D9 | How comprehensive should the security scan be? | Reviewed Sprint 2 plan and security requirements | **Basic but thorough** - OWASP ZAP, bandit (Python), trivy (container) - no penetration testing | Integrate security scans into CI/CD pipeline, fail build on high/severe issues |
| D10 | What should be included in the README and portfolio documentation? | Reviewed Sprint 2 plan and existing documentation | **Complete package** - setup instructions, architecture diagram, API documentation, screenshots, video demo | Create docs/ folder with comprehensive documentation |

## Rationale for Key Decisions

**D1 - Google OAuth Scope Limitation**: 
- Sprint 2 goal is "Feature Complete MVP" not exhaustive feature set
- Google covers majority of target users (based on user research in PRD)
- Other providers (Apple, Facebook) can be added in future sprints
- Keeps authentication implementation simple and focused

**D2 - AI Memory Approach**:
- Balances personalization with privacy and implementation complexity
- Explicit preferences are more reliable than inferred memories
- Aligns with Sprint 1's conversational AI foundation
- Reduces risk of incorrect assumptions about user preferences

**D4 - Configurable Plan Templates**:
- Enables faster iteration based on user feedback
- Reduces need for code updates when adding new workout types
- Aligns with Epic 1 (Knowledge Ingestion) principles of configurability
- Supports future expansion to user-generated templates

**D5 - Recharts Selection**:
- Already in line with frontend tech stack (React)
- Smaller footprint than alternatives like Chart.js or Victory
- Good documentation and community support
- Sufficient for MVP progress tracking needs

**D8 - Performance Optimization Focus**:
- Addresses known risks from Sprint 1 (LLM latency)
- Measurable targets (API latency, Lighthouse score)
- Foundation for future optimization efforts
- User-facing metrics that directly impact experience

## Open Questions Requiring Research

| ID | Question | Needed By |
|----|----------|-----------|
| R1 | What's the exact format for Google OAuth callback handling? | Day 1-2 |
| R2 | How should we structure the AI memory database schema? | Day 1-2 |
| R3 | What specific metrics should the safety audit log track? | Day 1 |
| R4 | Should plan templates include exercise substitutions? | Day 2 |
| R5 | What chart types are most useful for progress tracking? | Day 3-4 |
| R6 | How many versions of a plan should we retain by default? | Day 3-4 |
| R7 | What natural language patterns should we recognize for workout logging? | Day 4 |
| R8 | Which specific API endpoints need caching for performance? | Day 5-6 |
| R9 | What constitutes a "high/severe" security issue for build failure? | Day 5-6 |
| R10 | What level of detail should architecture diagrams include? | Day 7 |

## Risk Flags Identified

| ID | Risk | Probability | Impact | Mitigation |
|----|------|-------------|--------|------------|
| RISK1 | Google OAuth integration complexity | Medium | High | Use well-tested authlib library, time-box to 1 day, have fallback plan |
| RISK2 | Plan generation quality (LLM output structure) | High | High | Strict Pydantic output schemas; fallback to template-based generation |
| RISK3 | Chat-to-plan intent recognition accuracy | Medium | High | Pre-define intent patterns; leverage LangGraph routing nodes |
| RISK4 | Chart rendering performance on mobile | Medium | Medium | Use lightweight chart lib (Recharts); lazy load charts |
| RISK5 | Sprint velocity overestimation (carrying over Sprint 1 debt) | Medium | High | Reserve Day 1 morning for Sprint 1 carryover; re-estimate immediately |
| RISK6 | Security scan delays release timeline | Low | Medium | Integrate scans early in CI, maintain security backlog for lower priority issues |