# Run on main: App original parent split, current paired-seek source

Status: **one-run packet; do not execute in this worker**.

This is the PLAN D01 original parent-split proof on the integrated paired-seek
successor. It reuses the existing normal three-products driver, fixture,
assertions, credential guards, and `playwright.parent-split.config.ts`. It is
not a new driver, graph, selector, timeout, Player policy, fps policy,
tolerance, callback, or protocol.

## Exact source and review ancestry

The immutable App source for this packet is the worker's integrated source,
not a moving branch tip:

| purpose | ref / review fact | commit (40) | tree (40) |
|---|---|---|---|
| App under test | `tl/integration` source at packet composition; publish as `hub/timeline/app/tl/integration` | `435e76eb3f2dcaa0324ed69d4c019ab9c32bfbef` | `daf4e71ba71ebaf6a2bc8b6cd6e66fc13d762273` |
| r44 paired seek fix | `tl/app-m2-split-late-same-frame-paired-fix-r44` | `e1c0d8d52bd37c792368523ce8a6bfc7a55ad40a` | `51534291177131094cc8da49a02792be21b59c5a` |
| r45 independent review | `tl/app-m2-split-late-frame-pair-independent-review-r45`, **APPROVE** | `e1c0d8d52bd37c792368523ce8a6bfc7a55ad40a` | `51534291177131094cc8da49a02792be21b59c5a` |
| integration merge | `2b85341ef` merge of r44 | `2b85341ef724a15f34179e270a7acf323ac7b878` | `5ea64a704797fd034fb5fd184832448ae6b12ce0` |

The exact source has both `e1c0d8d52` and `2b85341ef` as ancestors. The
cached hub integration ref may lag; main must refuse to run unless the
resolved `hub/timeline/app/tl/integration` (or its exact source keeper)
resolves to `435e76eb…` / `daf4e71b…`. Do not substitute the older hub value
or a later moving tip without recording a new packet.

The approved fa20 credential correction is reused at blob level, unchanged;
its commit is intentionally not claimed as an ancestor of the integrated
merge:

| existing packet file | exact SHA-256 | fa20/current blob |
|---|---|---|
| `tests/e2e/local/parent-split-command.spec.ts` | `48938cfeffed2f3d6180206a4e7744c00979b31a14021f61c66ff98638f1f574` | `b01afea2421e3a55e3764daf475c6fa62bc2cf43` |
| `playwright.parent-split.config.ts` | `7eb1bff0269a554f1b9bfd5d750c622cec07b3472827f68290874fc4b690bad4` | `401ef0be0de28204b1af64acb7ff1068c0b366a4` |
| `scripts/testing/current013-parent-split.mjs` | `93c0a21a35ca9a6d254aa12ad7150994ff870e1f7eeac4ecf78172d4a05c86b7` | `f6c5233f2448e400cabd356154667436fc2a6b7b` |
| `scripts/testing/current013-parent-split.test.mjs` | `0cd2e7cbbef272e5ac8d8f6ea5e515498fa6dc78c4815c6658a835937b046449` | `35cf6677c4ac61cfcad4514ed677b92496ddce96` |

The current packet files must compare byte-for-byte with these values before
the actual. The current source includes the reviewed late same-frame producer
and consumer pair; do not add or alter any Player behavior, fps/tolerance,
selector, or timeout.

## Immutable paired dependency tuple

The existing launcher and source guards require this exact tuple:

| dependency | commit / tree | release evidence |
|---|---|---|
| Agent/Astrid execution | `6efc81500a0e0688c2bb41e736503f0fc3e04abb` / `2ed2b8a12b5b3391ca221ba6ff05390f71a73556` | existing pinned execution source |
| Agent vendor in App | `091aa23ec83ea05ffd3b0115a640230d51c8c429` / `e3ae90fe482ba6cad6c3f94069127faf76ebceb6` | existing vendor provenance |
| Runtime producer and App lock | `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c` / `d3a290b407fa61e6ab2d476f50c068073f70df00` | published Runtime 0.2.14, 76 artifacts |
| Runtime producer digest | `sha256:54205b3ecb55038e416b31af936c9af26afa30dc1b05da16157ee4d861fe05ac` | exact `runtime.lock.json` / manifest value |
| Composition carrier | `0.0.13`, archive SHA-256 `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738` | exactly 77 safe regular archive files |

