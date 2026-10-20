# App five-case Node20 private environment repair

## Result

Repaired the retained controller's run-local Node20 selection without changing
the frozen five-case source tuple or any qualification guard.

The controller now honors the existing `ASTRID_NODE_EXECUTABLE` injection
contract for a private run, while retaining its original frozen executable
path as the default. The fixed Node version and SHA-256 digest remain in the
controller and are still checked by `assertNode20`.

Changed product source:

- `tests/e2e/timeline/viewing-parity/tab-audio.controller.mjs`

No fixture, instrument, case, grant, marker, source tuple, lease, cache,
native-channel, transfer, negative, or browser code changed.

## Repaired private runtime

The previously admitted path was absent. I installed only the exact
`node@20.19.4` npm package into a private worker overlay, outside shared
`node_modules` and outside the App worktree. Its executable reported:

```text
v20.19.4
43d6cf63f2a460b463eba6b19df5e9a259771c56f11b5130e04178a15bb99490
```

The run-local executable was supplied as:

```text
ASTRID_NODE_EXECUTABLE=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-fivecase-node20-private-env-fix/node20-install/node_modules/node/bin/node
```

The shared App `node_modules` tree was not written. No Node22 executable was
relabeled or wrapped, and no version, hash, or output was fabricated.

## Evidence

Before the repair, the exact retained failure was reproduced with the default
Node22 environment:

- controller subtest 8, `Node identity accepts the retained admitted executable and full hash`: failed with `ENOENT` for the absent frozen Node20 path;
- five-case discovery: failed because the same executable could not be spawned.

After the repair, with the private Node20 executable and private cache/temp
paths:

```text
ASTRID_NODE_EXECUTABLE=<private-node20> XDG_CACHE_HOME=<private-cache> TMPDIR=<private-temp> <private-node20> --test tests/e2e/timeline/viewing-parity/tab-audio.controller.test.mjs
9 passed, 0 failed, 0 skipped

ASTRID_NODE_EXECUTABLE=<private-node20> XDG_CACHE_HOME=<private-cache> TMPDIR=<private-temp> <private-node20> tests/e2e/timeline/viewing-parity/tab-audio.controller.mjs --discover <app-worktree>
discovered exactly 5 current native-codec-chrome155 parity cases
```

`git diff --check` passed. No browser, PCM, frame, render, transfer, live
socket, build, typecheck, duplicate, or full suite was run.

## Grant note

The retained controller's current grant check binds Node version and
executable digest, not the absolute executable path. No signed real grant was
edited. If an external fresh grant used by a later launch binds the old
absolute path, it must be replaced by a new manager-issued grant naming the
private run's executable path while retaining version `v20.19.4` and digest
`43d6cf63f2a460b463eba6b19df5e9a259771c56f11b5130e04178a15bb99490`.

## Next step

Run the controller's normal manager-controlled readiness/launch flow with a
fresh private Node20 environment and grant. Physical browser, PCM, render, or
parity qualification remains unverified by this repair.
