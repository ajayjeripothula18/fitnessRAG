---
description: Sprint retrospective for continuous improvement
---

# Sprint Retrospective Workflow

**Version**: 1.0  
**Last Updated**: 2026-01-04  
**Purpose**: Continuous improvement through systematic sprint review

---

## When to Use This Workflow

### ✅ Use For:
- End of each sprint/week
- After major milestones
- When process improvements needed
- Team learning and growth

### Frequency:
- **Regular sprints**: End of each week
- **Ad-hoc**: After significant events (incidents, breakthroughs)

---

## Retrospective Structure

```
1. PREPARE   → Gather data and metrics
2. SET THE STAGE → Create safe environment
3. REVIEW     → What happened this sprint
4. ANALYZE    → What went well / what didn't
5. ACT        → Action items for next sprint
```

**Duration**: 30-60 minutes  
**Participants**: PM, CC (if applicable), User

---

## Step 1: PREPARE (Before Retrospective)

### Gather Sprint Data

#### Quantitative Metrics

**From Sprint Tracker**:
```bash
cat app/backend/.project/planning/SPRINT_TRACKER_WEEKN.md
```

**Collect**:
- [ ] Planned vs. completed features
- [ ] Number of prompts/tasks
- [ ] Blockers encountered
- [ ] Iteration loops needed

#### Qualitative Data

**From Session Logs**:
```bash
ls app/backend/.project/history/sessions/weekN/
```

**Review**:
- [ ] What challenges were faced
- [ ] What went smoothly
- [ ] Any recurring patterns
- [ ] User feedback

---

## Step 2: SET THE STAGE

### Create Safe Environment

**Retrospective principles**:
- **Blameless**: Focus on process, not people
- **Constructive**: Solutions, not just problems
- **Honest**: Speak openly about challenges
- **Action-oriented**: Must result in improvements

---

## Step 3: REVIEW (What Happened)

### Sprint Summary

**Document**:
```markdown
## Sprint Week N Summary

**Goal**: [Original sprint goal]

**Planned**: [N features]
**Completed**: [N features] (X%)

**Features Delivered**:
- ✅ [Feature 1]
- ✅ [Feature 2]
- ⏭️ [Feature 3 - pushed to next sprint]

**Unexpected Work**:
- [Hotfix 1]
- [Research task]
```

### Key Events

**Notable moments**:
- New features launched
- Bugs discovered
- Process changes
- Learning moments
- Blockers encountered

---

## Step 4: ANALYZE

### What Went Well ✅

**Categories to consider**:

**Process**:
- New workflows/tools that helped
- Effective collaboration patterns
- Good estimation accuracy
- Smooth deployments

**Technical**:
- Clean implementations
- No major bugs
- Good test coverage
- Performance improvements

**Communication**:
- Clear requirements
- Quick clarifications
- Effective handoffs

**Examples**:
```markdown
### What Went Well

**RRPAI Workflow**:
- The VALIDATE phase caught 3 bugs before deployment
- Multi-model research helped avoid wrong architectural choice

**Code Quality**:
- Test coverage reached 85% (target: 80%)
- Zero production bugs this sprint

**Collaboration**:
- User was very responsive to approval requests
- PM/CC handoff was smooth
```

---

### What Didn't Go Well ❌

**Categories to consider**:

**Process**:
- Missed steps in workflow
- Poor estimation
- Delayed approvals
- Rework needed

**Technical**:
- Bugs in production
- Performance issues
- Technical debt accumulated
- Integration problems

**Communication**:
- Unclear requirements
- Late feedback
- Misunderstandings

**Examples**:
```markdown
### What Didn't Go Well

**Estimation**:
- Feature A took 2x longer than estimated (4h → 8h)
- Didn't account for migration complexity

**Technical**:
- N+1 query problem found in production
- Should have been caught in code review

**Process**:
- Skipped code review for hotfix (bad practice)
- Deployment rollback needed due to missing env var
```

---

### Root Cause Analysis

For each significant issue, ask **"Why?"** 5 times:

**Example**:
```
Issue: Production deployment failed

Why? → Missing environment variable
Why? → Not documented in deployment checklist
Why? → Deployment workflow was rushed
Why? → Hotfix was urgent
Why? → Didn't catch bug in VALIDATE phase (tests incomplete)

Root cause: Test coverage gap for edge cases
```

---

## Step 5: ACT (Action Items)

### Create Actionable Improvements

**Good action items are**:
- **Specific**: Clear what to do
- **Measurable**: Can track completion
- **Assigned**: Someone owns it
- **Achievable**: Realistic for next sprint
- **Time-bound**: Deadline clear

**Examples**:

```markdown
## Action Items for Week N+1

| ID | Action | Owner | Priority | Deadline |
|----|--------|-------|----------|----------|
| A1 | Add edge case tests for wallet feature | PM | High | Before next deploy |
| A2 | Update deployment checklist with env vars | PM | High | This week |
| A3 | Schedule 30min session for estimation training | User | Medium | Next sprint |
| A4 | Create PR template for better reviews | PM | Low | Week N+2 |
```

