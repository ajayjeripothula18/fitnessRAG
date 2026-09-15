---
description: Phase 7 - Handle validation failures and course corrections
---

# Phase 7: ITERATE

**Purpose**: Handle validation failures and course corrections through systematic root cause analysis.

**Time**: Varies by complexity  
**Next Phase**: Loop back to appropriate phase, then eventually VALIDATE again

---

## When to Enter ITERATE

### ✅ Triggers (Use ITERATE For):
- ❌ Major test failures (>3 failures or fundamental issues)
- ❌ Design approach proven wrong
- ❌ Requirements misunderstood
- ❌ Blocker issues discovered
- ❌ Performance beyond acceptable range

### ❌ DON'T Use ITERATE For:
- ✅ 1-2 minor bugs (back to IMPLEMENT instead)
- ✅ Simple fixes or polish (back to IMPLEMENT instead)
- ✅ Trivial errors like typos (fix immediately)

---

## Root Cause Analysis

### Step 1: Identify WHAT Went Wrong

```
Failure Type?
├─ Requirements misunderstood → Gap in REVIEW phase
├─ Technology choice wrong → Gap in RESEARCH phase
├─ Design has structural flaws → Gap in PLAN phase
├─ Implementation bugs → Gap in IMPLEMENT phase
└─ Testing was incomplete → Gap in VALIDATE phase
```

### Step 2: Identify WHY

- Were clarifying questions not asked?
- Was research insufficient?
- Was planning rushed?
- Was implementation not following plan?
- Were edge cases not considered?

---

## Iteration Decision Tree

```
Root Cause Complete?
│
├─ Requirements Gap → Loop to REVIEW
│   └─ Re-run: REVIEW → RESEARCH → PLAN → APPROVE → IMPLEMENT → VALIDATE
│
├─ Research Gap → Loop to RESEARCH
│   └─ Re-run: RESEARCH → PLAN → APPROVE → IMPLEMENT → VALIDATE
│
├─ Design Flaw → Loop to PLAN
│   └─ Re-run: PLAN → APPROVE → IMPLEMENT → VALIDATE
│
└─ Implementation Bug → Loop to IMPLEMENT
    └─ Re-run: IMPLEMENT → VALIDATE
```

---

## Iteration Types

| Type | Loop To | Example | Time |
|------|---------|---------|------|
| **Hot Fix** | IMPLEMENT | Typo, missing field | <30 min |
| **Rework** | PLAN | Wrong API structure | 2-4 hours |
| **Re-research** | RESEARCH | Library limitations | 1-2 hours |
| **Re-scope** | REVIEW | Misunderstood user need | 1-3 hours |

---

## Iteration Process

### 1. Document Root Cause

Update session log:
```markdown
## Iteration Triggered

**Trigger**: [What failed - be specific]

**Root Cause**: [Why it failed]

**Type**: Hot Fix / Rework / Re-research / Re-scope

**Loop Back To**: REVIEW / RESEARCH / PLAN / IMPLEMENT

**Estimated Fix Time**: [hours]
```

### 2. Update Sprint Tracker

```markdown
## Blockers
| Issue | Root Cause | Resolution Plan | Status |
|-------|------------|-----------------|--------|
| [Issue] | [Cause] | Loop back to [PHASE] | In Progress |
```

### 3. Determine User Notification

**Notify user if ANY of these**:
- [ ] Iteration will take >2 hours
- [ ] Requires breaking changes
- [ ] Impacts timeline significantly
- [ ] Changes user-approved plan substantially
- [ ] Uncertainty remains after analysis

Use `notify_user` tool to inform user.

### 4. Execute Mini-RRPAI Cycle

Start from identified phase:
- Requirements gap → Full RRPAI from REVIEW
- Research gap → RESEARCH → PLAN → IMPLEMENT → VALIDATE
- Design flaw → PLAN → APPROVE → IMPLEMENT → VALIDATE
- Implementation bug → IMPLEMENT → VALIDATE

**Always end at VALIDATE** - never skip validation after iteration

---

## Error Complexity Framework

| Complexity | Characteristics | Action |
|------------|----------------|--------|
| **Trivial** | Syntax, typo, import | Fix immediately, no RRPAI |
| **Simple** | Logic bug, wrong field | IMPLEMENT → VALIDATE |
| **Medium** | API design flaw | ITERATE → PLAN |
| **Complex** | Architecture issue | ITERATE → RESEARCH |
| **Critical** | Security, data integrity | ITERATE → REVIEW + User escalation |

---

## Iteration Outputs

- [ ] Root cause documented in session log
- [ ] Iteration type identified
- [ ] Loop-back phase determined
- [ ] Sprint tracker updated
- [ ] User notified (if criteria met)
- [ ] Mini-RRPAI executed
- [ ] Validation re-run

### Decision Log (append after each major discussion)
- ✅ **Decision Made**: [what was agreed]
- ❓ **Open Question**: [what needs more research]
- 🚫 **Rejected**: [what was dropped and why]
- 📌 **Action Item**: [what happens next]
- ⚠️ **Risk Flagged**: [new risks identified]

---

## Success Criteria

✅ **Iteration Complete When**:
- Root cause fully understood
- Appropriate phase loop-back executed
- All RRPAI phases re-executed from loop-back point
- **Validation passed**
- Issue resolved and documented

---

## User Escalation Criteria

Escalate immediately if ANY apply:
- [ ] Fix will take >2 hours
- [ ] Requires breaking changes
- [ ] Impacts timeline significantly
- [ ] Security or data concerns
- [ ] Uncertainty > 20%

---

**Next**: Loop back to [appropriate phase], end at VALIDATE  
**Previous**: [Phase 6: VALIDATE](file://.agent/workflows/validate.md)  
**Back**: [Master Workflow](file://.agent/workflows/rrpai.md)
