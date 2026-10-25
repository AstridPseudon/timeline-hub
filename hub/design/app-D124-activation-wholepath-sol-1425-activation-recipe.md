# Supported activation recipe — pending central controls

No App/Runtime source change is required for the basename root. Use the existing D66 path/hash override with this exact canonical source file:

- Helper: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-D124-activation-wholepath-sol-1425/evidence/p2_commit_phase_capture.py`
- SHA256: `6c9daef27884c30b8faf234349078310af7ebe016bf0c4339960d5baae5a0760`
- Normal helper: `/home/user/work/wt/rt-pin-5e9ad1c6/tests/helpers/p2_commit_phase_capture.py`, SHA256 `a17a92115661fcef13b49169504ad8726e6f6c0cdce66b195128b14477fa76a4`.

The manager must preserve the required basename when publishing the helper. A flat design filename ending in `-helper.py` is not runnable through the normal bootstrap. Do not change that guard.

After the separate clean importer adopts reviewed candidate `9d75477be4ab209fed52087f06bfcd20487ce1a9`'s two test files, register the following exact two-control commands with the central service, running against that actual source snapshot. This task's af5fe0 worktree still has the old test assertions; it has not imported or edited those files. Do not use the original/full/P2/browser/native suites.

Normal control (unset both D66 and ASTRID helper overrides before launch):

```bash
env -u D66_P2_COMMIT_PHASE_CAPTURE_HELPER -u D66_P2_COMMIT_PHASE_CAPTURE_HELPER_SHA256 -u ASTRID_P2_COMMIT_PHASE_CAPTURE_HELPER -u ASTRID_P2_COMMIT_PHASE_CAPTURE_HELPER_SHA256 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-5e9ad1c6 ASTRID_RUNTIME_PYTHON=/home/user/work/venv-runtime/bin/python ASTRID_CHECKOUT=/home/user/work/wt/agt-pin-070dfc5e ASTRID_PYTHON=/home/user/work/venv-agent/bin/python ASTRID_P2_COMMIT_PHASE_CAPTURE_WATCHDOG_SECONDS=20 TSX_DISABLE_CACHE=1 /home/user/work/runtimes/agent-remotion-app-p1-787-2a9-1830/.toolchain/node-v20.19.4-linux-x64/bin/node --import tsx --test --test-name-pattern='a fixture that throws|P2 Runtime observer bootstrap' tests/e2e/fake-runtime/server.contract.test.mjs tests/e2e/local/support/p2-runtime-phase-bootstrap.test.ts
```

Reviewed control (fresh private TMPDIR sink; same exact source and environment apart from helper path/hash):

```bash
env -u ASTRID_P2_COMMIT_PHASE_CAPTURE_HELPER -u ASTRID_P2_COMMIT_PHASE_CAPTURE_HELPER_SHA256 D66_P2_COMMIT_PHASE_CAPTURE_HELPER=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-D124-activation-wholepath-sol-1425/evidence/p2_commit_phase_capture.py D66_P2_COMMIT_PHASE_CAPTURE_HELPER_SHA256=6c9daef27884c30b8faf234349078310af7ebe016bf0c4339960d5baae5a0760 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-5e9ad1c6 ASTRID_RUNTIME_PYTHON=/home/user/work/venv-runtime/bin/python ASTRID_CHECKOUT=/home/user/work/wt/agt-pin-070dfc5e ASTRID_PYTHON=/home/user/work/venv-agent/bin/python ASTRID_P2_COMMIT_PHASE_CAPTURE_WATCHDOG_SECONDS=20 TSX_DISABLE_CACHE=1 /home/user/work/runtimes/agent-remotion-app-p1-787-2a9-1830/.toolchain/node-v20.19.4-linux-x64/bin/node --import tsx --test --test-name-pattern='a fixture that throws|P2 Runtime observer bootstrap' tests/e2e/fake-runtime/server.contract.test.mjs tests/e2e/local/support/p2-runtime-phase-bootstrap.test.ts
```

Use the central worker's harness-cleaned TMPDIR and private Node/tsx cache. No shared dependencies are written. The unit control itself sets D66_RUNTIME_LOG_DIR to a new private child of TMPDIR and temporarily sets watchdog seconds to 2; retain its source and waits unchanged.

Effective startup chain: D66/Harness validates absolute regular non-symlink file plus SHA; runtimeEnv sets PYTHONPATH to App scripts/testing, pinned Runtime, pinned Agent, in that order, before Python starts. Automatic sitecustomize runs only for the opt-in `-m ... start` seam, checks helper basename, imports the helper, starts it, registers its stop hook and removes opt-in/sink/helper/watchdog env names from descendants. The normal Runtime CLI remains the entrypoint. A caller-only PYTHONPATH cannot substitute for runtimeEnv's explicit overlay. Source-proved relevant environment field names are listed in evidence/facts.json; no private env values are published.

Activation PASS requires a fresh actual Runtime lifecycle reaching endpoint/health and a resulting genuine request capture with expected phase/sampler evidence. Offline path acceptance and retained 1354 evidence alone are insufficient. After source and protected activation review, the manager decides any subsequent full tour.
