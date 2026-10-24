**Handback: no demonstrated Agent production fix.** Added six offline undo transport controls in `tests/sdk/test_timeline_undo_transport.py`; no production source changed.

The retained original20732 failed at line1090: expected `transport_error`, observed `transport_timeout` (**1 failed in 40.19s, exit1**). Its traceback reaches Runtime `timeline_commit_execution.py:101`: the authenticated replay lookup **after provider execution and port close**. Authorization then fails during teardown, potentially obscuring an earlier provider error. Runtime owns this coordinator boundary; neither the underlying delay nor hook execution/durable acceptance is established. Independent report0855 agrees acceptance remains unqualified.

Source comparison against original `0c2c28da4f`:

- WorkspaceClient, session/sync, provider `commit.py`, and generated transport are unchanged.
- The only `astrid/sdk/timeline/` difference is existing media-admission work in `publish.py`, untouched here.
- Original test blob remains `e55be12f88d23fddba3dd36614eb91745c1f8adf`, with all **59 assertions unchanged**.

Exact validation commands:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-460c2d39" /home/user/work/venv-agent/bin/python -m pytest -q -oaddopts= -pno:cacheprovider --timeout=45 --tb=short tests/sdk/test_timeline_undo_transport.py::test_undo_transport_failure_retains_exact_flight tests/sdk/test_workspace_client_timeline_commit.py tests/sdk/test_timeline_sync_native.py::test_public_undo_freezes_v2_metadata_and_retries_lost_ack
/home/user/work/venv-agent/bin/python -m ruff check --no-cache tests/sdk/test_timeline_undo_transport.py
/home/user/work/venv-agent/bin/python -m mypy --python-version 3.12 --cache-dir "$TMPDIR/mypy" --follow-imports=silent tests/sdk/test_timeline_undo_transport.py
git diff --check
```

Results: **17 passed in 0.71s**; Ruff passed; mypy passed; diff check passed.

Controls exercise the real Agent session → WorkspaceClient → generated transport path with fake acceptance, verifying distinct timeout/connection-loss codes, unchanged 30-second budget, durable body/key retention, and exact retry after reopening. They do not establish Runtime authentication, guarded inverse, or original acceptance. No causal oldRED/newGREEN repair is claimed.

Next: Runtime owner diagnoses provider completion/error through the final authenticated replay boundary before another original run. No full suite or live body rerun performed. Commit message and `DONE` written; no commit or push performed.