### Apply to Next Sprint

**Update planning documents**:

**TODO_NOW.md**:
```markdown
## Process Improvements (from retrospective)
- [ ] A1: Add edge case tests
- [ ] A2: Update deployment checklist
```

**Next SPRINT_TRACKER**:
```markdown
## Process Improvements from Week N
- Action items from retrospective
- Estimated effort
```

---

## Retrospective Formats

### Format 1: Start/Stop/Continue

**Start**:
- What should we start doing?
- New practices to adopt

**Stop**:
- What should we stop doing?
- Wasteful activities

**Continue**:
- What's working well?
- Keep doing

---

### Format 2: Glad/Sad/Mad

**Glad**:
- What made you happy this sprint?

**Sad**:
- What disappointed you?

**Mad**:
- What frustrated you?

---

### Format 3: 4 Ls

**Liked**:
- What did you enjoy?

**Learned**:
- What did you learn?

**Lacked**:
- What was missing?

**Longed For**:
- What did you wish for?

---

## Retrospective Template

**Use this for each sprint**:

```markdown
# Sprint Retrospective: Week N

**Date**: YYYY-MM-DD  
**Sprint Goal**: [Original goal]  
**Attendees**: PM, User

---

## Sprint Summary

**Planned Features**: [N]  
**Completed Features**: [N] (X%)  
**Carry-over to Next Sprint**: [N]

**Metrics**:
- Total prompts: [N]
- Total session hours: [N]
- Blockers: [N]
- Iterations: [N]

---

## What Went Well ✅

1. [Item 1]
2. [Item 2]
3. [Item 3]

---

## What Didn't Go Well ❌

1. [Issue 1]
   - **Impact**: [How it affected sprint]
   - **Root cause**: [Why it happened]

2. [Issue 2]
   - **Impact**: ...
   - **Root cause**: ...

---

## Insights & Learnings

**Key learnings**:
- [Learning 1]
- [Learning 2]

**Patterns observed**:
- [Pattern 1]

---

## Action Items for Next Sprint

| ID | Action | Owner | Priority | Deadline |
|----|--------|-------|----------|----------|
| A1 | ... | PM | High | ... |
| A2 | ... | User | Medium | ... |

### Decision Log (append after each major discussion)
- ✅ **Decision Made**: [what was agreed]
- ❓ **Open Question**: [what needs more research]
- 🚫 **Rejected**: [what was dropped and why]
- 📌 **Action Item**: [what happens next]
- ⚠️ **Risk Flagged**: [new risks identified]

---

## Sprint Rating

**Overall**: [1-10]  
**Productivity**: [1-10]  
**Quality**: [1-10]  
**Collaboration**: [1-10]

**Comments**: [Brief overall assessment]

---

**Retrospective Completed**: ✅  
**Next Retrospective**: Week N+1
```

---

## Metrics to Track Over Time

### Sprint Velocity
- Features completed per sprint
- Trend over time (increasing/stable/decreasing)

### Quality Metrics
- Bugs found in production
- Test coverage percentage
- Code review feedback volume

### Process Metrics
- Estimation accuracy
- Cycle time (idea → production)
- Rework percentage

### Satisfaction
- Sprint rating (1-10)
- Team satisfaction

---

## Common Retrospective Anti-Patterns

### ❌ Avoid These:

**Blame game**:
- Focusing on who made mistakes
- Personal criticisms

**No action items**:
- Just talking, no improvements
- Action items too vague

**Same issues every sprint**:
- Not addressing root causes
- No follow-up on actions

**Skipping retrospectives**:
- "Too busy to improve"
- False sense that everything is fine

**Analysis paralysis**:
- Over-analyzing minor issues
- Too many action items (can't do all)

---

## Integration with RRPAI

### Retrospective Uses RRPAI

**REVIEW Phase**:
- Load sprint tracker, session logs
- Understand what happened

**RESEARCH Phase** (optional):
- If recurring issues, research solutions
- Industry best practices

**PLAN Phase**:
- Create action items
- Plan improvements for next sprint

**IMPLEMENT Phase**:
- Apply action items in next sprint

**VALIDATE Phase**:
- Check if improvements worked
- Measure impact

---

## Quick Commands

### Prepare for Retrospective

```bash
# View sprint tracker
cat app/backend/.project/planning/SPRINT_TRACKER_WEEK15.md

# List session logs
ls -lh app/backend/.project/history/sessions/week15/

# Count completed features
grep "\[x\]" app/backend/.project/planning/TODO_NOW.md | wc -l
```

### Create Retrospective Document

```bash
# Copy template
cp app/backend/.project/templates/RETROSPECTIVE_TEMPLATE.md \
   app/backend/.project/history/retrospectives/week15.md

# Edit
nano app/backend/.project/history/retrospectives/week15.md
```

---

**Last Updated**: 2026-01-04  
**Version**: 1.0  
**Frequency**: End of each sprint  
**Duration**: 30-60 minutes  
**Purpose**: Continuous improvement
