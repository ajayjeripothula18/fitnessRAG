# FitnessRAG — Engineering Operating Model

## v1.0 — Final Draft Pending Repository Adoption

**Status:** Ready for adoption after independent review

**Scope:** Agile/Scrum delivery + professional software-engineering practices + AI-assisted development

> This document defines the operating model for FitnessRAG. The legacy RRPAI workflow is not the methodology. Existing RRPAI files are project history/process material and will be assessed during current-state recovery.

---

## 1. Purpose

FitnessRAG is a real software project and a deliberate engineering-training environment.

The objective is to practice a professional product-development lifecycle without allowing AI to hide the engineering process:

```text
Product Goal
→ Product Backlog
→ Refinement
→ Sprint Planning
→ Development
→ Tests
→ Pull Request
→ CI
→ Review
→ Merge
→ Release/Deployment
→ Feedback
→ Sprint Review
→ Retrospective
→ Next Sprint
```

The workflow should optimize for:

- clear requirements,
- small batches,
- frequent integration,
- automated validation,
- reviewable changes,
- traceability,
- reproducibility,
- security,
- learning.

AI accelerates the workflow; it does not replace engineering accountability.

---

## 2. Methodology

### 2.1 Scrum is the delivery framework

The current official Scrum Guide is the authority for Scrum concepts.

Scrum defines the Scrum Team, accountabilities, Product Goal, Product Backlog, Sprint Goal, Sprint Backlog, Increment, Sprint Planning, Daily Scrum, Sprint Review, Sprint Retrospective, and Definition of Done.

The Product Backlog is the ordered set of work for the product. Backlog refinement is an ongoing activity, not a mandatory standalone event.

Reference:
https\://scrumguides.org/scrum-guide.html

### 2.2 Engineering practices sit alongside Scrum

Scrum does not prescribe:

- Git branching,
- pull requests,
- CI/CD,
- test frameworks,
- deployment platforms,
- code-review mechanics,
- AI coding assistants.

Those are engineering practices layered onto the delivery framework.

The target engineering culture favors:

- version control,
- continuous integration,
- small changes,
- fast feedback,
- automated checks,
- code review,
- reproducible environments,
- secure secret handling,
- observable delivery.

References:

- https\://dora.dev/research/2025/dora-report/
- https\://dora.dev/capabilities/working-in-small-batches/
- https\://dora.dev/capabilities/version-control/

### 2.3 Solo-project adaptation

FitnessRAG currently has one human developer plus AI tools.

We will not pretend that this is a normal multi-person Scrum Team.

Scrum concepts will be practiced where they create useful learning and delivery discipline. Where a Scrum event requires genuine collaboration between people, the adaptation will be named explicitly rather than presented as an equivalent.

---

## 3. Roles

### 3.1 AJ — Developer

AJ is the human Software Developer.

Responsibilities:

- understand requirements,
- question ambiguity,
- implement work,
- write/update tests,
- inspect AI-generated changes,
- run validation,
- create pull requests,
- respond to review feedback,
- make final engineering decisions,
- maintain quality.

AI does not transfer accountability away from AJ.

### 3.2 Claude.ai — Product/Delivery Facilitator

Claude.ai is the product/delivery AI facilitator.

It can perform functions associated with:

- Product Owner,
- Scrum Master,
- project coordination.

It helps manage:

- Product Goal,
- backlog ordering,
- refine issues,
- Sprint Planning,
- progress tracking,
- Sprint Review preparation,
- Retrospective facilitation,
- blockers and risks.

Because the project is solo, Claude.ai is not treated as an independent human stakeholder.

It should surface trade-offs and unresolved questions rather than fabricate negotiations between AI personas.

### 3.3 Claude Code — Engineering Assistant

Claude Code operates inside the local development environment.

It assists with:

- repository inspection,
- implementation,
- test creation,
- local validation,
- debugging,
- Git operations,
- PR preparation.

Claude Code works from an accepted work item.

It must not silently expand scope.

It must not claim tests, CI, or deployment succeeded without evidence.

Reference:
https\://docs.anthropic.com/en/docs/claude-code/overview

### 3.4 ChatGPT — Optional Concept Tutor

ChatGPT is not a process authority.

It may explain:

- Git,
- testing,
- CI/CD,
- architecture,
- code review,
- debugging,
- other engineering concepts.

The repository operating model remains authoritative.

ChatGPT should not independently redesign the team's workflow during normal execution.

---

## 4. Systems of Record

### 4.1 GitHub Issues + Projects — work management

GitHub is the source of truth for current work management.

Use:

