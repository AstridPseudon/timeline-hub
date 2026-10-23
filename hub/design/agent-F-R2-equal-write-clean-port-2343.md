## Report

Ported the exact approved cumulative blobs from `97ce625c…`:

- `astrid/sdk/timeline/inverse.py`
- `tests/sdk/test_timeline_inverse_fork_guard.py`

Both hashes match the approved donor exactly:

- `6741905d6a94b825c3a87cbb0b78c77085d326fa`
- `a7cb4b52d1fdacb11248d7cde47f6a8f964de73f`

Tests:

- Required joint pytest collection: **91 passed**
- Ruff: passed
- Private-cache mypy: passed
- Diff check: passed
- Four pre-existing companion acceptance files unchanged

No full suite requested. No blockers. The donor worktree path was absent, so the approved local Git ref was used directly.

Commit message written to the required path, and `DONE` created.