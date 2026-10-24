## Report

Updated [`test_timeline_helper_capture.py`](/home/user/work/wt/agt-F-helper-fixture-0114/tests/sdk/test_timeline_helper_capture.py:110) to use `pop(..., None)`, accommodating the public reader’s already-removed `_runtime_document`.

Tests:

- Targeted node: 1 passed.
- Fixture/pair controls: 6 passed.
- Ruff: 2148/2148 baseline.
- Mypy: 1911/1911 baseline.
- Vendor lock, artifact manifest, and diff check: passed.

Only one fixture line changed; assertions and production code are untouched. Before/after full-file hashes: `2e4925…890e2` → `c0379c…46a`. Source origin remains `dba6e4e7a8`; changed line is uncommitted.

No blockers. Commit message written and `DONE` created.