- Issues → individual work items,
- Projects → backlog/cycle views and planning,
- milestones/projects → larger product groupings where useful.

GitHub Projects is designed to integrate issues and pull requests and can provide table, board and roadmap views.

References:

- https\://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/about-projects
- https\://docs.github.com/en/issues/tracking-your-work-with-issues/learning-about-issues/about-issues

### 4.2 Git / GitHub — engineering history

GitHub/Git is authoritative for:

- source code,
- branches,
- commits,
- pull requests,
- code-review discussion,
- CI evidence,
- release history.

### 4.3 Repository documentation — durable knowledge

The repository is authoritative for durable engineering knowledge:

- requirements/specifications,
- architecture,
- ADRs,
- API contracts,
- testing strategy,
- development workflow,
- operations,
- security guidance,
- AI-agent instructions.

Recommended home:

```text
docs/

```

The Engineering Operating Model itself must live in the repository and be version controlled.

### 4.4 Document authority over live sessions

The version of this document committed to `docs/` is authoritative.

If guidance from Claude.ai, Claude Code, or ChatGPT in a live session conflicts with the committed document, the committed document governs until a new version is explicitly committed and adopted. No session may silently redefine the operating model.

### 4.5 Session logs — continuity only

Session logs preserve AI context across sessions.

They are not a source of truth for:

- current requirements,
- current work status,
- Git state,
- accepted architecture decisions,
- completed functionality.

Current repository and work-management evidence takes precedence over old session summaries.

---

## 5. Product Backlog

The Product Backlog is the ordered set of current work for FitnessRAG.

Work may include:

- features,
- bugs,
- technical debt,
- infrastructure improvements,
- security work,
- research/spikes,
- operational improvements.

Do not recreate historical work that is already represented by Git history.

Only unfinished, relevant, or future work should be normalized into the active backlog.

### 5.1 Work in progress

Work on one issue at a time. Do not open a second branch before the current PR is merged, closed, or explicitly parked with a documented reason.

---

## 6. Issue Design

Different work types should use appropriately sized templates.

### 6.1 Feature issue

A feature issue should normally include:

```text
Problem / Goal
User or business value
Acceptance Criteria
Scope
Out of Scope
Dependencies
Risks / Constraints
Validation expectations
Relevant technical context
```

### 6.2 Bug / chore issue

A bug or small chore should use a lighter structure:

```text
Problem
Expected behavior / desired outcome
Acceptance Criteria
Relevant context
```

The issue should be small enough to understand and review.

Large work should be decomposed into related issues or sub-issues where useful.

GitHub recommends breaking large issues into smaller pieces because smaller work is easier to manage and typically produces smaller pull requests.

Reference:
https\://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/best-practices-for-projects

---

## 7. Definition of Ready

Scrum does not require a formal Definition of Ready.

For this project, an item is **Ready for Sprint selection** when it is sufficiently understood to be actionable.

Minimum expectations:

- clear problem/goal,
- testable acceptance criteria,
- scope understood,
- major dependencies/risks known,
- small enough for the intended Sprint.

### Sizing safeguard

If an issue cannot be reasonably sized against the available Sprint hours, it is not Ready yet.

Sizing exists to prevent overcommitment, not to measure developer productivity.

---

## 8. Estimation

Story points are optional.

When used:

- they are an estimation aid,
- they are not a productivity score,
- they should support Sprint planning.

We will not enforce arbitrary rules such as "every issue must be five points or less."

The practical objective is:

> work is small enough to complete and validate within the Sprint.

---

## 9. Sprint Cadence

### Default

**One-week Sprint.**

This is a training choice based on approximately 10–15 hours/week.

The purpose is to maximize complete development-cycle repetitions.

A one-week Sprint is not being presented as universally superior to other Sprint lengths.

### Sprint Planning

At the beginning of the Sprint:

1. Review Product Goal and backlog order.
2. Select a manageable set of work.
3. Establish one Sprint Goal.
4. Confirm acceptance criteria and dependencies.
5. Check realistic capacity.
6. Create the Sprint Backlog.

Do not intentionally plan 100% of available capacity.

### Daily Engineering Update

Because this is a solo project, a self-talk Daily Scrum is not presented as a genuine multi-person Scrum event.

Instead, maintain a lightweight daily engineering update:

```text
Done:
Next:
Blocked:
```

Use this for inspection and continuity.

### Sprint Review

At Sprint end:

- inspect the Increment,
- demonstrate or summarize completed work,
- record incomplete work,
- capture relevant feedback,
- update the backlog.

### Retrospective

At Sprint end:

