---
description: Phase 4 - Get user approval before implementation
---

# Phase 4: APPROVE

**Purpose**: Get explicit user approval before implementation begins.

**Time**: 5-60 minutes  
**Next Phase**: IMPLEMENT (if approved) or PLAN (if changes needed)

---

## Approval Gates

| Gate | Artifact | Required For |
|------|----------|--------------|
| **Gate 1: PRD** | PRD.md | Major features only |
| **Gate 2: TDD** | TDD.md | Major features only |
| **Gate 3: Plan** | All planning artifacts | ALL tasks before implementation |

---

## Steps

### 1. Create Approval Summary

#### For Major Features:
```markdown
## Ready for Approval: [Feature Name]

**Artifacts Created**:
- PRD: [link]
- TDD: [link]
- Prompts: [count] prompts ready

**Key Decisions**:
- D1: [Decision summary]
- D2: [Decision summary]

**Timeline**: [estimate]
**Session Checkpoints**: [count] checkpoints defined

**Questions**:
1. [Any remaining clarifications]
```

#### For Sprints/Smaller Tasks:
```markdown
## Ready for Implementation: [Task Name]

**Plan**: [link to prompt/plan]

**Approach**: [1-2 sentence summary]

**Timeline**: [estimate]

**Session Checkpoints**: [if applicable]
```

### 2. Request Approval

Use `notify_user` tool:
```python
notify_user(
    PathsToReview=[list of artifact paths],
    BlockedOnUser=True,
    Message="[approval summary]",
    ShouldAutoProceed=False  # Never auto-proceed for approvals
)
```

### 3. Handle Feedback

**If approved**: 
- Proceed to IMPLEMENT ✅

**If changes requested**:
- Determine scope of changes
- Loop back to appropriate phase:
  - Minor plan tweaks → Stay in PLAN, update artifacts
  - Requirements change → Loop to REVIEW
  - Approach change → Loop to RESEARCH
  - Design modifications → Update in PLAN

---

## Outputs

- [ ] User approval received
- [ ] Feedback incorporated (if any)
- [ ] Ready to implement

### Decision Log (append after each major discussion)
- ✅ **Decision Made**: [what was agreed]
- ❓ **Open Question**: [what needs more research]
- 🚫 **Rejected**: [what was dropped and why]
- 📌 **Action Item**: [what happens next]
- ⚠️ **Risk Flagged**: [new risks identified]

---

## Success Criteria

✅ **Proceed to IMPLEMENT when**:
- **Explicit user approval received**
- All feedback addressed
- No blocking questions remain

❌ **NEVER proceed if**:
- User hasn't explicitly approved
- Feedback not incorporated
- Questions remain unanswered

---

## Approval Checklist

Before requesting approval:
- [ ] All artifacts are complete
- [ ] Artifacts properly linked/referenced
- [ ] Checkpoints defined (if multi-session)
- [ ] Timeline estimate provided
- [ ] Dependencies clearly stated
- [ ] Risks identified and mitigated

---

**Next**: [Phase 5: IMPLEMENT](file://.agent/workflows/implement.md) or loop back to [Phase 3: PLAN](file://.agent/workflows/plan.md)  
**Previous**: [Phase 3: PLAN](file://.agent/workflows/plan.md)  
**Back**: [Master Workflow](file://.agent/workflows/rrpai.md)
