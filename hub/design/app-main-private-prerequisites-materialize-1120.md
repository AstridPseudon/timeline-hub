# App main private prerequisites materialization (1120)

This is the executable preparation for `auto1490`, `Trim0cc`, and `split92c`.
It addresses the actual REFUSED-PREFLIGHT results without changing product
code, the runner, or the framework. The previous split label `superseded435`
is not a source selection; the authoritative split source is `92c30b570`.

The preparation script is:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/app-main-private-prerequisites-materialize-1120.sh
```

Run it only after the r25 archive is published, with a new private root:

```bash
MAIN=/home/user/work/tl-app-main-private-r70 \
  /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/app-main-private-prerequisites-materialize-1120.sh
```

The script refuses to overwrite `MAIN`. It verifies every keeper, the existing
hub reachability, Node, the two existing venvs, the immutable graph archive,
and the exact peer versions before creating any private root. It clones each
App keeper with `--no-local --no-hardlinks --no-checkout`, checks out its exact
commit, and extracts the r25 graph into that private checkout. It never writes
to shared `.git`, `/home/user/work/app/node_modules`, a shared venv, or a
shared runtime. The three physical graph copies avoid a linked shared graph.

## Exact source and dependency tuple

| case | App commit | App tree | private keeper |
|---|---|---|---|
| `auto1490` | `1490fbfe90f83c7c7c380d5cb16ccfcc0e9dcfcf` | `8e242d1497841f391b6152ecd8d204143fa03b52` | `/home/user/work/wt/app-pin-1490fbfe` |
| `Trim0cc` | `0cc2583aaf07e89190b9344b5ac82849d6279586` | `320e74a93676c781e83885b86ec237b4a1465d80` | `/home/user/work/wt/app-pin-0cc2583a` |
| `split92c` | `92c30b570cf8105dc021a64874c258e6c950b841` | `c34d65b66481fd0015279451b175c53b7b5e8f4f` | `/home/user/work/wt/app-pin-92c30b57` |

The split source must also retain the reviewed `547da1a555cfe8514bc3f40a263ee56fdafd3d83`
ancestor. No `435e` source or old driver is authorized.

The immutable paired dependencies are:

- Agent/Astrid: `6efc81500a0e0688c2bb41e736503f0fc3e04abb`, tree `2ed2b8a12b5b3391ca221ba6ff05390f71a73556`, keeper `/home/user/work/wt/agt-pin-6efc8150`.
- Agent vendor: `091aa23ec83ea05ffd3b0115a640230d51c8c429`, tree `e3ae90fe482ba6cad6c3f94069127faf76ebceb6`, keeper `/home/user/work/wt/agt-pin-091aa23e`.
- Runtime: `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`, tree `d3a290b407fa61e6ab2d476f50c068073f70df00`, keeper `/home/user/work/wt/rt-pin-95bd3c5f`.
- Runtime producer digest: `sha256:54205b3ecb55038e416b31af936c9af26afa30dc1b05da16157ee4d861fe05ac`.
- Composition carrier: `0.0.13`, archive SHA-256 `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`, exactly 77 safe regular files.

If any keeper is absent, request it through the checkout service rather than
fetching or editing shared metadata:

```bash
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-checkout app 1490fbfe90f83c7c7c380d5cb16ccfcc0e9dcfcf 'exact App 1490 keeper'
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-checkout app 0cc2583aaf07e89190b9344b5ac82849d6279586 'exact App 0cc keeper'
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-checkout app 92c30b570cf8105dc021a64874c258e6c950b841 'exact App 92c keeper'
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-checkout agent 091aa23ec83ea05ffd3b0115a640230d51c8c429 'exact Agent vendor keeper'
```

The materializer checks the exact App objects and ancestor reachability from
the existing `refs/remotes/hub/timeline/app/tl/integration` ref. That is a
read-only check; absence means stop, not fetch.

## Node, graph, and private roots

Use only the existing exact Node binary:

```text
/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node
v20.19.4
```

Use the existing read-only environments:

```text
/home/user/work/venv-agent/bin/python
/home/user/work/venv-runtime/bin/python
```

The r25 graph artifact is:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/artifacts/app-public13-main-node-modules-r25.tgz
```

