## Report — R-P2-popup-422

Implemented authenticated projection for fork-created `shot:<id>` roots between same-step commands, preserving existing owner, identity, digest, source-pin, and physical-observation guards.

Added `tests/test_timeline_popup_fork_authority.py` with positive and forged-owner/sibling/source controls.

Tests:

- Runtime targeted: 7 passed, 111 deselected.
- Runtime auth cohort: 228 passed, 40 deselected.
- Agent fork/add suite: 18 passed.
- Ruff, Pyright, compile, `git diff --check`: passed.
- Protected original test body unchanged.
- No full/browser/live suite run.

Regression comparison found the projector originated before `bc227` in the earlier R2r created-child work; `bc227..HEAD` had no auth-file difference.

Commit message written to the requested path. Independent security/core review remains required before merge.