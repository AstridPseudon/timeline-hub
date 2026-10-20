# AP2 M2 ordinary committed-driver gate

## Result

Materialized the proven ordinary Composition 0.0.13 driver and Chromium
environment smoke helper in the worker record:

- `workers/ap2-m2-ordinary-committed-driver-gate/run-central-m2-ordinary.sh`
- `workers/ap2-m2-ordinary-committed-driver-gate/chromium-env-smoke.mjs`

The driver is independent of App helper files. It resolves its helper by
absolute path from its own record and the helper resolves Playwright from the
central App snapshot's `node_modules`. It preserves the effective graph/bin,
Agent, Runtime, Composition archive/tarball, runtime lock, source, authority,
private per-run graph, and cleanup guards from the committed owner runner.
The driver honors the incoming `TMPDIR` as the browser-temp base and uses
`EXIT` cleanup for the browser root, private graph, App symlink, and dist.

Added the unique central suite entry:

```text
app e2e-m2-ordinary-committed-driver-gate sh /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-ordinary-committed-driver-gate/run-central-m2-ordinary.sh "$PWD"
```

The driver performs a Playwright `--list` pre-build check and fails unless the
ordinary grep reports exactly `Total: 1 test in 1 file`, then runs only
`M2 ordinary extension batch`.

## Static evidence

Passed:

```text
sh -n .../run-central-m2-ordinary.sh
node --check .../chromium-env-smoke.mjs
absolute driver/helper realpath and executable/file checks
unique suite count and absolute-suite-path checks
git merge-base --is-ancestor 7d42fcd3a HEAD
git merge-base --is-ancestor 8c0e1f799 HEAD
```

The App worktree remained clean; no product, dependency, lock, schema, pin,
or API source was changed. No direct local driver, browser, socket, full, or
dirty-source run was made.

## Central evidence

Submitted exactly once through the central service:

```bash
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test ap2-m2-ordinary-committed-driver-gate e2e-m2-ordinary-committed-driver-gate)
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test ap2-m2-ordinary-committed-driver-gate-e2e-m2-ordinary-committed-driver-gate-1020214054-27865
```

The pre-build collection selected one ordinary test, the Chromium smoke
passed, the exact Agent/Runtime source tuple was reported, and the hosted App
build passed. The one test then failed at the first ordinary UI expectation:

```text
tests/e2e/local/three-products.spec.ts:1155
Expected: "2 markers"
Received: "No markers — press B at each phase."
```

The summary element was present but had no seeded markers. The action was not
clicked, so no command capture or later commit/retry/restart/undo assertions
ran. Full retained first-failure context is in
`workers/ap2-m2-ordinary-committed-driver-gate/central-first-failure.md` and
the central result `log.txt`/`summary`. The binary Playwright trace path was
reported in the central output but removed by the required `EXIT` cleanup.

## Decision and next step

The absolute worker-record driver and external helper were required because the
clean App target did not contain the previously named runner. The helper's
module-resolution adaptation was necessary once it moved outside App; it does
not alter product behavior. Do not infer command-path, ten-command ownership,
Runtime acceptance, retry, restart, or undo evidence from this run. The App
fixture owner should investigate why the current committed Scene Markers
surface starts with no markers and submit a reviewed follow-up gate if needed.
