# D127d validation

## Result

`SOURCE_PREPARED`; acceptance `NOTRUN`; Runtime COST-CANDIDATE remains
pending. No preflight, bootstrap, service, checkout, browser, socket, body,
profile, or actual Runtime execution was performed.

## Implemented seam

- Added the explicit `p2-element-verify` D66 selector, retaining the exact
  original element file, grep, count, and private stream-log behavior.
- The verification selector emits `D66_ELEMENT_VERIFICATION_ONLY=1` only for
  its normal launch stage and refuses the arm for any other suite.
- The harness allocates the existing private Runtime stream directory without
  resolving or creating a phase-capture sink for this arm.
- The actual Runtime child environment removes the verification selector,
  capture activation/sink/helper/hash, watchdog, Runtime log, and phase ordinal
  variables and uses no `scripts/testing` bootstrap path.
- The default `p2-element` arm, helper identity/path/hash checks, historical
  routes, source guard, and original element body remain unchanged.

## Commands and results

- `/home/user/work/runtimes/agent-remotion-app-p1-787-2a9-1830/.toolchain/node-v20.19.4-linux-x64/bin/node --check scripts/testing/d66-plain-stack.mjs` — PASS.
- Same Node 20.19.4 command with `--check scripts/testing/d66-plain-stack.test.mjs` — PASS.
- `.../node-v20.19.4-linux-x64/bin/node --test scripts/testing/d66-plain-stack.test.mjs` — PASS, 30 tests, 30 passed, 0 failed, 0 skipped.
- `.../node_modules/.bin/eslint tests/e2e/local/support/harness.ts --report-unused-disable-directives --max-warnings 0` — PASS.
- `.../node_modules/.bin/tsc --noEmit -p tsconfig.node.json` — PASS.
- `.../node_modules/.bin/tsc --noEmit -p tsconfig.app.json` — PASS.
- `git diff --check` — PASS.
- Original element body and phase-bootstrap source diff — empty.

The D127d offline control passed through the supported launch environment,
inherited measurement variables, and verified two spawned harness incarnations
had no capture/helper/watchdog/bootstrap activation while private stdout and
stderr files were retained with private modes.

## Deliberately not run

No full suite, live service, localhost/browser flow, Runtime body, candidate
profile, request-checkout, source preflight, bootstrap, registration,
submission, or original five-second element body was run. The later candidate
verification remains held for the independently qualified Runtime cost fix and
normal receipt.
