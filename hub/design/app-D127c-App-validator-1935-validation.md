# D127c validation

## Passed

- `node --import tsx --test --test-concurrency=1 --test-name-pattern='^(D127c reviewed-profiler validator|D127 reviewed-new validator)' --test-reporter=spec tests/e2e/local/support/p2-runtime-phase-bootstrap.test.ts` — 2 passed.
- `/home/user/work/runtimes/agent-remotion-app-p1-787-2a9-1830/.toolchain/node-v20.19.4-linux-x64/bin/node --import tsx --test --test-concurrency=1 --test-name-pattern='^D127c reviewed-profiler validator enforces the exact safe cProfile projection$' --test-reporter=spec tests/e2e/local/support/p2-runtime-phase-bootstrap.test.ts` — 1 passed, 5 skipped by name pattern.
- `node --import tsx --test --test-concurrency=1 --test-name-pattern='^D127c reviewed-profiler validator enforces the exact safe cProfile projection$' --test-reporter=spec tests/e2e/local/support/p2-runtime-phase-bootstrap.test.ts` — 1 passed.
- `npx eslint tests/e2e/local/support/p2-runtime-phase-bootstrap.test.ts --max-warnings 0` — passed.
- `npx tsc --noEmit --pretty false` — passed.
- `git diff --check` — passed.

## Not run / blocked

- The unscoped file invocation was not used as evidence: this checkout's default `RUNTIME_CHECKOUT` points at missing `/home/user/work/wt/astrid-runtime`, and the live harness has no selected executable. The dependent D78/live bootstrap and original observer body therefore remain NOTRUN.
- No browser, localhost, service, full suite, D66 body, or production qualification was run.
- Node available locally was `v22.22.0`; the supported Node `v20.19.4` path remains the canonical later admission path.
