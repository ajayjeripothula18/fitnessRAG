# ADR-004: Version-Control Alembic Migrations
## Created by Ajay (Developer)
## Status: Accepted
## Date: 2026-09-18

---

## Context

The FitnessRAG project uses Alembic for database migrations. Initially, the migration revision files in `backend/alembic/versions/` were ignored by Git via the `.gitignore` rule:

```
backend/**/alembic/versions/*.py
!backend/**/alembic/versions/__init__.py
```

This prevented the migration scripts from being version-controlled, causing potential issues with reproducibility and collaboration.

## Decision

We decided to version-control Alembic migration revision files. Specifically:

- Removed both the ignore rule for `backend/**/alembic/versions/*.py` and the exception for `__init__.py` from `.gitignore`.
- Add the existing migration files to Git tracking:
  - `ae2a53256191_initial_migration.py`
  - `65c1abccacc4_initial.py`
  - `cd30829874cb_initial.py`
- Preserve the existing migration history exactly: `ae2a53256191 → 65c1abccacc4 → cd30829874cb`.
- Do not delete or rewrite the two empty migration revisions.
- Do not change database schema or application models.

## Consequences

### Positive
- Migration scripts are now visible in Git history, enabling code review via pull requests.
- Database schema changes are reproducible from a fresh checkout.
- Collaborators can inspect and verify migration changes.
- Alembic upgrade head succeeds from an empty database using only the migration files tracked in Git.

### Negative
- Slight increase in repository size (negligible, as migration files are small text files).
- Requires care to avoid committing migration scripts that contain sensitive information (none present).

### Risks
- No additional risks were identified for this repository change. Migration scripts remain subject to normal PR review.

## Related Documents
- `.gitignore`
- `backend/alembic/versions/` directory

## References
- Alembic Documentation: https://alembic.sqlalchemy.org/