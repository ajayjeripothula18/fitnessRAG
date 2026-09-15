---
description: Complete RRPAI workflow for all task types (sprints, features, hotfixes)
---

# RRPAI Workflow - Master Orchestrator

**Version**: 3.1 (Modular)  
**Last Updated**: 2026-01-04  
**Structure**: Master + 7 Phase-Specific Workflows

---

## Quick Navigation

| Phase | Quick Link | Time Estimate |
|-------|------------|---------------|
| 1. REVIEW | `/rrpai/review` | 15-30 min |
| 2. RESEARCH | `/rrpai/research` | 30 min - 4 hours |
| 3. PLAN | `/rrpai/plan` | 30 min - 5 hours |
| 4. APPROVE | `/rrpai/approve` | 5-60 min |
| 5. IMPLEMENT | `/rrpai/implement` | 1-40 hours |
| 6. VALIDATE | `/rrpai/validate` | 15 min - 2 hours |
| 7. ITERATE | `/rrpai/iterate` | Varies |

---

## The 7-Phase Cycle

```
1. REVIEW     → Understand requirements and current state
2. RESEARCH   → Gather information and validate approaches
3. PLAN       → Create comprehensive implementation plan
4. APPROVE    → Get user sign-off before coding
5. IMPLEMENT  → Execute with mandatory checkpoints
6. VALIDATE   → Test systematically (Unit → Integration → E2E)
7. ITERATE    → Handle failures via root cause analysis
```

**Critical Rule**: Do NOT skip phases. Each phase builds on the previous one.

---

## When to Use This Workflow

### ✅ Use For:
- Sprint planning (multi-day features)
- Major features (new components/systems)
- Hotfixes (critical bugs)
- Bug fixes (non-critical issues)
- API development (new endpoints)
- Research tasks (technical investigations)

### ❌ Skip For:
- Simple file reads or explanations
- One-line code changes
- Minor documentation updates
- Context loading only

---

## Complete Flow Diagram

```
USER REQUEST
    ↓
[1. REVIEW] (/rrpai/review)
    ↓
Research needed?
├─ No → Skip to PLAN
└─ Yes → [2. RESEARCH] (/rrpai/research)
              ├─ Light (web search)
              ├─ Standard (web + docs)
              └─ Multi-model (critical decisions)
    ↓
[3. PLAN] (/rrpai/plan)
    ├─ Major Feature: PRD + TDD
    ├─ Sprint: Tracker + Decisions + Prompts
    ├─ API: Spec + Prompt
    └─ Hotfix/Bug: Debugging Prompt
    ↓
[4. APPROVE] (/rrpai/approve)
    ├─ Gate 1: PRD (major features)
    ├─ Gate 2: TDD (major features)
    └─ Gate 3: Plan (all tasks)
    ↓
Approved? ──No──> Loop to PLAN
    ↓ Yes
[5. IMPLEMENT] (/rrpai/implement)
    ├─ With mandatory checkpoints
    ├─ Session logging
    └─ Progress tracking
    ↓
[6. VALIDATE] (/rrpai/validate)
    ├─ Unit tests
    ├─ Integration tests (cURL)
    └─ E2E tests
    ↓
Test Results?
├─ ✅ All Pass → COMPLETE
├─ ⚠️ Minor Issues → Loop to IMPLEMENT
└─ ❌ Major Issues → [7. ITERATE] (/rrpai/iterate)
                          ↓
                    Root Cause Analysis
                          ↓
                    ├─ Requirements Gap → Loop to REVIEW
                    ├─ Research Gap → Loop to RESEARCH
                    ├─ Design Flaw → Loop to PLAN
                    └─ Implementation Bug → Loop to IMPLEMENT
```

---

## Quick Start Guide

### Step 1: Choose Your Starting Point

**For most tasks**, start at Phase 1 (REVIEW):
```bash
cat .agent/workflows/review.md
```

**If you already know what to do**, you might skip to PLAN:
```bash
cat .agent/workflows/plan.md
```

### Step 2: Follow the Phase Workflow

