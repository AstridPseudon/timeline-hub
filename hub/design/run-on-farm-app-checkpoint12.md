# App 12Z checkpoint full — test-farm request

Status: **HOLD**. The farm lead may change this to READY only after the exact
source checkout, named leases, toolchain, graph, and preflight below are
verified. This packet requests one existing-wrapper full-suite run; it does not
authorize a local full run, browser run, build, install, graph extraction, or
external-network operation. Farm approval is central.

## Scope and immutable source tuple

This is the App checkpoint for the hub integration source selected at packet
creation time. The farm must use a detached checkout, not the moving integration
worktree directly.

| role | exact identity / path |
|---|---|
| Hub source | `timeline/app/tl/integration`, App commit `a8a3f23313e92c523359b3b37c3a63bd526dbb5e`, tree `79f5c76b96d4be75959d67a57197dee5f9546225` |
| App keeper | `/home/user/work/wt/app-pin-a8a3f233`; obtain with `request-checkout app a8a3f23313e92c523359b3b37c3a63bd526dbb5e "App12Z exact current integration source for farm packet r49"` if absent |
| App lease | `/home/user/work/wt/app-pin-a8a3f233/LEASE`, lease name `app12z-current-integration-a8a3f233-farm-full`; keep active through farm result and postflight |
| Current matched Agent source | `/home/user/work/wt/agt-pin-091aa23e`, commit `091aa23ec83ea05ffd3b0115a640230d51c8c429`, tree `e3ae90fe482ba6cad6c3f94069127faf76ebceb6` |
| Agent source module | `astrid/packs/rendering/elements/catalog.ts`, SHA-256 `fc53e754326cd9fc9bc3e5233026fbc70ac6a4c5fd81a9d0b2c857665f13c661` |
| Agent publication witness | `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-gate13-current.md`, SHA-256 `1838b2afd04426c07bff6284a2584dbe5ffb0590e5db050e4145db4acb46126b` |
| Published Runtime 0.2.14 / Runtime95 | `/home/user/work/wt/rt-pin-95bd3c5f`, commit `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`, tree `d3a290b407fa61e6ab2d476f50c068073f70df00` |
| Runtime producer | version `0.2.14`; artifact-version SHA-256 `54205b3ecb55038e416b31af936c9af26afa30dc1b05da16157ee4d861fe05ac`; manifest SHA-256 `a902387c6a2315374f7e73511feea47da30191aba831b48820b3864b773a532d`; schema `sha256:7d4afa05962b8cd61643213fc79cdde41e16046c4e2a777bd299b48af0f31816` |
| Runtime generated artifacts | exactly **76** files |
| Published Composition C13 | `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/artifacts/banodoco-timeline-composition-0.0.13.tgz`, SHA-256 `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`, `58,477` bytes, exactly **77** regular members |

The App source currently has package SHA-256
`a4dc9fcc02b1769ba8472f551349f7875774b07ad0830c7260eb88d2db8292fd`, lock
SHA-256 `7f1bfcea48cef38d4c6f1163aa34190b8d5e71c9f08c7378e01a962d6696fc14`,
and `runtime.lock.json` SHA-256
`770352eaf1d015e90fca0ed2f1893749b73b69356ca82a7223b2573276fe485e`. The
lock must continue to name Runtime95. The staged Composition 0.0.14 work is
not part of this packet: do not force-pin C14, do not use its archive, and do
not substitute an older physical source tuple.

The existing wrapper also carries a compatibility witness for frozen Agent
scope `6efc81500a0e0688c2bb41e736503f0fc3e04abb` / tree
`2ed2b8a12b5b3391ca221ba6ff05390f71a73556`. That witness is a wrapper guard;
the current matched execution/vendor source for this App packet remains the
separately named `091aa23e` source above.

## Existing wrapper and literal farm command

Reuse the reviewed wrapper byte-for-byte:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m4-canonical-full-current-execute-r21/canonical/run-current-published014-full-canonical.sh`

Wrapper SHA-256: `751d0ef413fc6382ef40e640e7e8468dceef9949117d9ce8d58cf4986d9b1d0f`.
Its existing required preload is
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/app/notes/snapshot-vitest-runner.cjs`,
SHA-256 `f303229cd36c7878c739cad7e7669e3bf66ee416bd927434aca1addeab059f52`.
Do not edit either file or introduce another runner.

