## Report

Read-only investigation completed; no worktree source/test changes made.

Finding: Runtime’s `idempotency_mismatch` guard is correct. The first accepted request declares created identities in Agent-emitted order:

`track, asset, clip`

The replay calls `_commit(..., declare_track=False)`, producing:

`asset, clip`

All other request components are constructed identically: base revision/publication pair, patch previous values, media admission pin, steps, reads, label, source, merge, and dry-run. Runtime hashes the full envelope and rejects the changed payload before provider execution.

Owner: [tests/test_timeline_headless_overwrite_refused.py](/home/user/work/wt/rt-R5-headless-retry-path-review-0511/tests/test_timeline_headless_overwrite_refused.py:364). Smallest faithful correction is adding `declare_track=True` to both replay calls (before close/reload and after reload). Do not change the helper default; the trackless-invalid test depends on `False`.

The retained run was not rerun: 13 collected, 12 passed, 1 failed in 3.52s (`idempotency_mismatch`). Close/reopen assertions were therefore not reached. No complete serialized request/media capture exists; conclusions are source-derived plus retained failure evidence.

Checks:

- Agent: `9cd3dbe…`, tree `57f0231d…`
- Runtime: `66657fda…` over `faf6a547…`
- AST/topology and hashes verified.
- Compile: PASS
- Ruff: PASS
- `git diff --check`: PASS
- Prior unchanged Pyright result: 0 errors
- No provider, HTTP, full-suite, or browser execution.

Commit message and `DONE` marker created.