Each phase workflow contains:
- Detailed steps
- Decision criteria
- Templates to use
- Success criteria
- Tool commands (with `// turbo` annotations)

### Step 3: Create Checkpoints (Mandatory)

For multi-session work (>4 hours):
- Use `SESSION_LOG_ENHANCED.template.md`
- Create after each major component
- At least once per day

### Step 4: Validate Thoroughly

Don't skip testing:
- Unit tests (always)
- Integration tests (cURL smoke tests)
- E2E tests (full workflow)

### Step 5: Iterate When Needed

If validation fails, use Phase 7 (ITERATE) to:
- Analyze root cause
- Determine which phase to loop back to
- Execute mini-RRPAI cycle

---

## Task Type Quick Reference

| Task Type | Start At | Required Artifacts | Approvals |
|-----------|----------|-------------------|-----------|
| **Major Feature** | REVIEW | PRD + TDD + Prompts | 3 gates |
| **Sprint** | REVIEW | Sprint Tracker + Decisions + Prompts | 1 gate (plan) |
| **Single API** | REVIEW | API Spec + Prompt | 1 gate (plan) |
| **Hotfix** | REVIEW | Implementation Plan | 1 gate (if risky) |
| **Bug Fix** | REVIEW | Debugging Prompt | 0-1 gates |

---

## Phase Summaries

### Phase 1: REVIEW → `/rrpai/review`
**Purpose**: Understand requirements  
**Actions**: Load context, analyze, identify gaps, ask questions  
**Output**: Clear requirements, gaps documented  
**Time**: 15-30 min

### Phase 2: RESEARCH → `/rrpai/research`
**Purpose**: Gather information  
**Actions**: Web search, multi-model (if critical), knowledge base  
**Output**: Solutions validated, >80% confidence  
**Time**: 30 min - 4 hours (multi-model)

### Phase 3: PLAN → `/rrpai/plan`
**Purpose**: Create implementation plan  
**Actions**: PRD/TDD/Prompts, define checkpoints, routing by task type  
**Output**: Comprehensive plan, checkpoints defined  
**Time**: 30 min - 5 hours

### Phase 4: APPROVE → `/rrpai/approve`
**Purpose**: Get user sign-off  
**Actions**: Present plan, get approval, address feedback  
**Output**: User approval, ready to implement  
**Time**: 5-60 min

### Phase 5: IMPLEMENT → `/rrpai/implement`
**Purpose**: Execute changes  
**Actions**: Code, mandatory checkpoints, session logs  
**Output**: Implementation complete, tests written  
**Time**: 1-40 hours

### Phase 6: VALIDATE → `/rrpai/validate`
**Purpose**: Verify correctness  
**Actions**: Unit → Integration → E2E tests  
**Output**: Test results, decision (complete/fix/iterate)  
**Time**: 15 min - 2 hours

### Phase 7: ITERATE → `/rrpai/iterate`
**Purpose**: Handle failures  
**Actions**: Root cause analysis, determine loop-back, mini-RRPAI  
**Output**: Issue resolved, validation passed  
**Time**: Varies by complexity

---

## Error Handling Quick Reference

| Complexity | Example | Action |
|------------|---------|--------|
| **Trivial** | Typo, missing import | Fix immediately |
| **Simple** | Logic bug | Fix → Validate |
| **Medium** | API design flaw | ITERATE → PLAN |
| **Complex** | Architecture issue | ITERATE → RESEARCH |
| **Critical** | Security flaw | ITERATE → REVIEW + User |

See `/rrpai/iterate` for full error handling framework.

---

## Checkpoint Protocol (Mandatory)

**When to create**:
- After each complete implementation phase
- Before/after breaking changes
- At least once per day for multi-day work
- End of significant units of work

**Template**: `app/backend/.project/prompts/templates/SESSION_LOG_ENHANCED.template.md`

**Location**: `history/sessions/weekN/[feature-name]-checkpoint-N.md`

---

## Common Patterns

