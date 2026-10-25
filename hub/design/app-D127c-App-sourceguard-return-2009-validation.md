# D127c validation

## Passed

- `/home/user/work/runtimes/agent-remotion-app-p1-787-2a9-1830/.toolchain/node-v20.19.4-linux-x64/bin/node --import tsx --test --test-concurrency=1 --test-name-pattern='^(D127c source guard|D127c reviewed-profiler validator)$' tests/e2e/local/support/p2-runtime-phase-bootstrap.test.ts` — PASS, exit 0.
- `node --import tsx --test --test-concurrency=1 --test-name-pattern='^(D127c reviewed-profiler validator|D127 reviewed-new validator)$' tests/e2e/local/support/p2-runtime-phase-bootstrap.test.ts` — PASS, exit 0.
- `npx eslint tests/e2e/local/support/p2-runtime-phase-bootstrap.test.ts --max-warnings 0` — PASS.
- `npx tsc --noEmit --pretty false` — PASS.
- `git diff --check` — PASS.

The Node 20 control used the existing pinned v20.19.4 toolchain. The Node 20 sourceguard control covers all four supported hash arms, final `095c…`, mutated final hash rejection, and unknown basename rejection. The reviewed-profiler and reviewed-new schema/mutation validators were preserved and passed under Node 22.

## Reused evidence

- Runtime commit `368f53f4454d5908c86de53d174f0bedcf23781c`, helper `095c252b…`, central request `30318`: `61 passed in 3.62s`, reused unchanged; Runtime was not edited or rerun.

## Not run

No live bootstrap/source-guard body, browser, original element body, native/full/tour/Store/install/acquisition, or full suite was run. The later live bootstrap command remains held until the harness publishes the final App commit SHA and the protected Runtime pin is attached. Disk at validation was approximately 4.97 GiB free, above the 4.6 GiB floor; no heavy install or cache mutation was performed.
