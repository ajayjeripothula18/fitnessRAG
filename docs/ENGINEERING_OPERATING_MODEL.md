# FitnessRAG Engineering Operating Model v1.0

## Core Principles

1. Single mainline branch (`main`) as the sole long-lived branch.
2. Short-lived feature/fix/chore branches for all changes.
3. GitHub Issues and Projects for work management.
4. `docs/` directory for durable engineering documentation.
5. `.project/` retained temporarily for migration/recovery.
6. Claude Code works from GitHub issues.
7. No application-code changes as part of this migration.

## Branching Model

- `main`: Protected production branch. All changes must be merged via pull request.
- Feature branches: `feature/FIT-<issue-number>-short-description`
- Bug fixes: `fix/FIT-<issue-number>-short-description`
- Chore branches: `chore/<short-description>` (for refactoring, tooling, etc.)
- Hotfixes: `hotfix/FIT-<issue-number>-short-description` (for critical production fixes)

## Workflow

1. Work begins with a GitHub Issue.
2. Create a branch from `main` (e.g., `feature/FIT-123-add-widget`).
3. Implement changes, write/run tests.
4. Open a pull request targeting `main`.
5. Pull request must pass CI and review.
6. After approval, merge (preferably squash) into `main`.
7. Delete the feature branch.

## Documentation

All durable engineering documentation (architecture, API contracts, database design, etc.) resides in the `docs/` directory at the repository root.

## CI/CD

GitHub Actions workflow triggers on:
- Push to `main`
- Pull request targeting `main`

## Phasing Out `.project/`

The `.project/` directory is retained temporarily for migration and recovery of historical artifacts. It will be archived or removed in a future phase after reconciliation.

## Roles

- **Product Owner**: Defines and prioritizes GitHub Issues.
- **Tech Lead**: Reviews pull requests, ensures adherence to standards.
- **Developers**: Implement features, write tests, open pull requests.
- **CI/CD**: Automated testing and deployment.

## Quality Gates

- All changes must include automated tests.
- Code review required for all pull requests.
- CI must pass before merging.
- Documentation must be updated as needed.
