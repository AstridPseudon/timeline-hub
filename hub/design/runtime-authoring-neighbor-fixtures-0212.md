## Completed

Updated only:

- [tests/timeline/test_authoring_feedback.py](/home/user/work/wt/rt-F-authoring-neighbor-fixtures-0212/tests/timeline/test_authoring_feedback.py)
- [tests/timeline/test_authoring_bundle.py](/home/user/work/wt/rt-F-authoring-neighbor-fixtures-0212/tests/timeline/test_authoring_bundle.py)

Ported fake writers/transports to v2 immutable reads, history receipts, media-selection reads, `commit_timeline`, canonical replies, and idempotency handling. Preserved all 69 collected cases and original payload assertions.

## Verification

Required targeted command: **61 passed, 8 failed**.

Failures are out-of-scope v2 semantic boundaries: no-op commits, closure membership/removal, unplaced-shot changes, occurrence reorder, and the preserved real integration test using the retired seed route.

- Baseline source 5aee: 54 passed, 15 failed.
- Parent b61 review baseline: 68 passed, 1 retired-route failure.
- Ruff on both files: passed.
- Mypy on both files: passed.
- AST parse, diff check, and retired fake-route census: passed.
- No full suite run.

No production code or integration-test body was changed. Commit message and `DONE` marker were written.