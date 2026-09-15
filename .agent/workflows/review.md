---
description: Phase 1 - Review requirements and current state
---

# Phase 1: REVIEW

**Purpose**: Understand the current state, requirements, and scope of the task.

**Time**: 15-30 minutes  
**Next Phase**: RESEARCH (if unknowns exist) or PLAN (if straightforward)

---

## Steps

### 1. Load Context Files

// turbo
```bash
cat app/backend/.project/context/QUICK_CONTEXT.md
cat app/backend/.project/planning/TODO_NOW.md
```

Check current sprint tracker:
```bash
# Replace WEEKN with current week number
cat app/backend/.project/planning/SPRINT_TRACKER_WEEKN.md
```

### 2. Role-Based Discovery Questions

**Product Lens (Priya):**
- [ ] What problem does this solve?
- [ ] Who has this problem? How many?
- [ ] How are they solving it today?
- [ ] Why would they switch?
- [ ] How does this make money?

**Technical Lens (Arjun):**
- [ ] Any existing systems to integrate with?
- [ ] Scale expectations?
- [ ] Budget and timeline constraints?
- [ ] Team size for building?

**User Lens (Zara):**
- [ ] Who are the primary users? Tech-savviness?
- [ ] Top 3 user workflows?
- [ ] Design references or competitors?

**Data Lens (Meera):**
- [ ] What data already exists?
- [ ] Privacy/compliance requirements?
- [ ] External data sources needed?

### 3. Identify Gaps

Create a gap analysis:
- What's missing in the current implementation?
- What's unclear in the requirements?
- What dependencies exist?
- What could go wrong?

### 4. Ask Clarifying Questions

**STOP and ask user if ANY of these are true**:
- [ ] Requirements are ambiguous
- [ ] Multiple valid approaches exist
- [ ] Breaking changes may be needed
- [ ] Timeline impact is uncertain
- [ ] Security or data concerns exist

Use `notify_user` tool to ask questions.

---

## Outputs

- [ ] Requirements understood (or questions asked)
- [ ] Gaps documented
- [ ] Task type identified (sprint/feature/hotfix/bug)

### Decision Log (append after each major discussion)
- ✅ **Decision Made**: [what was agreed]
- ❓ **Open Question**: [what needs more research]
- 🚫 **Rejected**: [what was dropped and why]
- 📌 **Action Item**: [what happens next]
- ⚠️ **Risk Flagged**: [new risks identified]

---

## Success Criteria

✅ **Proceed to RESEARCH when**:
- All requirements are clear OR clarifying questions sent
- Current state fully understood
- Gaps identified and documented

❌ **DON'T proceed if**:
- Requirements still unclear
- User hasn't answered critical questions
- Assumptions being made

---

## Tools & Templates

**Context files**:
- `app/backend/.project/context/QUICK_CONTEXT.md`
- `app/backend/.project/planning/TODO_NOW.md`
- `app/backend/.project/planning/SPRINT_TRACKER_WEEKN.md`

**Gap analysis**: Document in session notes or create lightweight doc

---

**Next**: [Phase 2: RESEARCH](file://.agent/workflows/research.md) or [Phase 3: PLAN](file://.agent/workflows/plan.md)  
**Back**: [Master Workflow](file://.agent/workflows/rrpai.md)
