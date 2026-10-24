## Report

Updated only [`mypy_astrid.json`](/home/user/work/wt/agt-F-mypy-shrink-0437/scripts/reshape/baselines/mypy_astrid.json): 1909 → 1902.

Evidence against qualified parent `c8360b3732`:

- Parent: 1909 diagnostics
- Current: 1902 diagnostics
- Shared: 1902
- Removed: 7
- New: 0

Removed identities: one `arg-type`, five `assignment`, one `misc`, all in `generic_host.py`.

Checks:

- `compare_mypy_baseline --write-baseline` — passed
- Strict comparator — passed at 1902/1902
- `make mypy PY=...` — passed
- D40 scoped mypy — current 140; zero additions
- Baseline JSON validation — passed
- Vendor lock against `45c3a7f4` — passed
- Artifact manifest — passed
- `git diff --check` — passed
- Targeted tests — 11 passed

No full/browser/gate suite run. Commit message and `DONE` marker created.