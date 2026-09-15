# Implementation Prompt: Vikram (DevOps/QA) - Sprint 2

## Context
Based on Sprint 2 Plan decisions:
1. Sprint 1 is complete - all checkpoints done and validated
2. Sprint 2 ("Feature Complete MVP") begins 2026-09-08
3. Focus areas: Integration, Polish & Release (Days 5-7), plus support tasks throughout
4. Definition of Done must be followed for all tasks
5. Session logs required at checkpoints (use SESSION_LOG_ENHANCED.template.md)
6. Responsible for: DevOps, infrastructure, testing, performance, security

## Tasks for Vikram (DevOps/QA)

### Day 1-2: Support Tasks

#### US-304: Safety audit log dashboard (backend)
- Create safety log model: id, user_id, timestamp, safety_tier, reason, original_message, action_taken
- Create endpoint to retrieve safety logs (`/api/v1/safety/logs`)
- Add pagination and filtering (by date, tier, reason)
- Ensure logs are immutable (append-only)
- Write unit tests for safety logging
- Update API contracts in docs/api_contracts.md

### Day 5-7: Integration, Polish & Release

#### End-to-end integration testing (full user journey)
- Create test scenarios for complete user flows:
  1. New user registration → Google OAuth login → profile setup → ask fitness question → get RAG response → create plan → log workout → view progress
  2. Existing user login → view plans → modify plan via chat → log workout → check statistics
  3. User updates body measurements → see updated body composition → view progress charts
- Implement tests using pytest and selenium or playwright
- Test both happy paths and error conditions
- Write detailed test cases with expected outcomes
- Automate test execution in CI/CD pipeline

#### Performance optimization & load testing
- Identify performance bottlenecks:
  - Profile and optimize slow database queries
  - Add Redis caching for frequently accessed data (user profiles, plan templates)
  - Optimize LangGraph/RAG pipeline for faster responses
  - Implement HTTP caching headers where appropriate
  - Optimize frontend bundle size and loading
- Conduct load testing:
  - Simulate 100 concurrent users
  - Test API endpoints under load (target <2s response time)
  - Test WebSocket connections if applicable
  - Identify and fix breaking points
- Use tools like locust, k6, or jmeter for load testing
- Document performance improvements and benchmarks

#### Accessibility audit (WCAG 2.1 AA)
- Coordinate with frontend team to run axe-core accessibility testing
- Ensure all WCAG 2.1 AA violations are fixed
- Verify proper ARIA labels and roles
- Check color contrast ratios (minimum 4.5:1 for normal text)
- Test keyboard navigation throughout application
- Test screen reader compatibility (NVDA, VoiceOver)
- Document all accessibility fixes
- Create accessibility compliance report

#### PWA optimization (Lighthouse score ≥ 70)
- Run Lighthouse audit on production build
- Optimize for performance:
  - Implement efficient caching strategies (workbox)
  - Optimize image loading and compression
  - Minimize main-thread work and JavaScript execution time
  - Reduce bundle size through code splitting
  - Eliminate render-blocking resources
- Ensure offline functionality:
  - Precaching of essential assets
  - Runtime caching for API requests (with fallback)
  - Custom offline page
- Improve PWA manifest:
  - Ensure proper icons and naming
  - Add share target and file handling if applicable
- Update service worker with optimized caching strategies
- Target Lighthouse score ≥ 70 for:
  - Performance
  - Accessibility
  - Best Practices
  - SEO

#### Security scan (OWASP, bandit, trivy)
- Integrate security scanning into CI/CD pipeline:
  - Bandit for Python security issues (backend)
  - OWASP ZAP or npm audit for frontend dependencies
  - Trivy for container image scanning
  - Snyk or similar for dependency vulnerabilities
- Configure scans to fail build on high/severe issues
- Address all security findings:
  - Injection vulnerabilities
  - Broken authentication
  - Sensitive data exposure
  - XML external entities (XXE)
  - Broken access control
  - Security misconfiguration
  - XSS, CSRF
  - Using components with known vulnerabilities
- Document security scan results and remediation
- Create security report for audit purposes

#### Bug fixes and final polish
- Triage and prioritize bugs from testing
- Fix critical bugs blocking release
- Address UI/UX polish items
- Ensure consistent error handling and messaging
- Verify all forms have proper validation
- Test edge cases and boundary conditions
- Clean up temporary code and debug statements
- Ensure all logs are appropriate and not excessive

#### README and portfolio documentation
- Coordinate with documentation lead to create:
  - Setup instructions (local development, Docker, production)
  - Architecture diagram and explanation
  - API documentation (endpoints, request/response examples)
  - User guides and tutorials
  - Screenshots and demo video links
  - Technology stack and rationale
  - Design decisions and trade-offs
- Ensure documentation is clear, accurate, and up-to-date
- Verify all links work and examples are correct
- Add badges for build status, test coverage, etc.

#### Release preparation (tag v1.0.0, deployment runbook)
- Create release branch from main
- Bump version to v1.0.0 in all relevant places (package.json, setup.py, etc.)
- Create git tag v1.0.0
- Create deployment runbook documenting:
  - Prerequisites (server requirements, dependencies)
  - Step-by-step deployment instructions
  - Environment variables and configuration
  - Database migration procedures
  - Rollback procedures
  - Post-deployment verification steps
  - Monitoring and alerting setup
- Test deployment in staging environment
- Prepare rollback plan in case of issues
- Notify stakeholders of release schedule

## Verification & Testing
- Run backend tests to ensure all new endpoints work correctly
- Conduct full integration test suite (end-to-end user journeys)
- Run performance benchmarks before and after optimizations
- Execute load tests and document results
- Verify accessibility audit passes (WCAG 2.1 AA)
- Run Lighthouse and confirm score ≥ 70 in all categories
- Execute security scans and confirm no high/severe issues
- Validate all documentation is accurate and complete
- Test deployment process in staging environment
- Create session logs at end of each day using SESSION_LOG_ENHANCED.template.md

## Deliverables
- All code and infrastructure changes committed to git
- Tests written and passing (unit, integration, performance, security)
- Session logs created for each work session
- SPRINT_TRACKER_WEEK2.md updated with task status
- Deployment runbook and release documentation
- Security and accessibility reports
- Performance benchmarks and optimization documentation

## Checkpoints
- End of Day 1: Support tasks for backend safety logs completed
- End of Day 2: Performance bottlenecks identified and optimization plan created
- End of Day 3: Load testing framework established, initial benchmarks run
- End of Day 4: Security scanning integrated into CI/CD, initial scan completed
- End of Day 5: Accessibility audit coordinated, PWA optimization began
- End of Day 6: Performance and accessibility optimizations completed, Lighthouse ≥ 70
- End of Day 7: Security scan clean, release prepared, deployment runbook complete