The authoritative transport audit and safe extraction recipe are in
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-app-public13-main-graph-1120.md`.
Its archive SHA is `a1ef11b292548c22caa36cc38c683a67b01d9244f8389aade9405e5a7dca581e`
and its Composition carrier SHA is `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`.

Its bytes must hash to the graph-tar SHA below. Extract it only into the new
private case roots. Its graph-tar SHA-256 is
`a1ef11b292548c22caa36cc38c683a67b01d9244f8389aade9405e5a7dca581e`; the
Composition carrier SHA remains `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`.
The materializer checks these versions from each
physical graph: `@banodoco/timeline-composition 0.0.13`, `react 18.3.1`,
`react-dom 18.3.1`, `remotion 4.0.509`, `@remotion/player 4.0.509`,
`three 0.185.1`, `playwright 1.60.0`, and `@playwright/test 1.60.0`.

The root and every `evidence`, `home`, `run`, and `cache` directory are
physical mode `0700` directories. Keep the existing source disk floors and
the measured serial envelope: approximately 5.420 GiB (`5,819,583,972`
bytes), with the established 2 GiB transient and 2 GiB safety reservations.
Keep socket paths below 100 bytes, use the reserved port `17340`, and run one
case at a time. The script creates no browser, build, install, server, or
actual output.

The direct short-temp root is `/tmp/tl-app-main-private-r70` (mode `0700`);
the script refuses to reuse it. Set the existing driver's
`TIMELINE_CURRENT013_SHORT_TMPDIR` to this path, and set its cache/output
variables to the matching private case `cache`, `run`, and `evidence` roots.

The existing driver must be run with `env -i`, a private `HOME`, and no
`NODE_OPTIONS`, `NODE_PATH`, `PYTHONHOME`, or `LD_*` leakage. Use the existing
Chrome/Chromium keeper from the packet; do not download or substitute one.

## READY, LEASE, and credential truth

The materializer deliberately does not write `READY`, `LEASE`, or a token.
Those files are proof, not placeholders. After materialization, invoke the
existing graph qualifier with the published r25 handoff as its transport
input, bound to the exact
private `node_modules` path, the 77-member Composition archive, the exact
Runtime all-76 manifest/digest, and the current source/pin tuple. Require the
qualifier to generate fresh `READY` and `LEASE` for that physical graph. Do
not copy the old r6 READY/LEASE or the older protected-environment report;
their source tuple is different. If the r25 handoff or qualifier is missing,
stop.

For the existing split driver, the resulting paths are supplied as
`TIMELINE_CURRENT013_PRIVATE13_READY` and
`TIMELINE_CURRENT013_PRIVATE13_LEASE`; both must be absolute physical files
from that qualifier, with `PRIVATE13_NODE_MODULES` set to the matching case's
physical `source/node_modules`. The materializer does not create or copy any
of these files. The published r25 handoff records the verified transport
inputs and the existing qualifier evidence; it does not authorize reusing
the old r6 path as current-tuple proof.

Provision the product credential only through the existing r69 normal helper,
not by writing JSON or inventing a token. The full r69 handoff is
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/app-main-existing-credential-setup-1120.md`.
The authoritative flow is
`tests/e2e/local/support/harness.ts`: `DirectHarness.start()` calls
`provisionCredential(PRODUCT_ACTOR, ...)`; that helper POSTs the owner-auth
credential to the current private Runtime `/v1/credentials`, expects HTTP 201,
and writes `{ token, actor_id }` with mode `0600`. Use the private normal
realm created by that helper. Verify path, mode, actor, scope, and realm
without printing the secret. Reject owner/admin/worker/host actors and any
cross-realm credential. If the r69 output does not identify this existing
helper and its normal realm, stop.