### Simple Bug Fix
```
REVIEW (5 min) → RESEARCH (skip) → PLAN (10 min) → 
APPROVE (skip) → IMPLEMENT (30 min) → VALIDATE (10 min)
Total: ~1 hour
```

### Major Feature (Multi-Day)
```
REVIEW (2 hours) → RESEARCH multi-model (8 hours) → 
PLAN PRD+TDD (5 hours) → APPROVE (1 hour) → 
IMPLEMENT 3 checkpoints (18 hours) → VALIDATE (3 hours)
Total: ~3-4 days
```

### Failed Validation
```
... → VALIDATE (fail) → ITERATE (root cause) → 
Loop to [appropriate phase] → ... → VALIDATE (pass) → COMPLETE
```

---

## Phase-Specific Workflows

### 📋 Detailed Phase Documentation

For complete implementation details of each phase:

1. **[Phase 1: REVIEW](file://.agent/workflows/review.md)** - Context loading, gap analysis, clarifying questions
2. **[Phase 2: RESEARCH](file://.agent/workflows/research.md)** - Web search, multi-model research, consolidation
3. **[Phase 3: PLAN](file://.agent/workflows/plan.md)** - PRD/TDD creation, checkpoint definition, artifact generation
4. **[Phase 4: APPROVE](file://.agent/workflows/approve.md)** - Approval gates, feedback handling, sign-off process
5. **[Phase 5: IMPLEMENT](file://.agent/workflows/implement.md)** - Coding, checkpoints, session logging, PM/CC protocol
6. **[Phase 6: VALIDATE](file://.agent/workflows/validate.md)** - Test pyramid, validation strategy, decision criteria
7. **[Phase 7: ITERATE](file://.agent/workflows/iterate.md)** - Root cause analysis, loop-back logic, error framework

### 🐛 Specialized Workflows

8. **[CODE REVIEW](file://.agent/workflows/code-review.md)** - PR best practices, quality gate, feedback etiquette
9. **[DEPLOY](file://.agent/workflows/deploy.md)** - Staging/production deployment, rollback procedures, migration safety
10. **[RETROSPECTIVE](file://.agent/workflows/retrospective.md)** - Sprint review, continuous improvement, action items
11. **[DEBUG](file://.agent/workflows/debug.md)** - Systematic debugging, Django-specific troubleshooting guide

---

## Tips for Success

1. **Never Skip Phases** - Even "quick fixes" benefit from REVIEW
2. **Document Everything** - Session logs prevent context loss
3. **Ask Questions Early** - Better in REVIEW than iterating at hour 10
4. **Use Checkpoints** - They're mandatory for a reason
5. **Trust the Process** - RRPAI prevents bugs through structure
6. **When in Doubt, Ask User** - Better to request approval twice

---

## Support

### Quick Commands

View specific phase:
```bash
cat .agent/workflows/review.md         # Phase 1
cat .agent/workflows/research.md       # Phase 2  
cat .agent/workflows/plan.md           # Phase 3
cat .agent/workflows/approve.md        # Phase 4
cat .agent/workflows/implement.md      # Phase 5
cat .agent/workflows/validate.md       # Phase 6
cat .agent/workflows/iterate.md        # Phase 7

# Specialized workflows
cat .agent/workflows/code-review.md    # Code review guide
cat .agent/workflows/deploy.md         # Deployment guide
cat .agent/workflows/retrospective.md  # Sprint retrospective
cat .agent/workflows/debug.md          # Debugging guide
```

View master (this file):
```bash
cat .agent/workflows/rrpai.md
```

### References

- **PM Manual**: `app/backend/.project/PROJECT_MANAGER_MANUAL.md`
- **Templates**: `app/backend/.project/prompts/templates/`
- **Session Logs**: `app/backend/.project/history/sessions/weekN/`
- **Steering Files**: `.kiro/steering/`

---

**Last Updated**: 2026-01-04  
**Version**: 3.1 (Modular Architecture)  
**Status**: Active - Use for ALL tasks  
**Structure**: Master orchestrator + 7 phase-specific workflows