Use the existing private public13 graph and normal fixture. Do not install,
repack, mutate, or replace shared `node_modules`; a missing private graph is a
main-machine prerequisite failure, not permission to make a new graph.

## One mandatory case and zero-failure rule

The existing source is:

- `tests/e2e/local/parent-split-command.spec.ts`, exactly one test:
  `M2 native parent split preserves raw closure through lost ACK, restart,
  retry and Runtime inverse`;
- `playwright.parent-split.config.ts`, which selects the normal
  `three-products` fixture, one worker, and the existing output directory;
- `scripts/testing/current013-parent-split.mjs`, whose source/credential/list
  guards remain the authority for this packet.

The mandatory collection preflight must report **exactly 1 test in 1 file**.
The one actual must exit 0 with one passed and zero failed, skipped, or
unexpected tests. The existing test must retain all of its assertions:

1. normal connected App/Runtime/Astrid setup and the seeded parent clip at
   rational `30000/1001` fps;
2. `clip.split` at `on: 1`, with the exact raw/opaque closure and source
   identity preserved in both resulting clips;
3. first commit acknowledgement deliberately lost, outbox retry state, the
   exact original request body and idempotency key after reload and Runtime
   restart;
4. exact retry receipt, then guarded `timeline.inverse` undo restoring the
   original document; and
5. empty legacy composition-revision traffic and empty renderer/export
   traffic.

Any non-zero exit, extra collected test, failure, skip, flaky result, source
drift, unexpected retained HTTP failure, legacy writer request, or duplicate
actual is a failed run. Stop and retain evidence; do not rerun or reinterpret
it as a pass.

## Main-machine private paths and pure preflight

The App-machine-only runner needs a private source/graph/credential setup that
is not available in this worker. Main should use short, physical mode-0700
paths; the path to every resolved temporary directory, Chromium profile, and
Unix socket must be less than 100 characters. The following names are the
packet's concrete layout, not new authority:

```bash
set -Eeuo pipefail
MAIN=/home/user/work/tl-split-main-435e
APP=$MAIN/source/app-435e
AGENT=$MAIN/source/agent-6ef
AGENT_VENDOR=$MAIN/source/agent-vendor-091
RUNTIME=$MAIN/source/runtime-95
GRAPH=$MAIN/graph/public13
PRIVATE=$MAIN/private
EVIDENCE=$MAIN/evidence/split-current
NODE=$MAIN/node-v20.19.4-linux-x64/bin/node
CHROME=/opt/pw-browsers/chromium-1194/chrome-linux/chrome
TMP=$MAIN/t
PROFILE=$MAIN/p
SOCKET=$MAIN/s
CONFIG=$APP/playwright.parent-split.config.ts
SHORT=/tmp/tl-split-435e

test "$("$NODE" --version)" = v20.19.4
test -x "$CHROME"
for d in "$MAIN" "$APP" "$AGENT" "$AGENT_VENDOR" "$RUNTIME" "$GRAPH" "$PRIVATE" "$EVIDENCE" "$TMP" "$PROFILE" "$SOCKET" "$SHORT"; do
  test -d "$d" && test ! -L "$d"
done
for d in "$PRIVATE" "$EVIDENCE" "$TMP" "$PROFILE" "$SOCKET" "$SHORT"; do
  test "$(stat -c '%a' "$d")" = 700
done
test "${#TMP}" -lt 100; test "${#PROFILE}" -lt 100; test "${#SOCKET}" -lt 100
test "$(git -C "$APP" rev-parse HEAD)" = 435e76eb3f2dcaa0324ed69d4c019ab9c32bfbef
test "$(git -C "$APP" rev-parse HEAD^{tree})" = daf4e71ba71ebaf6a2bc8b6cd6e66fc13d762273
git -C "$APP" merge-base --is-ancestor e1c0d8d52bd37c792368523ce8a6bfc7a55ad40a HEAD
git -C "$APP" merge-base --is-ancestor 2b85341ef724a15f34179e270a7acf323ac7b878 HEAD
test -z "$(git -C "$APP" status --porcelain --untracked-files=normal)"
test -z "$(git -C "$AGENT" status --porcelain --untracked-files=normal)"
test -z "$(git -C "$AGENT_VENDOR" status --porcelain --untracked-files=normal)"
test -z "$(git -C "$RUNTIME" status --porcelain --untracked-files=normal)"
```

