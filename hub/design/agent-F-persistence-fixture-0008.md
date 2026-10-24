## Report

Implemented only the persistence fixture migration in [tests/sdk/test_timeline_persistence.py](/home/user/work/wt/agt-F-persistence-fixture-0008/tests/sdk/test_timeline_persistence.py).

Changes:

- Added `_FakeTimelines.history()` with revision/publication head pins and current history DTO fields.
- Added exact revision/publication validation to `open_bundle()`.
- Added publication IDs to all file-backed fixture heads.
- Updated genuine Runtime fixture head tracking to preserve publication identity.
- No production changes, skips, xfails, assertion changes, or new executor.

Tests:

- Baseline: `7 failed, 3 passed`; all failures were missing `_FakeTimelines.history`.
- Final targeted command: `9 passed, 1 failed`.
- Remaining failure: `test_publish_after_a_restart_merges_other_clips_onto_the_moved_head`, due to the existing Runtime guarded-address conflict (`intervening publication changed a guarded address`). The original positive assertion remains unchanged.
- Ruff: unchanged pre-existing `BLE001` at worker line 188; Ruff passes with that existing diagnostic excluded.
- Mypy: exactly baseline `1911` diagnostics.
- Runtime lock check: passed.
- Artifact manifest check: passed.
- `git diff --check`: passed.
- Production module hashes unchanged.

Commit message and `DONE` marker were created.