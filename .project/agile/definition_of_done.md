# FitnessRAG — Definition of Done (DoD)
## Created by Karan (BA/Scrum Master)
## Last Updated: 2026-08-31

> **Purpose**: A shared checklist ensuring every product increment meets quality standards before being considered "complete." Every team member is accountable for these criteria.

---

## 🎯 Story-Level Definition of Done

A user story is **DONE** when ALL of the following are true:

### Code Quality
- [ ] Code reviewed and approved by at least 1 team member (PR approved)
- [ ] All acceptance criteria from the user story are met and verified
- [ ] Code follows project coding standards (PEP 8 for Python, ESLint for TypeScript)
- [ ] No `TODO`, `FIXME`, or `HACK` comments without associated GitHub issues
- [ ] Type hints/annotations present on all public functions (Python) and all components (TypeScript)
- [ ] No hardcoded secrets, API keys, or sensitive data in code

### Testing
- [ ] Unit tests written and passing with ≥70% code coverage for the story's code
- [ ] Integration tests for API endpoints (request/response contract verified)
- [ ] Safety gateway tests for AI-related stories (medical/harmful content filtering)
- [ ] All existing tests still pass (no regressions)
- [ ] Edge cases identified and tested (empty inputs, boundary values, malformed data)

### Documentation
- [ ] Docstrings on all public functions/classes (Google-style for Python)
- [ ] API endpoint documented in OpenAPI/Swagger (auto-generated from FastAPI)
- [ ] README updated if new setup steps, env vars, or dependencies added
- [ ] ADR created if an architectural decision was made

### Security
- [ ] Input validation implemented (Pydantic models for all API inputs)
- [ ] Authentication/authorization enforced on protected endpoints
- [ ] No SQL injection vectors (parameterized queries / ORM only)
- [ ] Static analysis clean (`bandit` for Python, no critical findings)
- [ ] Dependencies scanned (`pip-audit` or `safety` check passes)

### Performance
- [ ] API response time < 500ms (p95) for non-AI endpoints
- [ ] AI-powered endpoints respond within 5s (p95) with streaming
- [ ] Database queries use appropriate indexes (no sequential scans on large tables)
- [ ] No N+1 query patterns

### Deployment
- [ ] Feature deployable to staging without breaking existing functionality
- [ ] Database migrations tested (forward and rollback)
- [ ] Environment configuration documented (new env vars added to `.env.example`)
- [ ] Docker build succeeds with multi-stage production build

---

## 📦 Sprint-Level Definition of Done

A sprint is **DONE** when ALL of the following are true:

### Delivery
- [ ] All committed stories meet Story-Level DoD
- [ ] Sprint increment is demonstrable (live demo possible)
- [ ] No critical or high-severity bugs open from this sprint's work
- [ ] Product backlog updated (remaining items re-estimated if needed)

### Quality Gates
- [ ] Overall test coverage ≥ 70% across the codebase
- [ ] Security scan clean (`bandit` + `trivy` container scan)
- [ ] No known vulnerabilities in dependencies
- [ ] Structured logging verified in staging (key flows produce expected logs)

### Documentation
- [ ] Sprint increment documented (what was built, how to use it)
- [ ] API documentation up-to-date and accessible at `/docs`
- [ ] Architecture Decision Records up-to-date
- [ ] Sprint retrospective notes captured

### Process
- [ ] Sprint Review conducted with stakeholder demo
- [ ] Sprint Retrospective completed with actionable improvement items
- [ ] Next sprint backlog refined and estimated
- [ ] Burndown chart updated

---

## 🚀 Release-Level Definition of Done

A release (MVP) is **DONE** when ALL of the following are true:

### Functional Completeness
- [ ] All Must-Have (P0) user stories meet Story-Level DoD
- [ ] End-to-end user journey works: signup → profile → chat → plan → track
- [ ] Safety gateway operational with medical/harmful content filtering
- [ ] RAG knowledge base populated with curated fitness content

### Non-Functional Requirements
- [ ] Application loads within 3 seconds on 3G connection (Lighthouse score ≥ 70)
- [ ] PWA installable on Chrome (Android) and Safari (iOS)
- [ ] WCAG 2.1 AA accessibility compliance for core flows
- [ ] Application handles 50 concurrent users without degradation
- [ ] Data backup/restore procedure documented and tested

### Security & Compliance
- [ ] OWASP Top 10 addressed for applicable categories
- [ ] GDPR compliance: data export, soft delete, privacy policy
- [ ] Rate limiting active on all public API endpoints
- [ ] CORS configured for production domain only
- [ ] HTTPS enforced (TLS 1.2+)

### Operational Readiness
- [ ] Health check endpoint operational (`/health`)
- [ ] Structured logging active with correlation IDs
- [ ] Error monitoring configured (Sentry or equivalent)
- [ ] CI/CD pipeline passing for all branches
- [ ] Deployment runbook documented
- [ ] Rollback procedure tested

### Portfolio Presentation
- [ ] README with project overview, screenshots, and setup instructions
- [ ] Architecture diagram current
- [ ] Live demo environment accessible
- [ ] Key technical decisions documented in ADRs

---

## 📏 Quality Metrics & Targets

| Metric | Target | Tool | Frequency |
|--------|--------|------|-----------|
| Code Coverage | ≥ 70% | pytest-cov + vitest | Every PR |
| Security Scan | 0 critical, 0 high | bandit + trivy | Every PR |
| Dependency Vulnerabilities | 0 known | pip-audit + npm audit | Daily |
| API Response (non-AI) | < 500ms p95 | pytest benchmarks | Sprint |
| AI Response (w/ streaming) | < 5s p95 | Load test script | Sprint |
| Lighthouse Performance | ≥ 70 | Lighthouse CI | Sprint |
| Lighthouse Accessibility | ≥ 90 | Lighthouse CI | Sprint |
| Type Coverage | 100% public APIs | mypy + TypeScript strict | Every PR |

---

## ⚠️ Exception Process

If a story cannot meet all DoD criteria:
1. **Document** the specific criteria that cannot be met and why
2. **Create a tech debt ticket** in the backlog with clear remediation steps
3. **Get approval** from Ravi (Tech Lead) and Karan (Scrum Master)
4. **Time-box** the exception — tech debt must be resolved within the next sprint
5. **Track** all exceptions in the sprint retrospective for pattern analysis

> [!CAUTION]
> **Safety gateway criteria are NEVER exempted.** Any story involving AI responses MUST pass safety testing before merge. No exceptions.

---

## 📝 DoD Review Checklist (For PR Reviews)

Reviewers should verify:
```
□ Acceptance criteria met (check story card)
□ Tests present and meaningful (not just coverage padding)
□ Security considerations addressed
□ Error handling appropriate
□ Logging sufficient for debugging
□ No performance anti-patterns
□ Documentation updated
□ Migration reversible (if applicable)
```
