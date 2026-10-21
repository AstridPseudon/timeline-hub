# Viewing M4 registry release-failure diagnosis

## Diagnosis

The 1025 failure is an execution-environment failure, not a Composition
registry defect and not a bad fixture. The manually selected runner was
executed inside the worker sandbox. `scripts/gen-registry.test.mjs` invokes
`spawnSync(process.execPath, ['--import', import.meta.resolve('tsx'),
 'scripts/gen-registry.ts', ...args], ...)`; the sandbox returns
`spawnSync /opt/node22/bin/node EPERM`. The child stderr is empty because the
child never starts. The test assertion only includes `result.stderr`, which
explains Node's opaque `failureType: testCodeFailure`, `exitCode: 1`, and
`error: 'test failed'` in 1025.

## Before/after focused evidence

Failing before (1025-style direct worker command):

```text
TMPDIR=<worker-private-tmp>
npm_config_cache=<worker-private-tmp>/npm-cache
/opt/node22/bin/node --import ./typescript/tests/register-extensionless.mjs --test scripts/gen-registry.test.mjs
=> exit 1; one failed test; child stderr empty
=> diagnostic child result.error: spawnSync /opt/node22/bin/node EPERM
```

The fixture's first generation succeeds whenever the child is allowed to
execute; the stale-check invocation is where the opaque failure is observed.

Corrected after (one central focused run, same source tree):

```text
request-test vw-m4-registry-release-failure-diagnosis-1038 targeted --files scripts/gen-registry.test.mjs
=> central argv: node --import tsx --test scripts/gen-registry.test.mjs
=> 1 passed, 0 failed, exit 0
```

The existing normal package runner is unchanged and remains the release path:
`npm run build:test && node --import ./typescript/tests/register-extensionless.mjs
--test typescript/test-dist/tests/*.test.js scripts/*.test.mjs`. The prior
central result for `npm test` was 85 passed, 0 failed. No new full run or pack
was requested.

## Exact diff and live callers

Composition source diff: none. No assertions, loader, isolation, versions, or
consumer expectations changed. The minimal repair is to run the qualification
through the central runner/outside the nested-process sandbox. Live callers:
none (command-only).

Prerequisite identity remains `df7b86308902fae90eda1dc3080d17d8fc30ea78` /
tree `71d8e95edb1bb2d187c3193ef3462d4cfde277fa`, package `0.0.14`; public13
remains SHA-256
`9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`.
