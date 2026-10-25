Implemented D134 source-only intake.

- Imported donor byte-exactly into [test_timeline_selected_schema_runtime.py](/home/user/work/wt/agt-F-D134-selected-source-intake-2112/tests/sdk/test_timeline_selected_schema_runtime.py).
- Donor/worktree SHA-256: `8243f3b9…`
- Original `a30e` preimage verified: `6d7ba762…`
- Exactly one product file changed; no source adaptation.

Validation:

- Python 3.11 compile: pass
- Ruff: pass
- `git diff --check`: pass
- Scoped mypy: known baseline-only `types-PyYAML` error
- Live/full tests and source probe: not run per brief; no behavior credit

Evidence, commit message, and `DONE` marker are recorded in the assigned worker directory.