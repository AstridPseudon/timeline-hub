PASS_SOURCE

Implemented the demonstrated D86 fix in `astrid/sdk/timeline/commit.py`: verified hydrated pins are now retained even with a non-empty `_copy_manifest`; inverse removals and Runtime guards remain unchanged. No tests were modified.

Checks:

- In-memory compile: pass
- Ruff baseline/candidate: pass
- Mypy candidate: pass
- `git diff --check`: pass
- Timing test AST unchanged
- Pytest/service/full suites not run per SOURCEONLY requirements

Evidence: worker `evidence/`; commit message written; `DONE` created.

Next step: independent protected review, then normal Agent merge. Functional behavior remains unverified here.