# D124/D126 commands and results

All commands below ran with cwd
`/home/user/work/wt/app-D124-protected-activation-1435`. The private `TMPDIR`
children were under `/tmp/w-da3319296b`; raw capture files were mode 0600 and
were not published.

## Normal control

```bash
env -u D66_P2_COMMIT_PHASE_CAPTURE_HELPER -u D66_P2_COMMIT_PHASE_CAPTURE_HELPER_SHA256 -u ASTRID_P2_COMMIT_PHASE_CAPTURE_HELPER -u ASTRID_P2_COMMIT_PHASE_CAPTURE_HELPER_SHA256 TMPDIR=/tmp/w-da3319296b/d124-protected-normal ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-5e9ad1c6 ASTRID_RUNTIME_PYTHON=/home/user/work/venv-runtime/bin/python ASTRID_CHECKOUT=/home/user/work/wt/agt-pin-070dfc5e ASTRID_PYTHON=/home/user/work/venv-agent/bin/python ASTRID_P2_COMMIT_PHASE_CAPTURE_WATCHDOG_SECONDS=20 TSX_DISABLE_CACHE=1 /home/user/work/runtimes/agent-remotion-app-p1-787-2a9-1830/.toolchain/node-v20.19.4-linux-x64/bin/node --import tsx --test --test-name-pattern='a fixture that throws|P2 Runtime observer bootstrap' tests/e2e/fake-runtime/server.contract.test.mjs tests/e2e/local/support/p2-runtime-phase-bootstrap.test.ts
```

Result: exit 0; 42 tests total, 2 passed, 0 failed, 40 skipped. A fresh
Runtime lifecycle produced a 102-row, 13,152-byte, mode-0600 capture with no
truncation and 102/102 retained events.

## Reviewed control

```bash
env -u ASTRID_P2_COMMIT_PHASE_CAPTURE_HELPER -u ASTRID_P2_COMMIT_PHASE_CAPTURE_HELPER_SHA256 TMPDIR=/tmp/w-da3319296b/d124-protected-reviewed D66_P2_COMMIT_PHASE_CAPTURE_HELPER=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-D124-protected-activation-1435/evidence/p2_commit_phase_capture.py D66_P2_COMMIT_PHASE_CAPTURE_HELPER_SHA256=6c9daef27884c30b8faf234349078310af7ebe016bf0c4339960d5baae5a0760 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-5e9ad1c6 ASTRID_RUNTIME_PYTHON=/home/user/work/venv-runtime/bin/python ASTRID_CHECKOUT=/home/user/work/wt/agt-pin-070dfc5e ASTRID_PYTHON=/home/user/work/venv-agent/bin/python ASTRID_P2_COMMIT_PHASE_CAPTURE_WATCHDOG_SECONDS=20 TSX_DISABLE_CACHE=1 /home/user/work/runtimes/agent-remotion-app-p1-787-2a9-1830/.toolchain/node-v20.19.4-linux-x64/bin/node --import tsx --test --test-name-pattern='a fixture that throws|P2 Runtime observer bootstrap' tests/e2e/fake-runtime/server.contract.test.mjs tests/e2e/local/support/p2-runtime-phase-bootstrap.test.ts
```

Result: exit 0; 42 tests total, 2 passed, 0 failed, 40 skipped. A fresh
Runtime lifecycle produced a 102-row, 30,754-byte, mode-0600 capture with no
truncation and 102/102 retained events. The bounded sampler recorded 20 ms
sampling, no sampler errors, and explicit unsupported-boundary markers.

## Other checks

- `git status --short`: PASS, clean.
- `git diff --check`: PASS, exit 0.
- Node: `v20.19.4`.
- Runtime/Agent Python: `3.13.16` each.
- Source/helper custody hashes: see `evidence/source-custody.json`.
- App lint/typecheck: N/A, no App source changes.
- Full/original/P2/browser/native/broad suites: not run by task instruction.