The farm service supplies an immutable snapshot root as the command's current
directory and keeps the App keeper separate; invoking this wrapper directly
from the keeper is invalid because its existing custody guard requires those
two roots to differ. The command is submitted to the existing service in that
snapshot cwd (there is intentionally no `cd` to the keeper). With the farm's
named READY marker at
`$ORCH/workers/tf-app12z-current-integration/READY` and run root at
`$ORCH/workers/tf-app12z-current-integration/full-run`, the one command is:

```sh
flock -w 600 /home/user/work/.app-m1-browser.lock \
  env -i \
  HOME=/root \
  LANG=C.UTF-8 \
  PATH=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin:/usr/local/bin:/usr/bin:/bin \
  TIMELINE_CURRENT_FULL_RUN=1 \
  TIMELINE_CURRENT_FULL_READY=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/tf-app12z-current-integration/READY \
  TIMELINE_CURRENT_FULL_RUN_ROOT=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/tf-app12z-current-integration/full-run \
  bash /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m4-canonical-full-current-execute-r21/canonical/run-current-published014-full-canonical.sh full
```

The service must preserve the wrapper's child argv exactly:

```text
npm test -- --maxWorkers=2 --configLoader=runner --no-cache
```

The suite name is `app-full-published014-checkpoint12-a8a3f233`; files must be
empty. There is no `|| true`, retry, test filter, skip, changed expected-failure
set, or summary-only result path. A nonzero child exit, nonzero postflight,
missing/unrun file, unexpected failure, or zero collected tests is FAIL.

## Farm prerequisites and protected paths

The farm lead must collect every failure in one preflight and stop before the
child if any item is missing.

1. Verify App keeper commit/tree/clean status, the central snapshot tree, the
   exact active lease `app12z-current-integration-a8a3f233-farm-full`, and the
   `timeline/app/tl/integration` hub source identity. The checkout requested by
   this worker is not a qualification until the dispatcher returns it and the
   farm verifies all 40-hex identities.
2. Verify the separately named Agent source, Runtime95 checkout, Runtime lock,
   C13 archive, wrapper, preload, package/lock hashes, and all76/all77 counts.
   Shared checkouts, venvs, runtimes, graphs, caches, and Node installs are
   read-only.
3. Use Node **20.19.4**, raw executable SHA-256
   `43d6cf63f2a460b463eba6b19df5e9a259771c56f11b5130e04178a15bb99490`, from
   `/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node` and npm
   `10.8.2` from the same toolchain. If that exact path is absent, the retained
   existing archive may be used only in a private farm-owned destination:
   `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-node20.19.4-retained-app.tgz`,
   archive SHA-256 `e481653ec961f88c9cb8f034740afca3ed1bbc5fa3f9d56efde0eb502372481f`.
   Verify the extracted `bin/node` against the raw SHA and `v20.19.4`; never
   use `/opt/node20` (`v20.20.0`) as a substitute. No package installation is
   part of this packet.
4. Use the existing qualified physical graph
   `/home/user/work/app-m3-private13-normal-lock-install-units-r6-owned/node_modules`
   with READY marker
   `/home/user/work/app-m3-private13-normal-lock-install-units-r6-owned/READY`
   and lease
   `/home/user/work/app-m3-private13-normal-lock-install-units-r6-owned/LEASE`.
   It must not be a symlink into `/home/user/work/app/node_modules` or a shared
   runtime. If the farm needs transport, the existing archive is
   `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/artifacts/app-public13-main-node-modules-r25.tgz`,
   SHA-256 `a1ef11b292548c22caa36cc38c683a67b01d9244f8389aade9405e5a7dca581e`,
   `130,648,897` bytes. Extract only to a new private farm-owned root after
   checking the sidecar; do not extract over any shared install and do not
   perform a new npm install.
5. The existing read-only Python environments are
   `/home/user/work/venv-agent/bin/python` and
   `/home/user/work/venv-runtime/bin/python`. They are prerequisites for the
   existing Runtime/Agent-backed fixture paths, not replacement interpreters
   for the Node suite.
6. Keep the test's existing credential setup. `DirectHarness` creates a mode
   `0700` private temp root, then uses `<tmp>/realm`, `<tmp>/support`,
   `<tmp>/support/credentials/owner.token`,
   `<tmp>/product-credential.json` (mode `0600`), and
   `<tmp>/support/discovery.json`. The child receives
   `WORKSPACE_RUNTIME_TOKEN_FILE=<tmp>/product-credential.json` and the
   existing actor `astrid-e2e-product`; it must not receive a printed token or
   a pre-seeded secret. Runtime starts with
   `/home/user/work/venv-runtime/bin/python -m runtime_protocol.cli` through
   the existing harness. Credential setup is in
   `tests/e2e/local/support/harness.ts`; do not invent a credential file or
   auth route.
