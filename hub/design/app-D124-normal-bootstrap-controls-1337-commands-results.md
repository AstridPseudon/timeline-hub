# D124 commands and results

All commands ran from `/home/user/work/wt/app-D124-normal-bootstrap-controls-1337` with Node compile cache under `/tmp/w-8bb84f01fd`.

1. Normal three-control rerun, with exact Runtime/Agent checkouts and `ASTRID_RUNTIME_PYTHON` bound before startup:

```sh
TMPDIR=/tmp/w-8bb84f01fd NODE_COMPILE_CACHE=/tmp/w-8bb84f01fd/app-D124-node-compile-cache-default-helper \
ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-5e9ad1c6 \
ASTRID_RUNTIME_PYTHON=/home/user/work/venv-runtime/bin/python \
ASTRID_CHECKOUT=/home/user/work/wt/agt-pin-070dfc5e \
ASTRID_PYTHON=/home/user/work/venv-agent/bin/python \
ASTRID_P2_COMMIT_PHASE_CAPTURE_WATCHDOG_SECONDS=20 timeout 180 \
/home/user/work/runtimes/agent-remotion-app-p1-787-2a9-1830/.toolchain/node-v20.19.4-linux-x64/bin/node \
--import tsx --test --test-name-pattern='a fixture that throws|D78 bootstrap|P2 Runtime observer bootstrap' \
tests/e2e/fake-runtime/server.contract.test.mjs \
tests/e2e/local/support/p2-runtime-phase-bootstrap.test.ts
```

Result: exit 1; 42 discovered, 1 passed, 2 failed, 39 skipped. D78 passed. The fake fixture expected 500 and received 200. P2 reached Runtime and failed the existing `readCapture` key assertion after bounded capture output was emitted.

2. Exact reviewed helper through the App D66 identity hook:

```sh
/home/user/work/runtimes/agent-remotion-app-p1-787-2a9-1830/.toolchain/node-v20.19.4-linux-x64/bin/node --input-type=module -e 'import { diagnosticHelperIdentity } from "./scripts/testing/d66-plain-stack.mjs"; const path = "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/app-D124-helper-final-review-1315-helper.py"; const sha256 = "6c9daef27884c30b8faf234349078310af7ebe016bf0c4339960d5baae5a0760"; console.log(JSON.stringify(diagnosticHelperIdentity({ runtimeCheckout: "/home/user/work/wt/rt-pin-5e9ad1c6", env: { D66_P2_COMMIT_PHASE_CAPTURE_HELPER: path, D66_P2_COMMIT_PHASE_CAPTURE_HELPER_SHA256: sha256 }, required: true })))'
```

Result: PASS; returned the exact path, SHA256, and `source: "explicit"`.

3. Existing D124 helper identity and normal-submit recipe tests:

```sh
TMPDIR=/tmp/w-8bb84f01fd NODE_COMPILE_CACHE=/tmp/w-8bb84f01fd/app-D124-node-compile-cache-d66 \
D66_P2_COMMIT_PHASE_CAPTURE_HELPER=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/app-D124-helper-final-review-1315-helper.py \
D66_P2_COMMIT_PHASE_CAPTURE_HELPER_SHA256=6c9daef27884c30b8faf234349078310af7ebe016bf0c4339960d5baae5a0760 timeout 180 \
/home/user/work/runtimes/agent-remotion-app-p1-787-2a9-1830/.toolchain/node-v20.19.4-linux-x64/bin/node \
--import tsx --test --test-name-pattern='D124 requires and carries|D124 normal submit recipe carries' \
scripts/testing/d66-plain-stack.test.mjs
```

Result: exit 0; 2 passed, 27 skipped.

The earlier protected receipt recorded the unqualified central harness as 44 passed / 3 failed because `ASTRID_RUNTIME_PYTHON` was absent before startup. No full suite or browser/native/P2 tour was requested or run here.
