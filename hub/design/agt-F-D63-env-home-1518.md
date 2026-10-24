## D63 actual-home proof

- Verified HEAD `d27b6601e56b19334c9534338ce1f3ac80e85fc`; merge parents are `68e82c0c` and author `2a8fbc6c`.
- `astrid/core/execution/orchestrator/runner.py` blob exactly matches author `2a8fbc6c`.
- `tests/test_env_vars_conformance.py` blob exactly matches upstream `924437716`.
- Production caller confirmed: `generic_host_worker → run_orchestrator`.
- No source or test edits; worktree clean.

Test command:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/wt/agt-F-D63-env-home-1518:/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q tests/test_env_vars_conformance.py::TestNoBareStringAccess::test_no_catalogued_bare_strings_in_core tests/core/execution/test_runtime_orchestrator_custody_d40.py --junitxml=.../evidence/home.xml
```

Result: `16 passed in 12.57s` — original order-181 test plus all 15 D40 guards. Exit `0`; JUnit reports 16 tests, zero failures/errors/skips.

Evidence: `workers/agt-F-D63-env-home-1518/evidence/` (40 KB). `DONE` and `commit-msg` created. No full suite, installs, Node, or source acquisition performed.

The initial command lacked the runtime import path and hit collection error for `runtime_protocol`; rerun used the existing shared Runtime path, with no installation. I did not write `design/` or `report.md` per the explicit D30 prohibition; harness publication remains responsible for the final report.