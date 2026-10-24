## PASS — bounded fixture review

Reviewed source `5b5eab591a` (tree `eea1215d…`) with fixture commit `d578725bbf` (tree `a963539b…`, parent `b7820cebaf`).

- Only `tests/timeline/test_authoring_bundle.py` differs from `b7820cebaf`; no product edits, deletions, ancestry changes, or uncommitted tracked changes.
- Exact patch SHA-256: `35432a737831cd22d7d78386d2a48b1fa77fe3fe6cd451a8490fbb086473a351`.
- `previous_revision_id` remains genuine: `parent-1 → saved-revision`.
- Saved-pair actions require both `readable` and `details` formats; current-head actions remain strictly covered without `from_revision`.
- Original one-compilation, identity mapping, request/base/merge/command, canonical reply, closure, receipt, idempotency, metadata, and quoting assertions remain present. All 52 original test functions/decorators remain; no per-test assertion count decreased.
- Production caller remains the v2 authoring commit path.

Checks:

- Exact isolated six-case run: **6 passed, 63 deselected**.
- Ruff on both fixture files: **passed**, zero new diagnostics.
- Parent/final mypy comparison: **0 diagnostics, 0 new identities**.
- `git diff --check`: **passed**.
- No full suite or excluded known-failure cases rerun.

The prior direct-base no-op failures remain known and are not masked by this fixture correction. Agent owns the normal current-only port/home follow-up after this review.