## Report

Changed only [tests/test_timeline_commit_acceptance.py:307](/home/user/work/wt/rt-R2-legacy-ABI-expectation-2131/tests/test_timeline_commit_acceptance.py:307), updating the exact expected legacy metadata to include authenticated `recorder_abi: 1`.

Normative basis: D61 commit `6e8ae0142` makes `recorder_abi` an approved optional history field; D62 commit `8825219b4` requires acceptance-time ABI classification and persistence. C0 still preserves legacy `rebased` status, absent labels/steps, and restart replay.

Tests:

- Parent reproduction: 1 expected failure at line 304; XML: [parent-red.xml](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-R2-legacy-ABI-expectation-2131/evidence/parent-red.xml)
- `ASTRID_CHECKOUT=/home/user/work/agent PYTHONPATH=... /home/user/work/venv-runtime/bin/python -m pytest -q -o addopts='-pno:cacheprovider' --timeout=45 ...`: 75 passed
- Compile: passed
- `git diff --check`: passed
- Ruff: existing 64 diagnostics before and after; zero new
- Pyright: existing 23 errors/1 warning; none on changed line

AST review confirms 18 statements and 12 assertions unchanged; only the SQL equality literal changed. Proposed deletion-ledger entry, report-only: retire the obsolete one-key expected metadata literal; no shared ledger was modified.

Commit message written and `DONE` created.