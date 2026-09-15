---
description: Phase 2 - Research and validate solutions
---

# Phase 2: RESEARCH

**Purpose**: Gather information to address unknowns and validate the approach.

**Time**: 30 min - 4 hours (depends on type)  
**Next Phase**: PLAN

---

## Decision Tree: What Type of Research?

```
Is research needed?
├─ No unknowns → SKIP to PLAN
├─ Simple/known solution → Light (web search) - 30 min
├─ Moderate complexity → Standard (web + docs) - 1-2 hours
└─ High complexity/critical → Multi-model (external AIs) - 4-8 hours
```

---

## Research Types

### Skip Research
**When**: Solution is obvious, similar work done before  
**Action**: Skip directly to PLAN

### Light Research (Web Search)
**When**: Need best practices, API docs  
**Time**: 30 minutes  
**Tools**: Web search, official docs

### Standard Research  
**When**: Architectural decisions, new libraries  
**Time**: 1-2 hours  
**Tools**: Web search + knowledge base + V1/V2 code review

### Multi-Model Research ⭐
**When ANY apply**:
- [ ] Architectural decision affecting multiple components
- [ ] Security or payment features
- [ ] Core user flows (booking, authentication)
- [ ] MVP timeline impact > 1 week
- [ ] Confidence level < 80% after standard research

**Time**: 4-8 hours  
**Models**: Perplexity + ChatGPT + Gemini + Claude

---

## Multi-Model Research Process

### Step 1: Create Research Prompts
**Location**: `.project/research_outputs/[topic]/`

**Template**: `app/frontend-research/templates/EXECUTION_GUIDE_TEMPLATE.md`

### Step 2: Execute Across Models

| Model | Focus | Time |
|-------|-------|------|
| **Perplexity** | Benchmarks, trends, competitor analysis | 45-90 min |
| **ChatGPT** | Code examples, implementation details | 60-90 min |
| **Gemini** | Strategic analysis, trade-offs, risks | 60-75 min |
| **Claude** | Synthesis, comprehensive analysis, QA | 75-95 min |

### Step 3: Consolidate Findings

**Template**: `app/frontend-research/templates/CONSOLIDATION_TEMPLATE.md`

**Create**: `.project/research_outputs/[topic]/CONSOLIDATED_FINDINGS.md`

**Must include**:
- [ ] Common agreements across models
- [ ] Conflicting opinions with analysis
- [ ] Recommended approach with confidence %
- [ ] Implementation implications
- [ ] Timeline impact

---

## Standard Research Steps

### Web Search
```bash
# Search for:
# - Best practices (2024-2025 articles)
# - Framework/library documentation
# - Performance benchmarks
# - Security considerations
```

### Check Knowledge Base
- Previous research outputs (`.project/research_outputs/`)
- V1/V2 implementations
- Session logs from similar features

### Review Existing Code
// turbo
```bash
grep -r "similar_pattern" app/backend/apps/
```

---

## Outputs

- [ ] Research findings documented
- [ ] Consolidated report (if multi-model)
- [ ] Confidence level stated (%)
- [ ] Recommended approach clear

### Decision Log (append after each major discussion)
- ✅ **Decision Made**: [what was agreed]
- ❓ **Open Question**: [what needs more research]
- 🚫 **Rejected**: [what was dropped and why]
- 📌 **Action Item**: [what happens next]
- ⚠️ **Risk Flagged**: [new risks identified]

---

## Success Criteria

✅ **Proceed to PLAN when**:
- All unknowns addressed
- Solutions validated
- **Confidence ≥ 80%** for critical decisions
- **Confidence ≥ 60%** for non-critical decisions

❌ **DON'T proceed if**:
- Key unknowns remain
- Confidence too low
- Conflicting information not resolved

---

## Tools & Templates

**Multi-model templates**:
- `app/frontend-research/templates/EXECUTION_GUIDE_TEMPLATE.md`
- `app/frontend-research/templates/CONSOLIDATION_TEMPLATE.md`

**Research storage**:
- `.project/research_outputs/[topic]/`

---

**Next**: [Phase 3: PLAN](file://.agent/workflows/plan.md)  
**Previous**: [Phase 1: REVIEW](file://.agent/workflows/review.md)  
**Back**: [Master Workflow](file://.agent/workflows/rrpai.md)
