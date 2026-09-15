---
description: Code review workflow for quality assurance and knowledge sharing
---

# Code Review Workflow

**Version**: 1.0  
**Last Updated**: 2026-01-04  
**Purpose**: Quality gate between IMPLEMENT and VALIDATE phases

---

## When to Use This Workflow

### ✅ Use For:
- All production code before merging
- Self-review before requesting peer review
- Quality assurance checkpoint
- Knowledge sharing and learning

### ❌ Skip For:
- Experimental/spike code (not for production)
- Documentation-only changes (minor)
- Hotfixes in emergency (but review post-merge)

---

## Code Review in RRPAI Flow

```
IMPLEMENT → CODE REVIEW → VALIDATE → (if pass) → DEPLOY

If code review finds issues:
├─ Minor (style, comments) → Fix and re-review
└─ Major (logic, architecture) → ITERATE → PLAN
```

**Position**: Quality gate after implementation, before testing

---

## The 5-Step Review Process

```
1. PREPARE → Self-review and organize changes
2. SUBMIT → Create PR with clear context
3. REVIEW → Systematic code inspection
4. DISCUSS → Address feedback collaboratively
5. APPROVE → Merge when ready
```

---

## Step 1: PREPARE (Self-Review)

### Purpose
Catch obvious issues before others review.

### Self-Review Checklist

Before creating PR, review your own code:

#### Functionality
- [ ] Code does what it's supposed to do
- [ ] Edge cases handled
- [ ] Error handling present
- [ ] No obvious bugs

#### Code Quality
- [ ] Follows project conventions (PEP 8 for Python)
- [ ] Functions/classes have clear names
- [ ] Complex logic has comments
- [ ] No commented-out code (remove or explain)
- [ ] No TODO comments (create issues instead)

#### Tests
- [ ] Unit tests written and passing
- [ ] Test coverage is adequate (>80% for new code)
- [ ] Edge cases tested

#### Documentation
- [ ] Docstrings for functions/classes
- [ ] README updated (if needed)
- [ ] API docs updated (if API changed)

#### Dependencies
- [ ] No unnecessary dependencies added
- [ ] requirements.txt updated (if packages added)
- [ ] Migrations created (if models changed)

---

## Step 2: SUBMIT (Create Pull Request)

### PR Best Practices

#### Small and Focused
- **Ideal size**: <400 lines of code changed
- If larger, break into multiple PRs

#### Clear Title and Description

**Title format**: `<type>: <clear description>`

Examples:
- `feat: Add wallet recharge API endpoint`
- `fix: Correct GST calculation for inter-state bookings`
- `refactor: Simplify agency model structure`

**Description template**:
```markdown
## What
[Brief description of changes]

## Why
[Problem being solved or feature being added]

## How
[Approach taken]

## Testing
[How to test these changes]

## Checklist
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] Migrations created (if needed)
- [ ] Manual testing completed
```

#### Link Related Issues
```markdown
Closes #123
Relates to #456
```

---

## Step 3: REVIEW (Inspect Code)

### For Reviewers

#### Review Mindset
- **Be kind**: Remember there's a person behind the code
- **Be specific**: Vague feedback isn't helpful
- **Be constructive**: Suggest alternatives, not just problems
- **Be thorough but fast**: Aim to review within 24 hours

#### Review Checklist

**Architecture & Design**:
- [ ] Changes align with project architecture
- [ ] No unnecessary complexity
- [ ] Reusable where appropriate
- [ ] Follows SOLID principles

**Logic & Correctness**:
- [ ] Logic is sound
- [ ] Edge cases considered
- [ ] No potential bugs
- [ ] Handles errors properly

