## Report

No worktree changes were made.

- Exact qualification: 1 passed, 3 failed.
  - Semantic removal/undo: passed.
  - Shared alias `[first]`/`[second]`: failed with live `shot item source changed` / `identity_conflict`.
  - New duplicate residual: failed because `authoring_commit_request` rejects unregistered closure-membership additions.

Controls: 20 passed, including alias/source forgery no-write checks and shared-removal controls.

Checks:

- Ruff: 2143/2143
- Mypy: 1902/1902
- `git diff --check`: passed
- Durable controls XML SHA-256: `f426c9e160f4c50f68430441c8d9380a5d577df5c40ff35bccc3f0c3c552c5d5`

The remaining failures are production seams, not valid fixture migrations. Recommended next steps: Sol review of authenticated fork source materialization and registration of a semantic duplicate-membership command.