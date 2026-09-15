# Definition of Done (DoD)

This checklist applies to all User Stories and technical tasks in the backlog. A task cannot be moved to "Done" in the Sprint Tracker unless all applicable criteria below are met.

## General Code Quality
- [ ] Code is formatted and linted according to project standards (e.g., `black`, `flake8`, `mypy` for Python).
- [ ] No hardcoded secrets or API keys exist in the codebase.
- [ ] Code has been peer-reviewed (or reviewed by a secondary AI agent via `/code-review` workflow).

## Testing & Validation
- [ ] Unit tests have been written for new business logic.
- [ ] Integration tests verify the new component works with the database/external APIs.
- [ ] `pytest` (or equivalent) passes locally with no regressions.
- [ ] Test coverage for the modified component is >80%.

## Architecture & Security
- [ ] Changes adhere to the architectural boundaries defined in `architecture_document.md` (e.g., deterministic rules in Python, not LLM).
- [ ] Safety constraints (no medical diagnosis, non-clinical only) have been respected.

## Documentation
- [ ] Inline code documentation (docstrings) is updated.
- [ ] `README.md` or specific component documentation is updated if setup steps have changed.
- [ ] A checkpoint/session log has been created using `SESSION_LOG_ENHANCED.template.md`.

## User Acceptance
- [ ] The feature meets all Acceptance Criteria defined in the User Story.
- [ ] The user (Product Owner) has approved the changes via the `/approve` workflow or explicit chat confirmation.
