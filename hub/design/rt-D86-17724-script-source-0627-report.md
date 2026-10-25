## Result

- Corrected S3 dry-run setup to use `capture_occurrence_add_media`, preserving the accepted command’s authenticated claims.
- No changes to union/script tests or production code.
- Commit message written; `DONE` created.

## Unapplied seams

- Ordinary union’s two failures require Runtime-owned same-commit physical promotion/read authentication.
- Timeline script descriptor failure requires Runtime/authoring hydration of `binding_id`; assertion was preserved.

## Checks

- AST/in-memory compile: pass.
- Ruff on parent/candidate files: pass.
- Mypy on 7 scoped files: pass.
- AST selector/assertion conservation: pass.
- `git diff --check`: pass.
- Functional pytest/service tests not run per brief.