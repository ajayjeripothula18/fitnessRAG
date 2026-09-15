# FitnessRAG — Sprint 2 Plan: "Feature Complete MVP"
## Created by Karan (BA/Scrum Master)
## Last Updated: 2026-08-31

---

## Sprint Overview

| Field | Value |
|-------|-------|
| **Sprint Number** | 2 |
| **Sprint Name** | Feature Complete MVP |
| **Duration** | 1 Week (7 days) |
| **Sprint Goal** | Users can create personalized workout plans, track progress with body composition, and have richer AI interactions with plan generation and workout logging |
| **Estimated SP** | ~56 SP (adjusted based on Sprint 1 velocity) |
| **Capacity** | Full team × 7 days = 35 person-days |

---

## Sprint Goal Validation

> **Done when**: A user can generate a personalized workout plan through AI, log workouts, record body measurements, view progress charts, and manage plan versions — all within the established safe AI framework.

---

## Sprint Backlog

### Day 1-2: Enhanced Auth & AI Memory

| Story | Owner | SP | Dependencies | Day |
|-------|-------|-----|-------------|-----|
| US-103: Google OAuth sign-in | Meera | 5 | Sprint 1 auth foundation | D1-D2 |
| US-106: Password reset flow | Meera | 3 | Sprint 1 auth | D1-D2 |
| US-203: AI memory & preferences | Ravi | 5 | Sprint 1 chat system | D1-D2 |
| US-304: Safety audit log dashboard | Vikram | 2 | Sprint 1 safety gateway | D1 |

### Day 2-4: Plan Generation & Management

| Story | Owner | SP | Dependencies | Day |
|-------|-------|-----|-------------|-----|
| US-401: Curated plan templates | Ravi + Meera | 3 | Sprint 1 database | D2 |
| US-402: AI-powered plan generation | Ravi | 5 | US-203, US-401 | D2-D3 |
| US-403: Plan display (day-by-day view) | Zara | 3 | US-402 | D3-D4 |
| US-404: Plan versioning & rollback | Meera | 3 | US-402 | D3-D4 |
| US-204: Workout plan creation via chat | Ravi + Meera | 8 | US-402 | D3-D4 |
| US-205: Chat-based plan modifications | Ravi | 5 | US-204 | D4-D5 |

### Day 3-5: Progress Tracking & Workout Logging

| Story | Owner | SP | Dependencies | Day |
|-------|-------|-----|-------------|-----|
| US-501: Body measurement recording | Meera + Zara | 3 | Sprint 1 profile | D3 |
| US-502: Body composition calculator | Meera | 3 | US-501 | D3-D4 |
| US-206: Chat-based workout logging | Ravi + Meera | 3 | Sprint 1 chat | D4 |
| US-503: Progress trend charts | Zara | 5 | US-501, US-206 | D4-D5 |
| US-504: Workout statistics | Zara + Meera | 3 | US-206 | D5 |

### Day 5-7: Integration, Polish & Release

| Task | Owner | Day |
|------|-------|-----|
| End-to-end integration testing (full user journey) | Vikram + All | D5-D6 |
| Performance optimization & load testing | Vikram | D6 |
| Accessibility audit (WCAG 2.1 AA) | Zara | D6 |
| PWA optimization (Lighthouse score ≥ 70) | Zara | D6 |
| Security scan (OWASP, bandit, trivy) | Vikram | D6 |
| Bug fixes and final polish | All | D6-D7 |
| README and portfolio documentation | Ravi + All | D7 |
| Sprint review / MVP demo | All | D7 |
| Sprint retrospective | All | D7 |
| Release preparation (tag v1.0.0, deployment runbook) | Vikram + Ravi | D7 |

---

## Story Dependency Graph

```
Sprint 1 Foundation
├── US-103 (Google OAuth)
├── US-106 (Password Reset)
├── US-203 (AI Memory)
│   └── US-402 (AI Plan Generation)
│       ├── US-204 (Plan via Chat)
│       │   └── US-205 (Plan Modifications via Chat)
│       ├── US-403 (Plan Display)
│       └── US-404 (Plan Versioning)
├── US-401 (Plan Templates)
│   └── US-402
├── US-304 (Safety Audit Logs)
├── US-501 (Body Measurements)
│   ├── US-502 (Body Composition Calc)
│   └── US-503 (Progress Charts)
├── US-206 (Chat Workout Logging)
│   ├── US-503
│   └── US-504 (Workout Statistics)
```

---

## Sprint 2 Specific Risks

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| Plan generation quality (LLM output structure) | High | High | Strict Pydantic output schemas; fallback to template-based generation |
| Chat-to-plan intent recognition accuracy | Medium | High | Pre-define intent patterns; leverage LangGraph routing nodes |
| OAuth integration complexity (Google callback flow) | Low | Medium | Use well-tested library (authlib); time-box to 1 day |
| Chart rendering performance on mobile | Medium | Medium | Use lightweight chart lib (Chart.js or Recharts); lazy load |
| Sprint velocity overestimation (carrying over Sprint 1 debt) | Medium | High | Reserve Day 1 morning for Sprint 1 carryover; re-estimate immediately |

---

## Flex Stories (Deprioritize if Behind)

If the sprint is running behind, these stories can be moved to a post-MVP backlog:

1. **US-504** (Workout Statistics) — nice to have, not core flow
2. **US-304** (Safety Audit Dashboard) — can use raw DB queries initially
3. **US-205** (Chat Plan Modifications) — users can recreate plans as workaround
4. **US-404** (Plan Versioning) — can use simple overwrite initially

---

## Sprint 2 Definition of Done Additions

In addition to the standard DoD, Sprint 2 must also verify:

- [ ] MVP Release Checklist complete (all release-level DoD items)
- [ ] Production deployment tested with rollback verified
- [ ] README has screenshots, architecture diagram, and setup instructions
- [ ] Portfolio-ready: live demo accessible, code clean, no debug artifacts
- [ ] All "Should Have" stories either complete or explicitly deferred with justification

---

## Daily Focus Areas

| Day | Focus | Key Metric |
|-----|-------|-----------|
| D1 | Sprint 1 carryover + OAuth + Memory | Sprint 1 bugs = 0 |
| D2 | Plan templates + Generation begins | Template data seeded |
| D3 | Plan generation + Body tracking | AI generates valid plan structure |
| D4 | Chat-plan integration + Charts | E2E: chat → plan → stored |
| D5 | Workout logging + Statistics | Full tracking pipeline works |
| D6 | Testing + Security + Performance | All quality gates green |
| D7 | Release prep + Demo + Retro | v1.0.0 tagged, demo smooth |

---

## Sprint 2 Success Criteria

**The sprint is successful if:**
1. ✅ Users can generate personalized workout plans through AI conversation
2. ✅ Plans display in structured day-by-day format with exercises
3. ✅ Users can log body measurements and see body composition estimates
4. ✅ Progress charts show trends over time (weight, body fat %)
5. ✅ Chat-based workout logging stores data accurately
6. ✅ Google OAuth provides alternative sign-in
7. ✅ MVP passes all release-level DoD criteria
8. ✅ Application deployed to production with monitoring active
9. ✅ README and portfolio documentation complete