```text
What worked?
What created friction?
What one concrete change should we make next Sprint?
```

Retrospective actions should be actionable and tracked when they create real work.

---

## 10. Branching Strategy

Use a simple single-mainline model:

```text
main
 ↑
short-lived feature/fix/chore branch
 ↑
developer work
```

Examples:

```text
feature/123-user-profile
bugfix/124-ingestion-rollback
chore/125-ci-cleanup
```

The number is the GitHub Issue number.

A permanent `develop` branch is not required for this solo project.

The project favors short-lived branches and frequent integration rather than GitFlow-style long-lived branches.

---

## 11. Pull Request Workflow

Normal flow:

```text
Issue
→ Ready
→ branch
→ implementation
→ tests
→ PR
→ CI
→ review
→ fix/retest
→ merge
→ issue closes
```

Use GitHub's issue/PR linking and closing behavior so the work item remains traceable.

Reference:
https\://docs.github.com/en/issues/tracking-your-work-with-issues/learning-about-issues/about-issues

### PR content

A focused PR should communicate:

- what changed,
- why,
- implementation approach,
- tests performed,
- evidence/results,
- risk/operational impact,
- documentation/migration impact.

### PR size guideline

Prefer small, reviewable PRs.

As a soft guideline, flag PRs approaching or exceeding roughly **400 changed lines** for possible splitting.

This is a review heuristic, not a hard engineering limit. Some changes naturally exceed it.

### Handling a broken `main`

If `main` breaks after merge, revert the offending commit immediately via `git revert`, then open a bug issue for the proper fix. Do not attempt a forward-fix under pressure on top of a known-broken `main`.

---

## 12. Code Review in a Solo AI-Assisted Project

A solo project cannot truthfully claim a human peer review when no human peer reviewed the change.

Therefore distinguish:

### AI review

An independent AI review context can inspect:

- correctness,
- requirements,
- maintainability,
- security,
- tests,
- unnecessary complexity.

### Human developer acceptance

AJ remains responsible for reviewing the feedback, understanding the change, and deciding whether it is acceptable.

### Future human review

If another human collaborator joins the project, human peer review becomes the preferred review mechanism.

The project should never describe AI self-review as equivalent to human peer review.

---

## 13. Definition of Done

A work item is Done when the agreed quality standard is satisfied.

Baseline:

- acceptance criteria satisfied,
- tests added/updated where appropriate,
- relevant tests pass,
- formatting/lint/type checks pass where applicable,
- no secrets committed,
- CI passes,
- review completed according to the project review model,
- documentation updated when behavior/contracts change,
- merged through the approved PR workflow.

"Code exists" is not Done.

"AI says it works" is not evidence.

The Scrum Guide defines the Definition of Done as the formal description of the state of the Increment when it meets the required quality measures.

Reference:
https\://scrumguides.org/docs/scrumguide/v2020/2020-Scrum-Guide-US.pdf

---

## 14. Evidence-First AI Rule

Claims require evidence.

Examples:

```text
"Tests pass"
→ actual test output

"CI passes"
→ GitHub Actions result

"Deployment succeeded"
→ deployment evidence
```

The evidence chain should look like:

```text
AI claim
↓
actual command/tool output
↓
CI / GitHub evidence where applicable
↓
human verification where appropriate
```

AI summaries are useful, but evidence is authoritative.

---

## 15. Claude Code Operating Rules

Claude Code must:

1. Start from the GitHub Issue.
2. Read repository instructions.
3. Inspect existing code before broad changes.
4. State its understanding for non-trivial work.
5. Identify ambiguity and risk.
6. Implement only the accepted scope.
7. Add/update tests.
8. Run relevant validation.
9. Inspect the final diff.
10. Report actual evidence.
11. Prepare the PR.
12. Stop when the change is ready for review.

Claude Code must not:

- invent requirements,
- silently broaden scope,
- perform unrelated refactors,
- remove tests to make failures disappear,
- weaken security/safety controls,
- add unnecessary dependencies,
- claim unverified success.

---

## 16. AI Session Continuity

### Purpose

AI context windows are temporary.

Session memory prevents repeated investigation and loss of important context.

### Format

Keep logs lightweight.

Example:

```text
.project/history/sessions/
└── 2026-09-17-session-01.md
```

Each session contains:

```text
What I did:
What I decided:
What's half-done:
What's next:
What I'm unsure about:
```

Avoid verbose checkpoint rituals.

### New-session retrieval order

Prefer:

