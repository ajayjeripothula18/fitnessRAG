---
description: Agile Ceremony - Sprint Planning
---

# Sprint Planning Workflow

**Purpose**: Kick off a new sprint by pulling prioritized items from the Product Backlog, estimating effort, defining the Sprint Goal, and generating the Sprint Tracker.

## Trigger
Use this workflow at the start of a project, or when the previous sprint is closed out.

## Steps

### 1. Load Context
- **Read**: `app/backend/.project/PRODUCT_BACKLOG.md`
- **Check**: Does `history/sessions/weekN/SPRINT_TRACKER.md` already exist for the upcoming week?

### 2. Formulate the Sprint Plan
- Identify the highest priority Epic or group of cohesive User Stories.
- Determine a realistic **Sprint Goal** based on a 1-2 week capacity for the AI agent team.
- Select the specific stories to include in the sprint.

### 3. Present the Plan
Present the proposed sprint to the user:

```markdown
### 🏃 Sprint Planning

**Proposed Sprint Goal:** [Clear, single sentence goal]

**Stories to Pull:**
1. [Story Name] (Priority: High)
2. [Story Name] (Priority: Medium)
...

**Capacity Check:**
- This feels like a healthy amount of work for a 1-2 week sprint, allowing time for TDD and validation.

**Next Steps:**
- Do you approve this Sprint Backlog? Once approved, I will generate the `SPRINT_TRACKER.md` and we can move to the `/implement` phase.
```

### 4. Execute Planning Setup
- Upon user approval, create or update `app/backend/.project/history/sessions/weekN/SPRINT_TRACKER.md` with the selected stories in the TODO column.
- Update `PRODUCT_BACKLOG.md` if necessary to mark stories as "In Active Sprint".
