## Report

Implemented fixture-only authentication fixes in:

- `tests/sdk/test_timeline_open_commit.py`
- `tests/sdk/test_timeline_open_commit_v2.py`

Changes keep revision/publication pairs aligned with provider-backed and executed peer heads. All v2 assertions remain unchanged.

Tests:

- Targeted two-file pytest: **42 passed**
- Ruff: **22 pre-existing diagnostics before and after; no new findings**
- Qualified mypy: **1902 current / 1902 baseline**
- `git diff --check`: **PASS**

Provenance:

- Base: `7e25823c2498`
- R1: `0eab665187`
- R2: `668b183783`
- Runtime pin: `becfe6db88b2`

No product code or shared dependencies changed. No full suite run. Commit message written and `DONE` marker created.