```text
1. Current Git state
2. Current GitHub Issue / Sprint context
3. Current repository documentation
4. Latest relevant session log
5. Earlier logs only when needed
6. Current source code/tests as final evidence
```

Old summaries must never override newer repository evidence.

### Promotion rule

An uncertainty should not remain dormant indefinitely.

If the same "unsure/undecided" item remains unresolved across **two Sprints**, it must be:

- promoted to a GitHub Issue,
- documented as an ADR/decision when appropriate,
- or explicitly marked abandoned.

There should be no silent aging of unresolved session notes.

---

## 17. Durable Documentation

Use durable documentation for information that should survive indefinitely.

Examples:

```text
docs/
├── architecture/
├── adr/
├── requirements/
├── api/
├── testing/
└── operations/

```

Session logs are for temporary continuity.

Promotion model:

```text
Temporary observation
→ validated conclusion
→ issue / ADR / durable documentation
```

A session log does not become authoritative merely because an AI wrote it.

---

## 18. Slack and Additional Project Tools

Slack is intentionally deferred.

For a solo project:

- GitHub issues provide work discussion,
- PRs provide technical discussion,
- GitHub Actions provides CI feedback,
- GitHub Projects provides planning visibility.

Slack can be introduced when a second human collaborator or a concrete communication/incident need justifies it.

Linear, Jira and Notion are also deferred.

The objective is not to collect project-management tools.

GitHub Issues + Projects already provide integrated issue tracking and project views. GitHub describes Projects as a customizable planning/tracking system integrated with issues and PRs.

Reference:
https\://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/about-projects

---

## 19. Repository Governance

Target governance:

- PR-based changes to `main`,
- required CI checks where available,
- appropriate review controls,
- secret protection/scanning,
- dependency/security automation where practical.

GitHub protected branches can require status checks, reviews and other merge conditions.

Current GitHub documentation states that protected branches are available on public repositories with GitHub Free, while private repositories require GitHub Pro, Team, Enterprise Cloud or Enterprise Server.

Because the FitnessRAG repository is currently public, protected-branch governance is available under the current free-plan setup.

If the repository is later made private, re-evaluate the governance setup at that point.

### 19.1 Secret history scan (completed)

Full git history was scanned for secrets prior to adoption (Gitleaks). All 6 findings were confirmed false positives — placeholder/example tokens in `docs/api_contracts.md` — not real credentials. No rotation was required. Full security review (dependencies, authZ, Docker, SAST, CI security) remains scoped to the Current-State Assessment, not this migration.

References:

- https\://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches
- https\://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/managing-a-branch-protection-rule

---

## 20. Commit Convention

Use **Conventional Commits** as a lightweight commit-message convention.

Examples:

```text
feat: add user profile endpoint
fix: handle failed ingestion rollback
test: cover retrieval fallback
docs: update API contract
chore: update CI workflow
refactor: simplify retrieval service
```

This is a project convention, not a Scrum requirement.

It should improve readability and consistency without becoming a blocking bureaucracy.

---

## 21. Current-Project Recovery

FitnessRAG is already partially implemented.

The project must not pretend to be a new repository.

Before planning a normal feature Sprint, perform a **Current-State Assessment**.

Assess:

### Product

- current requirements,
- intended user value,
- roadmap,
- completed vs planned functionality.

### Architecture

- actual architecture,
- dependencies,
- modules/services,
- data flow,
- integration boundaries.

### Code

- implemented features,
- incomplete areas,
- suspicious behavior,
- duplicated logic,
- inconsistencies.

### Tests

- coverage areas,
- missing behavior,
- mismatch between tests and runtime,
- fixture/integration reliability.

### CI/CD

- actual workflows,
- triggers,
- current status,
- validated checks,
- missing checks.

### Infrastructure

- local setup,
- database,
- migrations,
- Docker,
- LLM/runtime dependencies,
- reproducibility.

### Security and safety

- secrets,
- authentication/authorization,
- input validation,
- safety controls,
- configuration exposure.

### Documentation

- current vs stale documentation,
- duplicate process files,
- architecture/specification gaps.

---

## 22. Backlog Recovery

After assessment:

```text
Current reality
↓
Findings
↓
Classification
↓
Prioritization
↓
GitHub Issues
↓
Backlog ordering
↓
Sprint Goal
↓
First honest Sprint
```

Do not create a ticket for every observation.

Classify findings as:

- immediate bug,
- product gap,
- technical debt,
- test gap,
- infrastructure gap,
- documentation gap,
- security/safety concern,
- accepted limitation,
- obsolete documentation.

Only actionable work should enter the active backlog.

---

## 23. Existing `.project/` Material