The helper must remain alive in the same parent process as the existing list
and actual driver. The executable setup shape is:

```bash
cd "$APP"
env -i HOME="$CASE/home" LANG=C.UTF-8 \
  PATH="/home/user/work/toolchain/node-v20.19.4-linux-x64/bin:/usr/bin:/bin" \
  ASTRID_CHECKOUT=/home/user/work/wt/agt-pin-6efc8150 \
  ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-95bd3c5f \
  ASTRID_PYTHON=/home/user/work/venv-agent/bin/python \
  ASTRID_RUNTIME_PYTHON=/home/user/work/venv-runtime/bin/python \
  /home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node --import tsx --input-type=module <<'NODE'
import { DirectHarness } from './tests/e2e/local/support/harness.ts';
const harness = await new DirectHarness().start({ seed: false });
// Invoke the existing Main list/actual phases here while harness is alive.
// Pass only realmId, runtimeInstanceId, and credentialPath; set
// WORKSPACE_RUNTIME_TOKEN_FILE=credentialPath; never print token.
// Finally: await harness.stop().
NODE
```

`APP` must be one of the exact private case sources and `CASE` its matching
mode-0700 case root. This setup performs no project/film/media write before
the existing Main path. Do not detach the process: teardown would remove the
ephemeral realm and credential.

After those two proofs, preserve the packet's source, actor, realm, credential,
pin, short-socket, overlay/cache, and postflight guards. The existing list
preflight must still collect exactly one test in one file with zero failures,
skips, or unexpected tests. Only then may the orchestrator authorize the one
existing actual command; no new runner, selector, retry loop, browser flow, or
framework is introduced here.

For `split92c`, the existing packet blobs remain immutable and must hash to:

| file | SHA-256 |
|---|---|
| `tests/e2e/local/parent-split-command.spec.ts` | `48938cfeffed2f3d6180206a4e7744c00979b31a14021f61c66ff98638f1f574` |
| `playwright.parent-split.config.ts` | `7eb1bff0269a554f1b9bfd5d750c622cec07b3472827f68290874fc4b690bad4` |
| `scripts/testing/current013-parent-split.mjs` | `93c0a21a35ca9a6d254aa12ad7150994ff870e1f7eeac4ecf78172d4a05c86b7` |
| `scripts/testing/current013-parent-split.test.mjs` | `0cd2e7cbbef272e5ac8d8f6ea5e515498fa6dc78c4815c6658a835937b046449` |

## All missing dependencies in one list

The remaining prerequisites are:

1. exact private App keepers for `1490fbfe`, `0cc2583a`, and `92c30b57`, with clean trees and existing hub reachability;
2. exact Agent `6efc`, Agent vendor `091aa`, and Runtime `95bd` keepers plus their clean-tree and tree-hash checks;
3. the r25 immutable graph archive, its 77-safe-member proof, the exact Runtime all-76 manifest/digest, and a fresh private READY/LEASE pair emitted by the existing graph qualifier after the archive checks;
4. Node `20.19.4`, the existing Agent/Runtime venvs, the packet's existing Chromium, and no dependency installation or package-version substitution;
5. new physical mode-0700 run/cache/HOME/evidence roots, the source disk envelope and floors, socket length below 100, reserved port `17340`, and serial execution;
6. the r69 normal-helper product credential in the private normal realm, physically mode `0600`, with actor/scope/realm checks and no hand-written token;
7. the exact packet driver/spec/config/blob hashes, Composition archive hash, source ancestor/hub checks, clean postflight, and untouched overlay/cache guards.

No actual, browser, build, install, graph build, or new graph was performed by
this preparation. The historical main attempts remain REFUSED-PREFLIGHT with
zero processes/tests; that is expected until the two proof-producing steps
above are completed by the orchestrator using the existing systems.
