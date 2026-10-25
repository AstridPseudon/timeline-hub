## Report

Changed only `tests/editing_conformance/test_commit_runtime_shared_inverse.py`.

- Preserved authored-first topology: `repeated-third` remains at 13s instead of being incorrectly moved to 12s.
- Preserved all test bodies, selectors, assertions, refusal branches, and authored values.
- Confirmed original-third remains mathematically incompatible: global move `3.5s`, host start `3.3s`, host window `1.8s`, clip duration `1.8s` → local end `2.0s`. Runtime guard remains unchanged; no fabricated fix applied.

Validation:

- Ruff targeted: pass.
- Ruff baseline: pass, `2143 = 2143`.
- Mypy targeted: pass.
- In-memory compile and `git diff --check`: pass.
- Repository mypy comparator: blocked by missing `types-PyYAML` and incompatible NumPy stubs.
- No pytest, fixture execution, service, browser, or build runs.

Candidate blob: `9f84493a1537a0da7b34b56f6f0c218d767bd4ba`.

Commit message written and `DONE` created. Functional MAIN proof remains owed.