Also compare the four packet files against the exact SHA-256 table above,
verify `APP/node_modules` resolves only into the private `$GRAPH/node_modules`,
verify the Runtime manifest has 76 artifacts and the Composition archive has
77 safe regular files with SHA-256 `9412…d54738`, and verify the existing
mode-0600 Runtime product credential is not an owner/admin/worker credential.
The direct door port must be free. These are pure identity, permissions,
archive, and source checks; they start no browser, Runtime, Vite, socket,
build, install, or test.

The existing source-only driver check may then be run from `$APP` with the
normal private paths. It must print the source identities and pass the
existing vendor-lock/provenance checks; do not set
`TIMELINE_CURRENT013_RUN=1` during preflight:

```bash
cd "$APP"
env -i \
  HOME="$MAIN/h" LANG=C.UTF-8 PATH="$MAIN/node-v20.19.4-linux-x64/bin:/usr/bin:/bin" \
  ASTRID_CHECKOUT="$AGENT" ASTRID_RUNTIME_CHECKOUT="$RUNTIME" \
  ASTRID_PYTHON=/home/user/work/venv-agent/bin/python \
  ASTRID_RUNTIME_PYTHON=/home/user/work/venv-runtime/bin/python \
  TIMELINE_CURRENT013_APP_SHA=435e76eb3f2dcaa0324ed69d4c019ab9c32bfbef \
  TIMELINE_CURRENT013_APP_TREE=daf4e71ba71ebaf6a2bc8b6cd6e66fc13d762273 \
  TIMELINE_CURRENT013_AGENT_SHA=6efc81500a0e0688c2bb41e736503f0fc3e04abb \
  TIMELINE_CURRENT013_RUNTIME_SHA=95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c \
  TIMELINE_CURRENT013_AGENT_VENDOR_CHECKOUT="$AGENT_VENDOR" \
  TIMELINE_CURRENT013_RUNTIME_PRODUCER_CHECKOUT="$RUNTIME" \
  PRIVATE13_NODE_MODULES="$GRAPH/node_modules" \
  TIMELINE_CURRENT013_PRIVATE13_READY="$PRIVATE/READY" \
  TIMELINE_CURRENT013_PRIVATE13_LEASE="$PRIVATE/LEASE" \
  TIMELINE_CURRENT013_SHORT_TMPDIR="$SHORT" \
  TIMELINE_CURRENT013_CONFIG_PATH="$CONFIG" \
  PLAYWRIGHT_CHROMIUM_EXECUTABLE="$CHROME" \
  WORKSPACE_RUNTIME_TOKEN_FILE="$PRIVATE/product-credential.json" \
  "$NODE" --input-type=module -e '\
    import { readCurrent013ParentSplitInputs, checkCurrent013ParentSplitSources } from "./scripts/testing/current013-parent-split.mjs";\
    const input = readCurrent013ParentSplitInputs(process.env, process.cwd());\
    console.log(JSON.stringify(checkCurrent013ParentSplitSources(input)));\
  '
```

The direct `--list` check is mandatory and is the only collection command in
preflight. It must select one test, once:

```bash
cd "$APP"
env -i HOME="$MAIN/h" LANG=C.UTF-8 PATH="$MAIN/node-v20.19.4-linux-x64/bin:/usr/bin:/bin" \
  ASTRID_CHECKOUT="$AGENT" ASTRID_RUNTIME_CHECKOUT="$RUNTIME" \
  ASTRID_PYTHON=/home/user/work/venv-agent/bin/python \
  ASTRID_RUNTIME_PYTHON=/home/user/work/venv-runtime/bin/python \
  npm_config_cache="$MAIN/n" npm_config_offline=true \
  npm exec -- playwright test \
    --config "$CONFIG" tests/e2e/local/parent-split-command.spec.ts --list
# Required: exactly one title, one file, and “Total: 1 test in 1 file”.
```

If the private driver, exact pinned checkouts, credential, or normal public13
graph is absent, stop here. The worker cannot recreate or qualify an
App-machine-only browser/localhost graph. Main may recreate the private source
keepers only from these immutable pins (without touching shared installs),
then repeat the preflight; it must not choose another source:

