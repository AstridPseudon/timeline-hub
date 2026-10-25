## D127 report

- Restored the unnecessary observer assertion rewrite; only `tests/test_p2_commit_phase_capture.py` changed.
- Kept helper byte-exact: SHA256 `4ee0424b…`.
- Mapped all 160 original assertions. Four remaining changes are strict current-schema/lifecycle migrations; no assertions were removed or weakened.
- Produced all requested evidence artifacts under the worker evidence directory.
- App validator handoff freezes lifecycle values, keysets, derivations, bounds, and helper hash.

Tests/checks:

- Focused pytest: `1 passed, 22 deselected`
- Ruff: passed
- mypy: passed
- py_compile: passed
- `git diff --check`: passed
- Reused prior central receipt: `23 passed in 3.46s` on unchanged helper source.

App validator adoption remains App-owned and was not modified. Commit message and `DONE` marker are written.