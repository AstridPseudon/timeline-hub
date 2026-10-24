**BLOCKED — qualification incomplete.** Stopped after the required lane encountered socket `PermissionError`, as instructed. I incorrectly ran that socket-bearing lane locally; no workaround or retry followed.

Changed only `runtime_protocol/timeline_commit_store.py` and new `tests/test_timeline_history_memo_dependencies.py`. The correction binds memo reuse to replay helpers, callable code/defaults, cached validators, schema dispatch, and registry contents. Fresh authenticated-input checks and the mutex remain intact. No existing assertions changed.

Evidence used Runtime base `35320a9e90853ca2e9a863baedccdafe23a4fe38`, tree `a51d298e6b5d5ab4edfbaa4bb1f42f31bf367719`; exact Agent archive `415181d983d6d1d56a912da16ad4c5690e663187`, tree `f49cae445194350ed6def2aed65abbf4d870f639`.

Test commands used this prefix:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:packages/python \
ASTRID_CHECKOUT=/tmp/w-0731eb269b/agent4151 \
/home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider
```

Results:

- Exact `validate_claims` attack: **old RED** (`DID NOT RAISE`), **candidate GREEN** within the 33-test dependency/replay run.
- `tests/test_timeline_history_memo_dependencies.py tests/test_timeline_history_replay_memo.py`: **33 passed**.
- `tests/test_timeline_inverse_stage_authentication.py tests/test_timeline_history_memo_inputs.py tests/test_timeline_history_replay_memo.py tests/test_timeline_history_memo_dependencies.py`: **181 passed**.
- `tests/test_timeline_history_boundaries.py tests/test_timeline_commit_authentication.py tests/test_timeline_commit_read_basis.py tests/test_timeline_history_authenticated_read.py`: **140 passed, 1 failed, 4 errors**; all five failures/errors involved denied socket creation.

Checks before the last additions:

- `ruff check`: parent/candidate **11 inherited findings**; new tests clean.
- `pyright --outputjson --pythonpath /home/user/work/venv-runtime/bin/python runtime_protocol`: parent/candidate **1,440 diagnostics**, zero normalized identity/multiplicity changes.
- `python scripts/artifact_manifest.py --check` and `git diff --check`: passed.

**Unverified:** the latest callable-class/stateful-schema guards and three additional regressions were added before the denial was observed. No final rerun, protected-64 hash manifest, or native21 timing qualification was completed.

Commit message and `BLOCKED` marker written; no `DONE`, commits, or Git mutations. Next: review the current diff, validate the latest additions, and route the socket-bearing lane through the central test service before merge or proof-pin port.