```bash
git -C "$APP" rev-parse HEAD HEAD^{tree}
git -C "$AGENT" rev-parse HEAD HEAD^{tree}
git -C "$AGENT_VENDOR" rev-parse HEAD HEAD^{tree}
git -C "$RUNTIME" rev-parse HEAD HEAD^{tree}
git -C "$APP" show-ref --verify refs/remotes/hub/timeline/app/tl/integration
```

The last command is a publication check, not permission to use a stale hub
ref. The graph remains the existing normal fixture graph; no `npm install`,
package extraction, graph build, or shared-node_modules mutation is allowed.

## One exact main command

After every preflight check passes, run this existing Playwright command once
from `$APP`, with no `--grep`, selector override, timeout override, retry loop,
or alternate config. `env -i` keeps `NODE_OPTIONS`, `NODE_PATH`, `PYTHONHOME`,
and all `LD_*` variables unset for the harness children.

```bash
cd "$APP"
env -i \
  HOME="$MAIN/h" LANG=C.UTF-8 PATH="$MAIN/node-v20.19.4-linux-x64/bin:/usr/bin:/bin" \
  ASTRID_CHECKOUT="$AGENT" ASTRID_RUNTIME_CHECKOUT="$RUNTIME" \
  ASTRID_PYTHON=/home/user/work/venv-agent/bin/python \
  ASTRID_RUNTIME_PYTHON=/home/user/work/venv-runtime/bin/python \
  TIMELINE_CURRENT013_APP_SHA=435e76eb3f2dcaa0324ed69d4c019ab9c32bfbef \
  TIMELINE_CURRENT013_APP_TREE=daf4e71ba71ebaf6a2bc8b6cd6e66fc13d762273 \
  TIMELINE_CURRENT013_AGENT_SHA=6efc81500a0e0688c2bb41e736503f0fc3e04abb \
  TIMELINE_CURRENT013_RUNTIME_SHA=95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c \
  TIMELINE_CURRENT013_AGENT_VENDOR_CHECKOUT="$AGENT_VENDOR" \
  TIMELINE_CURRENT013_RUNTIME_PRODUCER_CHECKOUT="$RUNTIME" \
  PRIVATE13_NODE_MODULES="$GRAPH/node_modules" \
  TIMELINE_CURRENT013_PRIVATE13_READY="$PRIVATE/READY" \
  TIMELINE_CURRENT013_PRIVATE13_LEASE="$PRIVATE/LEASE" \
  TIMELINE_CURRENT013_SHORT_TMPDIR="$SHORT" \
  TIMELINE_CURRENT013_CONFIG_PATH="$CONFIG" \
  WORKSPACE_RUNTIME_TOKEN_FILE="$PRIVATE/product-credential.json" \
  TIMELINE_BUNDLE_AGENT_HEAD=6efc81500a0e0688c2bb41e736503f0fc3e04abb \
  TIMELINE_BUNDLE_RUNTIME_HEAD=95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c \
  PLAYWRIGHT_CHROMIUM_EXECUTABLE="$CHROME" PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers \
  ASTRID_APP_DIRECT_DOOR_PORT=17340 \
  TMPDIR="$TMP" XDG_RUNTIME_DIR="$SOCKET" \
  npm_config_cache="$MAIN/n" npm_config_offline=true PWTEST_CACHE_DIR="$MAIN/w" \
  VITE_CACHE_DIR="$MAIN/v" XDG_CACHE_HOME="$MAIN/c" \
  PLAYWRIGHT_OUTPUT_DIR="$EVIDENCE" \
  npm exec -- playwright test \
    --config "$CONFIG" tests/e2e/local/parent-split-command.spec.ts \
  > "$EVIDENCE/playwright.log" 2>&1
```

The command carries the exact source, private-graph, credential, Runtime,
Agent, and Chromium assignments used by the source preflight. Preserve the
evidence directory on failure, including the Playwright trace and failure
context. A passing result is only the exact one-test, zero-failure result
above.

## Scope and next step

This worker performed read-only ancestry/blob/source checks and documentation
only. It did not run the actual, browser, localhost/live-socket, build,
install, full suite, or create a dependency graph. Main should execute the
single command only after the exact source publication and private normal
fixture preflight pass; report the exact source tuple, list output, exit/count,
and retained failure evidence.
