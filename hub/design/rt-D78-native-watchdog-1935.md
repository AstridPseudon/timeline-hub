## Report

Implemented the bounded native watchdog in:

- [p2_commit_phase_capture.py](/home/user/work/wt/rt-D78-native-watchdog-1935/tests/helpers/p2_commit_phase_capture.py)
- [test_p2_commit_phase_capture.py](/home/user/work/wt/rt-D78-native-watchdog-1935/tests/test_p2_commit_phase_capture.py)

Behavior:

- Default 20-second per-dispatch daemon timer.
- Request-owned cancellation at dispatch completion, raised return, abort, stop, and restart.
- All-thread `faulthandler` dumps to derived private `*.stacks.txt`, mode `0600`.
- Default global capture cap of one.
- Observer-disabled behavior unchanged.
- Existing App `sitecustomize` activation remains the caller; no App or client-timeout changes.

Tests:

- Targeted pytest: `12 passed`
- Ruff: passed
- Compileall: passed
- Pyright: `0 errors`
- `git diff --check`: passed
- JUnit XML: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-D78-native-watchdog-1935/evidence/watchdog.xml`

The literal requested `--timeout45` spelling was rejected by pytest; `--timeout=45` passed. The live smoke uses a shortened injected timer and genuine `RuntimeHTTPServer` dispatch, not an actual App/browser hang. The original 5-second UI timeout remains below the default 20-second capture window, and the dump contains Python frames only—not Node/browser frames.

Source hashes are recorded in `evidence/watchdog-source-hashes.txt`. Commit message and `DONE` marker were created.