7. Verify Chromium is already available at
   `/opt/pw-browsers/chromium-1194/chrome-linux/chrome` (qualified version
   `141.0.7390.37`) and that the farm's browser lock is free. Use private
   mode-`0700` `TMPDIR`, `XDG_RUNTIME_DIR`, browser profile, npm/Vite/Vitest
   cache, and output directories under the named run root; keep the longest
   socket path below 100 bytes. Unset `NODE_OPTIONS`, `NODE_PATH`, every
   `LD_*`, and `PYTHONHOME` for any Remotion/pack-host child locally.
8. Enforce the farm disk floor before staging, before the child, and after
   postflight: at least `12,000,000,000` available bytes (`df -B1`), with the
   farm's absolute hard stop at 5 GiB. Do not delete protected leases or shared
   dependencies to make room.

## Guards and expected output

The wrapper's source, graph, package, Runtime, Composition, vendor-provenance,
credential-boundary, and pre/post snapshots remain authoritative. The farm
must retain `full-before.json`, `full-after.json`, raw `full.log`,
`classification.md`, and the central result record. Compare snapshots byte-for-
byte and report source/graph postflight separately from child status.

The only authorized expected failures are the three existing original drag
cases:

```text
src/tools/video-editor/hooks/useClipDrag.test.tsx:774
src/tools/video-editor/hooks/useClipDrag.test.tsx:1120
src/tools/video-editor/hooks/useClipDrag.test.tsx:1230
```

`check-known-failures.mjs` must report exactly three audited markers and zero
forbidden markers. The prior green r36 evidence was
`19,454 passed / 3 authorized expected failures / 0 unexpected` on the older
App tree `757ff3e20c344afd87b15d1bcea273738011987c` (central result
`app-m4-agentchat-fixed-current-one-full-r36-app-full-published014-agentchat-fixed-r36-07d86990c-1021075701-20810`). It is retained evidence for the wrapper, not a current-tree count; the current App deltas require the new checkpoint result.

The C13/public13 dependency has a bounded known warning: seven historical
public13 TypeScript duration diagnostics disappear only under the not-yet-
authorized Composition14 adoption. Do not force C14, hide those diagnostics,
or relabel a C13 warning as an App pass; record the exact diagnostic and keep
the public13/C13 tuple intact.

No credential value, bearer token, owner token, or secret environment value may
appear in stdout, stderr, retained logs, snapshots, or the result. Paths and
redacted status metadata are allowed. A secret-output finding is a hard FAIL.

## Latest targeted source deltas

These are the current-tree changes after the older green r36 full and are the
reason a new checkpoint is useful. They were qualified with targeted evidence
under the lighter interim rule; they are not silently folded into the older
full result.

| integrated delta | targeted evidence |
|---|---|
| `d78f40a9b` occurrence-media typing/refusal repair | `occurrenceMediaCapture.test.ts`: 5/5; capture + `commitSession.test.ts`: 84/84; target-only TypeScript had 0 owned-file diagnostics |
| `2ded0e0ec` placement/provider typing repair | Focused Vitest: 253 passed across 5 files; targeted ESLint and `git diff --check` passed |
| `5ca458868` popup parent occurrence-media passthrough | Focused Vitest: 128 passed across 4 files; Astrid editor test: 13 passed; targeted ESLint and `git diff --check` passed; independent safety review recorded 214 controls |
| `88a417ecc` retained public-trim record custody hardening | Existing wrapper syntax and `node --test scripts/testing/public-trim-action-wrapper.test.mjs` passed; central planted-failure control propagated child 7 → wrapper 7 → service FAIL |

The current HEAD also retains the existing queued browser packets for the 18Z
checkpoint (automatic, public Trim, original split, and prompt/settings). They
remain queued evidence and are **not merge prerequisites** for this packet;
do not merge, delete, or relabel them while preparing the farm run.

## What this packet does not claim

No farm result exists yet. This worker did not run the full suite, browser,
build, install, graph, credential, or external-network operation. The farm
owner must report one exact result with App/Agent/Runtime/Composition source
and tree identities, counts, exit and postflight status, raw log path, all
preflight failures if refused, and the bounded warning classification.
