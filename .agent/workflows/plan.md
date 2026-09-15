---
description: Phase 3 - Create comprehensive implementation plan
---

# Phase 3: PLAN

**Purpose**: Create a comprehensive, actionable implementation plan.

**Time**: 30 min - 5 hours (depends on task type)  
**Next Phase**: APPROVE

---

## Task Type Routing

Select planning approach based on task type:

| Task Type | Artifacts | Time |
|-----------|-----------|------|
| **Major Feature** | PRD + TDD + Prompts | 2-4 hours |
| **Sprint** | Tracker + Decisions + Prompts | 3-5 hours |
| **Single API** | Spec + Prompt | 30-60 min |
| **Hotfix** | Implementation Plan | 15-30 min |
| **Bug Fix** | Debugging Prompt | 20-40 min |

---

## Major Feature Planning

### Step 1: Create PRD
**Template**: `app/backend/.project/templates/PRD_TEMPLATE.md`

**Must include**:
- [ ] User stories with acceptance criteria
- [ ] Functional requirements (prioritized: Must/Should/Nice)
- [ ] Non-functional requirements (performance, security)
- [ ] Business rules
- [ ] Success metrics
- [ ] Dependencies
- [ ] Risks & assumptions

### Step 2: Create TDD
**Template**: `app/backend/.project/templates/TDD_TEMPLATE.md`

**Must include**:
- [ ] Architecture diagrams
- [ ] Data model changes
- [ ] API design (request/response)
- [ ] Implementation phases
- [ ] Testing strategy
- [ ] Security considerations
- [ ] Performance considerations

### Step 3: Create Implementation Prompt
**Template**: `app/backend/.project/prompts/templates/IMPLEMENTATION_PROMPT.template.md`

---

## Sprint Planning

### Step 1: Create Sprint Tracker
**Location**: `app/backend/.project/planning/SPRINT_TRACKER_WEEKN.md`

**Must include**:
- [ ] Sprint goal
- [ ] Feature lifecycle table
- [ ] Prompt-to-result tracking
- [ ] **Session checkpoint plan**

### Step 2: Document Decisions
**Create**: `.project/planning/WEEKN_DECISIONS.md`

```markdown
| ID | Question | Research | Decision | Implementation |
|----|----------|----------|----------|----------------|
| D1 | [Question] | [Findings] | [Choice] | [How] |
```

### Step 3: Create ALL Prompts in ONE Session
⚠️ **CRITICAL**: Generate all prompts together to preserve context.

**Naming**: `prompts/weekN/01_FEATURE.md`, `02_NEXT.md`, etc.

---

## Session Checkpoint Planning (MANDATORY)

For multi-session work (>4 hours), define checkpoints:

**Checkpoint criteria**:
- After each major component
- Before/after breaking changes
- At least once per day for multi-day work
- Testable unit of work complete

**Example for 3-day feature**:
- Day 1: Database models + migrations → Checkpoint 1
- Day 2: API endpoints + serializers → Checkpoint 2
- Day 3: Tests + documentation → Final

---

## Update Tracking Files

```bash
# Update TODO_NOW.md with current task
# Update SPRINT_TRACKER with new feature
# For decisions, update DECISION_LOG.md
```

---

## Planning Outputs

### Artifact Ownership
- PRD: Product perspective (user stories, acceptance criteria, MVP scope)
- TDD: Technical perspective (architecture, data model, API contracts)
- UX Plan: User perspective (flows, wireframes, design system)
- Test Strategy: Quality perspective (test pyramid, edge cases, performance)
- Sprint Plan: Process perspective (epics → stories → tasks, checkpoints)

### AI-Coding Readiness Checklist (Before Phase 4)
- [ ] Clear, unambiguous specifications
- [ ] Well-defined interfaces and contracts
- [ ] Modular, independently implementable components
- [ ] Explicit edge cases and error handling specs
- [ ] Code-ready acceptance criteria
- [ ] File structure and naming conventions documented

**For Major Features**:
- [ ] PRD created
- [ ] TDD created
- [ ] Implementation prompt created
- [ ] Checkpoints defined

**For Sprints**:
- [ ] Sprint tracker created
- [ ] Decisions documented
- [ ] All prompts created
- [ ] Checkpoint plan defined

**For All Tasks**:
- [ ] TODO_NOW.md updated
- [ ] SPRINT_TRACKER updated
- [ ] DECISION_LOG.md updated (if applicable)

### Decision Log (append after each major discussion)
- ✅ **Decision Made**: [what was agreed]
- ❓ **Open Question**: [what needs more research]
- 🚫 **Rejected**: [what was dropped and why]
- 📌 **Action Item**: [what happens next]
- ⚠️ **Risk Flagged**: [new risks identified]

---

## Success Criteria

✅ **Proceed to APPROVE when**:
- Plan is comprehensive and specific
- Verification strategy is clear
- All artifacts properly structured
- Dependencies identified
- **Checkpoints defined** (if multi-session)

❌ **DON'T proceed if**:
- Plan is vague or incomplete
- No clear verification strategy
- Checkpoints not defined for multi-session work

---

## Tools & Templates

**Major Feature**:
- `app/backend/.project/templates/PRD_TEMPLATE.md`
- `app/backend/.project/templates/TDD_TEMPLATE.md`

**Implementation**:
- `app/backend/.project/prompts/templates/IMPLEMENTATION_PROMPT.template.md`
- `app/backend/.project/prompts/templates/DEBUGGING_PROMPT.template.md`

**Tracking**:
- `app/backend/.project/planning/TODO_NOW.md`
- `app/backend/.project/planning/SPRINT_TRACKER_WEEKN.md`
- `app/backend/.project/planning/DECISION_LOG.md`

---

**Next**: [Phase 4: APPROVE](file://.agent/workflows/approve.md)  
**Previous**: [Phase 2: RESEARCH](file://.agent/workflows/research.md)  
**Back**: [Master Workflow](file://.agent/workflows/rrpai.md)
