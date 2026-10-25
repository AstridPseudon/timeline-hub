# Validation

## Executed intended nodes

- `TSX_DISABLE_CACHE=1 ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime node --experimental-test-isolation=none --import tsx --test --test-concurrency=1 --test-name-pattern='D127c source guard accepts every reviewed arm and rejects wrong hash or source' --test-reporter=tap tests/e2e/local/support/p2-runtime-phase-bootstrap.test.ts` — **PASS**, 1 named node.
- `TSX_DISABLE_CACHE=1 ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime node --experimental-test-isolation=none --import tsx --test --test-concurrency=1 --test-name-pattern='D127c reviewed-profiler validator' --test-reporter=tap tests/e2e/local/support/p2-runtime-phase-bootstrap.test.ts` — **PASS**, 1 named node.
- `TSX_DISABLE_CACHE=1 ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime node --experimental-test-isolation=none --import tsx --test --test-concurrency=1 --test-name-pattern='D127 reviewed-new validator' --test-reporter=tap tests/e2e/local/support/p2-runtime-phase-bootstrap.test.ts` — **PASS**, 1 named node.

Node22 is supplemental. It was used only for no-live validator/sourceguard nodes; no bootstrap body ran.

## Required Node20 control

- `/home/user/work/runtimes/agent-remotion-app-p1-787-2a9-1830/.toolchain/node-v20.19.4-linux-x64/bin/node --import tsx --test --test-concurrency=1 --test-name-pattern='^(D127c source guard|D127c reviewed-profiler validator)$' tests/e2e/local/support/p2-runtime-phase-bootstrap.test.ts` — **NOTPASS / NOTRUN**: wrapper only (`tests 1`, no named inner node; custom event stream had zero intended child nodes). The unchanged combined Node20 pattern was not repeated.
- The analogous Node20 command with the reviewed-profiler/reviewed-new pattern had the same wrapper-only result and is also **NOTRUN**.

## Static/source checks

- `npx eslint tests/e2e/local/support/p2-runtime-phase-bootstrap.test.ts --max-warnings 0` — **PASS**.
- `npx tsc --noEmit --pretty false` — **PASS**.
- `git diff --check d5a1d1ab6550187e377fd7387d300102b8b82ece 466c921f40fb9c08e50928df6dea27dfdfb45d15` — **PASS**.
- `git diff --quiet d5a1d1ab6550187e377fd7387d300102b8b82ece 466c921f40fb9c08e50928df6dea27dfdfb45d15 -- . ':(exclude)tests/e2e/local/support/p2-runtime-phase-bootstrap.test.ts'` — **PASS** (exit 0; outside blobs/modes unchanged).
- Real `p2CommitPhaseCaptureConfig()` source-proof probe with `D66_P2_COMMIT_PHASE_CAPTURE_HELPER=/tmp/runtime-helper-check.py` containing the exact Runtime `368f…` Git object and the exact `095c…` expected SHA — **PASS**, returned the exact digest; its temporary noncanonical basename was not treated as sourceguard-qualified.
- Final App status — **clean**.
- Final App commit/tree — `466c921f40fb9c08e50928df6dea27dfdfb45d15` / `6d2744e271f016206854ab33f57b3cfc737ad54d`.
- Runtime helper source proof — Git commit `368f53f4454d5908c86de53d174f0bedcf23781c`, helper SHA-256 `095c252b…`; central request `30318`, **61 passed in 3.62s**, reused and not rerun.

## Not run by design

No live bootstrap/source-guard body, socket, browser, original-element, native, full suite, tour, acquisition, product, Runtime retest, or additional helper review was run. The Node20 combined pattern previously hung and was not blindly repeated.
