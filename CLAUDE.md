# FitnessRAG Engineering Workflow

This repository is developed using a production-style, AI-assisted engineering workflow.

## Core rule
Do not implement work directly from a vague request. Work must map to a GitHub Issue unless the change is an explicitly approved repository-maintenance task.

## Before changing code
1. Read the relevant GitHub Issue and acceptance criteria.
2. Inspect the existing implementation and tests before proposing changes.
3. Identify affected components, dependencies, data changes, and tests.
4. State the implementation approach briefly before making broad changes.
5. Prefer the smallest change that satisfies the requirement.

## Branching
- `main`: protected production/release branch. Do not develop directly on it.
- Feature branches: `feature/FIT-<issue-number>-short-description`
- Bug fixes: `fix/FIT-<issue-number>-short-description`
- Hotfixes: `hotfix/FIT-<issue-number>-short-description`

## Implementation rules
- Do not modify unrelated files.
- Do not perform opportunistic refactors while implementing a ticket.
- Do not add a dependency unless the ticket or technical design justifies it.
- Do not change public API behavior without explicitly identifying the contract impact.
- Do not remove tests to make CI pass.
- Do not weaken validation, authentication, authorization, or safety controls to make a feature work.
- Never commit secrets, local `.env` files, credentials, or tokens.

## Testing rules
Every production-code change must include appropriate automated tests.

At minimum:
- New business logic: unit tests.
- API behavior: API/integration tests where practical.
- Database behavior: database-backed tests where practical.
- Bug fixes: a regression test that reproduces the bug before the fix.

Run the narrowest relevant tests while developing, then the broader test suite before opening a PR.

## Pull requests
A completed ticket should normally result in a focused PR into `main`.

A PR must explain:
- What changed
- Why it changed
- How it was implemented
- How it was tested
- Any migration, configuration, API, security, or operational impact

The PR is not complete merely because the code runs locally. CI, review, acceptance criteria, and documentation requirements must also be satisfied.

## AI-agent behavior
Claude Code is an implementation assistant, not the product owner.

Claude Code must:
- Ask for clarification when requirements conflict or are materially ambiguous.
- Verify assumptions against the repository before coding.
- Prefer evidence from code/tests/docs over assumptions.
- Explain risky changes before making them.
- Never claim tests passed without actually running them or having CI evidence.
- Never claim a deployment occurred without deployment evidence.
- Keep implementation scope aligned with the issue.

## Production mindset
Optimize for correctness, maintainability, security, observability, and operability before premature scale.

Do not introduce microservices, queues, caches, Kubernetes, or other infrastructure merely because they are common in production systems. Introduce them when the project has a concrete requirement for them.

## Learning objective
This project is also a hands-on training environment for professional software-development workflows. Prefer explanations that teach the engineering reason behind a practice when that explanation helps the developer build transferable skills.
