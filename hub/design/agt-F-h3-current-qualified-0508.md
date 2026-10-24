# F-D32-h3 report

- Read PLAN §3 and Runtime fallback contract `contract/commit-v2.md` (hash `4581ea85…`); requested Agent design path was absent.
- Recovered historical runner `tl/agt-F-h3-env-0137:tools/run-h3-import-0137.sh` (SHA `b0855c09…`); not executed.
- Verified D40 child, receipt SHA `e8b01d8b…`, Agent `ba8f0bc8…`, Runtime `f3208b26…`, Node `v20.19.4`, Remotion archive `819acf6b…`.
- Current host `9cd3dbe…` differs from installed Agent commit, but all four relevant source files and target AST body are byte-identical. Production caller reaches `_install_host_vibecomfy_import_root()` before `GenericPackHost` construction.
- Collected exactly seven originals, then ran them once under `child/bin/python -I` with no `PYTHONPATH`.

Result: **7 passed**, 0 failed/errors/skipped/xfail/xpass/deselected/other faults. One non-failing `PytestConfigWarning` occurred because plugin autoload was disabled.

Evidence: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-h3-current-qualified-0508/evidence/`

No product changes, installs, provisioning, metadata changes, or full-suite runs. Worktree is clean. `DONE` and commit message were written.