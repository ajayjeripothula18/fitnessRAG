---
description: Agile Ceremony - Backlog Grooming & Refinement
---

# Backlog Refinement Workflow

**Purpose**: Review the Product Backlog, break down large Epics into actionable User Stories, and ensure stories have clear Acceptance Criteria based on the Definition of Done (DoD).

## Trigger
Use this workflow when the user requests a backlog review, wants to plan future work, or when the current Sprint is running out of tasks.

## Steps

### 1. Load Context
- **Read**: `app/backend/.project/PRODUCT_BACKLOG.md`
- **Read**: `app/backend/.project/DEFINITION_OF_DONE.md`

### 2. Analyze the Backlog
- Identify any Epics that are too vague and need breaking down.
- Ensure that the top 3-5 priority stories have enough detail for an agent to execute them without ambiguity.
- Check if stories map correctly to architectural constraints (e.g., in `architecture_document.md`).

### 3. Propose Refinements
Generate a response to the user proposing changes to the backlog:

```markdown
### 📝 Backlog Refinement

I've reviewed our `PRODUCT_BACKLOG.md`. Here are my proposed refinements:

**1. [Epic/Story Name] Needs Detail:**
- Current State: [Brief description]
- Proposed Breakdown: 
  - Sub-task A
  - Sub-task B
- Acceptance Criteria needed: [Draft criteria]

**2. Priority Check:**
- Is [Story X] still a higher priority than [Story Y]?

**3. Next Actions:**
- Would you like me to update the `PRODUCT_BACKLOG.md` with these refined details?
```

### 4. Execute Changes
- Only after user approval, use file editing tools to update the `PRODUCT_BACKLOG.md` with the new, refined stories and Acceptance Criteria.