**Code Quality**:
- [ ] Readable and maintainable
- [ ] Follows coding standards
- [ ] Appropriate abstractions
- [ ] DRY (Don't Repeat Yourself)

**Testing**:
- [ ] Tests are comprehensive
- [ ] Tests cover edge cases
- [ ] Tests are maintainable
- [ ] No flaky tests

**Security**:
- [ ] No SQL injection vulnerabilities
- [ ] Authentication/authorization correct
- [ ] Sensitive data not logged
- [ ] Input validation present

**Performance**:
- [ ] No obvious performance issues
- [ ] Database queries optimized (N+1 checked)
- [ ] Caching used where appropriate

---

## Step 4: DISCUSS (Address Feedback)

### Feedback Etiquette

#### Giving Feedback
**Good examples**:
```
✅ "Consider using a list comprehension here for better readability:
   `[x.id for x in items]` instead of the current loop."

✅ "This function is doing too much. Could we split the validation 
   logic into a separate validate_input() function?"

✅ "Great approach! Small suggestion: we could cache this query result
   since the data rarely changes."
```

**Bad examples**:
```
❌ "This is wrong."
❌ "Why did you do it this way?"
❌ "Just use a list comprehension."
```

#### Receiving Feedback
- **Stay open-minded**: Feedback improves the code
- **Ask questions**: If unclear, ask for clarification
- **Push back respectfully**: It's okay to disagree with reasoning
- **Thank reviewers**: They're spending time to help

#### Comment Types

**Use labels** to clarify intent:
- `nit:` - Nitpick, not blocking (style, minor preference)
- `question:` - Seeking clarification
- `suggestion:` - Optional improvement
- `blocker:` - Must be addressed before approval

Examples:
```
nit: Missing trailing comma in this list (not blocking)

question: Is there a reason we're not using the existing helper function?

suggestion: Could add a comment explaining this algorithm

blocker: This will cause a 500 error if agency is None
```

---

## Step 5: APPROVE (Merge When Ready)

### Approval Criteria

**Required for approval**:
- [ ] All conversations resolved
- [ ] No blocking comments remain
- [ ] Tests passing (automated checks green)
- [ ] At least 1 approval received
- [ ] Changes reviewed by code owner (if applicable)

### Merging

**Pre-merge checks**:
```bash
# Pull latest main
git checkout main
git pull origin main

# Merge main into branch
git checkout feature-branch
git merge main

# Resolve conflicts if any
# Run tests
python manage.py test

# Push
git push origin feature-branch
```

**Merge strategy**:
- **Squash merge**: For feature branches (cleaner history)
- **Merge commit**: For long-lived branches

**Post-merge**:
- Delete feature branch
- Update tracking (mark task complete)

---

## Common Review Scenarios

### Scenario 1: Self-Review Before PR

```bash
# Review your changes
git diff main...feature-branch

# Check what files changed
git diff --stat main...feature-branch

# Review each commit
git log main..feature-branch --oneline
```

**Ask yourself**:
- Would I be comfortable reviewing this code?
- Is the context clear for a reviewer?
- Have I tested all scenarios?

### Scenario 2: Requesting Changes

When requesting changes:
1. Be specific about what needs to change
2. Explain why it matters
3. Suggest an alternative approach (if you have one)
4. Indicate severity (blocker vs. nit)

### Scenario 3: Disagreeing with Feedback

If you disagree:
1. Explain your reasoning
2. Ask questions to understand reviewer's perspective
3. Suggest alternatives
4. Escalate to team discussion if needed (rare)

### Scenario 4: Large PR Review

For large PRs (>400 lines):
1. Review in multiple passes:
   - Pass 1: Architecture and design
   - Pass 2: Logic and correctness
   - Pass 3: Details and style
2. Focus on high-risk areas first
3. Suggest breaking into smaller PRs for future

---

## GitHub PR Features

### Inline Comments
```
Comment on specific lines for precise feedback
Suggest changes directly (GitHub will create a commit)
```

### Review Status
- **Comment**: General feedback, no approval decision
- **Approve**: Code is ready to merge
- **Request changes**: Must be addressed before merge

### Draft PRs
- Use for work-in-progress
- Get early feedback
- Mark as "Ready for review" when complete

---

## Integration with RRPAI

### In IMPLEMENT Phase

**Before finishing IMPLEMENT**:
- Self-review code
- Ensure it's review-ready

### In CODE REVIEW Phase (New)

**This phase** - quality gate:
- Create PR
- Get feedback
- Address comments

### In VALIDATE Phase

**After code review passed**:
- Run full test suite
- Perform integration testing
- E2E validation

**If major issues found in VALIDATE**:
- Don't go back to CODE REVIEW
- Use ITERATE phase instead

### Decision Log (append after each major discussion)
- ✅ **Decision Made**: [what was agreed]
- ❓ **Open Question**: [what needs more research]
- 🚫 **Rejected**: [what was dropped and why]
- 📌 **Action Item**: [what happens next]
- ⚠️ **Risk Flagged**: [new risks identified]

---

## Quick Reference

### PR Size Guide
- **Small**: <100 lines → Ideal
- **Medium**: 100-400 lines → Good
- **Large**: 400-1000 lines → Break up if possible
- **Huge**: >1000 lines → Definitely break up

### Review Time Budget
- Small PR: 10-20 min
- Medium PR: 30-60 min
- Large PR: 1-2 hours (or reject and ask to split)

### Comment Response Time
- **Target**: Within 24 hours
- **Maximum**: 48 hours

---

## Tools & Commands

### Git Commands
```bash
# Create branch for feature
git checkout -b feature/wallet-recharge

# Push branch
git push -u origin feature/wallet-recharge

# Update with main
git fetch origin
git merge origin/main

# Interactive rebase (clean up commits)
git rebase -i main
```

### GitHub CLI (Optional)
```bash
# Create PR
gh pr create --title "feat: Add wallet recharge" --body "..."

# View PR
gh pr view 123

# Approve PR
gh pr review 123 --approve

# Merge PR
gh pr merge 123 --squash
```

---

**Last Updated**: 2026-01-04  
**Version**: 1.0  
**Integrated with**: RRPAI v3.1  
**Next**: `/rrpai/validate` after approval
