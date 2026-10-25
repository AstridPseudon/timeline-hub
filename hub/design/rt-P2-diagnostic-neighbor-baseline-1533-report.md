## Result: BASELINE

The immutable Runtime `5e9ad1c6…` parent reproduced the same failure with the same clean Agent pin `070dfc5e…`.

Command:

```text
ASTRID_CHECKOUT=/home/user/work/wt/agt-pin-070dfc5e
ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-5e9ad1c6
PYTHONPATH=/home/user/work/wt/rt-pin-5e9ad1c6:/home/user/work/wt/agt-pin-070dfc5e
/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider -m integration \
  --basetemp=$TMPDIR/ordinary-parent \
  --junitxml=<evidence>/ordinary-parent.xml \
  tests/test_timeline_ordinary_http.py::test_ordinary_http_empty_bootstrap_must_be_reachable
```

Result: **1 failed, exit 1, 1.81s**. Failure is identical at line 210:

`CommandError: hold clear requires a surviving source window`

The failure occurs in Agent capture before the hold-clear Runtime commit is submitted. Exact owner seam: `astrid/sdk/timeline/_clip_scalar_commands.py:44-47`.

Before/after module origins remained pinned to the immutable Runtime and Agent paths. Protected diagnostic source hashes match the independent 1527 packet; durable JUnit/XML and logs are in:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-P2-diagnostic-neighbor-baseline-1533/evidence/`

No product/test edits were made. Diagnostic-source readiness is qualified with this explicit baseline; overall ordinary-HTTP readiness remains blocked on the Agent-owned source-window behavior. `DONE` and the conventional commit message were written.