The existing `.project/` directory is legacy material.

Do not delete it before assessment.

Classify contents into:

```text
Current work
→ GitHub Issue / Project

Durable engineering specification
→ docs/

Architecture decision
→ docs/adr/

Historical material
→ retained as appropriate

Obsolete personas/process/checkpoint material
→ eventually retired
```

The legacy RRPAI process does not govern the new methodology.

Genuinely useful specifications and decisions should be preserved.

---

## 24. Environment Setup Sequence

Configure the environment incrementally.

### Stage 1 — Work management

Set up:

- GitHub Issues,
- GitHub Project,
- issue templates,
- statuses,
- priorities,
- iteration/Sprint representation.

### Stage 2 — Repository governance

Set up:

- `main`,
- branch naming,
- PR template,
- CI expectations,
- repository security features available under the current plan.

### Stage 3 — Claude.ai

Provide the final operating model.

Configure Claude.ai to:

- manage backlog,
- refine issues,
- facilitate Sprint Planning,
- track progress,
- facilitate Review/Retrospective,
- require evidence.

### Stage 4 — Claude Code

Configure repository-level instructions around:

- issue-first development,
- scope control,
- tests,
- Git,
- PRs,
- evidence,
- session continuity.

### Stage 5 — Current-State Assessment

Assess FitnessRAG before normal feature planning.

### Stage 6 — First real Sprint

Run:

```text
Planning
→ Issue
→ Branch
→ Implementation
→ Tests
→ PR
→ CI
→ Review
→ Retrospective
```

---

## 25. Learning Objectives

AJ should progressively become able to perform and explain:

### Product/process

- Product Goal,
- backlog ordering,
- refinement,
- Sprint planning,
- acceptance criteria,
- review,
- retrospective.

### Git

- branching,
- commits,
- merge,
- rebase,
- conflicts,
- branch cleanup.

### Collaboration

- issue/PR linking,
- PR creation,
- review comments,
- responding to feedback.

### Testing

- unit,
- integration,
- API/component,
- E2E where appropriate,
- regression tests,
- fixtures.

### CI/CD

- triggers,
- jobs,
- status checks,
- builds,
- test stages,
- artifacts,
- deployments,
- failure recovery.

### Engineering

- architecture decisions,
- migrations,
- configuration,
- security,
- observability,
- technical debt.

### AI-assisted development

- repository context,
- scoped prompting,
- implementation,
- verification,
- evidence,
- AI failure modes,
- context continuity.

---

## 26. Professional Honesty Rule

When discussing the project publicly, describe the process accurately.

Appropriate description:

> "I ran a disciplined Scrum-adapted workflow on a solo software project, using AI for product/delivery facilitation and coding assistance, with real GitHub issues, pull requests, CI, automated tests, and AI-assisted review."

Do not claim:

- a multi-person Scrum Team existed when it did not,
- human peer review occurred when it did not,
- production deployment occurred when it did not,
- AI review was equivalent to human review.

The goal is credible evidence of engineering discipline, not simulated credentials.

---

## 27. Operating Principles

1. One source of truth for each kind of information.
2. Requirements before implementation.
3. Small changes before giant AI-generated diffs.
4. Evidence before claims.
5. Tests remain part of engineering quality.
6. AI assists; the developer remains accountable.
7. Current repository evidence beats stale memory.
8. Do not add tools without a concrete need.
9. Do not add ceremony without a delivery or learning benefit.
10. Optimize for working software and transferable engineering skill.

---

## 28. Adoption Sequence

This v1.0 model becomes authoritative only after:

```text
Independent Claude review
↓
Final corrections
↓
Commit to repository
↓
Configure GitHub Project
↓
Configure Claude.ai
↓
Configure Claude Code
↓
Perform Current-State Assessment
↓
Create normalized backlog
↓
Plan first honest Sprint
```

No application-code changes are part of adoption itself.

---

## 29. Independent Review Request

Before adoption, Claude.ai should independently challenge this v1.0 document.

It should identify:

- anything inaccurate about Scrum,
- anything incorrectly presented as an industry standard,
- anything unnecessarily bureaucratic,
- missing engineering practices,
- unrealistic AI responsibilities,
- problems caused by the solo-project adaptation,
- weaknesses in session continuity,
- weaknesses in evidence/review,
- anything that could create misleading claims of professional experience,
- anything that should be deferred.

Claude should distinguish:

- Scrum requirements,
- optional Scrum adaptations,
- engineering best practices,
- GitHub capabilities,
- project-specific decisions.

It should challenge the document rather than rubber-stamp it.