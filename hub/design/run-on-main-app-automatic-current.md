# Run on main: App automatic placement, current source

Status: **one-run packet; do not execute in this worker**.

This is the Gate 6 writer/automatic-placement D01 handoff. It is one mandatory
Playwright case, against the post-R51 current App source, using the existing
runner, harness, assertions, Runtime door, and UI assembly. It is not a new
protocol, DTO, selector, timeout, graph build, install, or duplicate actual.

## Exact source tuple

The source authority is the App integration branch after approved R51, not the
historical R39 source `c497b28c56d136a918e4e4489293a049009befa5` / tree
`17dac8608225e05e522888f29a6334585bee97aa`.

| repo / purpose | ref or keeper | commit (full 40) | tree (full 40) |
|---|---|---|---|
| App under test | `hub/timeline/app/tl/integration` (actual branch `tl/integration`) | `1490fbfe90f83c7c7c380d5cb16ccfcc0e9dcfcf` | `8e242d1497841f391b6152ecd8d204143fa03b52` |
| approved R51 admission fix | `hub/timeline/app/tl/app-m2-auto-all-entrypoints-admission-fix-r51` | `02ac224cd3c0d376f08b6129f58ded624f3e400d` | `aed5248fada10bdd2c74da4d3b3c2515671cc1ed` |
| current readiness fix | `da5d6d564af58ad06f126188c25e9a47f4e45be4` | `da5d6d564af58ad06f126188c25e9a47f4e45be4` | `1a3489722e87faa38d843a650fd668637363e934` |
| Agent/Astrid pin used by this actual | local keeper `agt-pin-6efc8150` | `6efc81500a0e0688c2bb41e736503f0fc3e04abb` | `2ed2b8a12b5b3391ca221ba6ff05390f71a73556` |
| Runtime pin used by this actual | local keeper `rt-pin-95bd3c5f` | `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c` | `d3a290b407fa61e6ab2d476f50c068073f70df00` |

At packet preparation, the local `tl/integration` worktree had the App tuple
above, while the locally cached hub integration ref still showed the older
`5ff11809e8100a6670acdb55eb19588ea168a80c`. Main must publish/resolve the
post-R51 App ref first and refuse if its commit or tree is not the tuple above.
That is a publication prerequisite, not permission to substitute c497.

The exact current requester/spec is unchanged and must be used:

- `tests/e2e/local/auto-real-proxy.spec.ts`, test
  `real operation proxy automatic image placement survives reconnect, lost ACK retry, reload and guarded undo`;
- `playwright.auto-real-proxy.config.ts` (`testMatch: auto-real-proxy.spec.ts`,
  one worker, no retries, `trace: retain-on-failure`);
- `scripts/testing/auto-real-proxy-main95.mjs`, current runner SHA-256
  `7ea0243ab6760d5fb06d17cf7e673f338549206090799c4946d532c3926d5d1f`;
- production requester path: `src/tools/video-editor/commands/placementRequester.ts`,
  `sessionPlacement.ts`, `editorImagePlacement.ts`, `commitSession.ts`, and
  `src/integrations/runtime/clientLocalAdapter.ts` / `operationHost.ts`.

Current source checks before the run must prove that `02ac224cd` and
`da5d6d564` are ancestors of the exact App commit. The readiness change is the
approved one-line state-identity republish at
`src/tools/video-editor/hooks/useTimelineCommandSession.ts:375`:
`changed({ ...session.getState() });`.

## One mandatory case; zero-failure result

Run exactly one test, once, with zero retries and zero second actuals. The
mandatory result is one collected and passing test with all of these existing
assertions passing:

1. The existing UI opens the seeded timeline, observes at least two native
   `/api/runtime/v1/events` responses, and exposes the existing Generate image
   control/readiness state.
2. The initial task admission is paused by the existing route probe until the
   outbox reservation is visible. The saved continuation has the exact owner,
   occurrence, `V2` lane, anchor, request body, idempotency key, head, and
   saved canonical document; the task host succeeds and returns the expected
   generated image object.
3. After Runtime and Vite restart, the original continuation and task locator
   survive reload; managed output is available; the first commit response is
   deliberately lost by the existing route, and the outbox enters retry.
4. After the second restart/reload, recovery sends the exact original commit
   method/body/key and receives the exact original receipt. The accepted
   publication is retained, and the existing guarded inverse undo removes the
   generated image.
5. The observed operation traffic includes task admission, task read, managed
   outputs, verified media selection, and `/commit`; `legacy` is exactly empty.

The zero-failure conditions are: Playwright exit 0, one passed/zero failed,
zero unexpected non-2xx responses in the retained failure list, zero page
errors/request failures/console errors that invalidate the case, zero legacy
writer POSTs, no source drift, and no duplicate actual. If any condition fails,
stop at that result; do not rerun or reinterpret the result as a pass.

## Main-owned keepers and prerequisites

Main must recreate or verify these durable paths before admission. None may be
created by `npm install`, a graph build, or the actual command. No old App
machine `/tmp` path is an authority.

```text
MAIN=/home/user/work/tl-auto-current-1490fbfe9
APP=$MAIN/source/app-1490fbfe9
AGENT=$MAIN/source/agent-6efc8150
RUNTIME=$MAIN/source/runtime-95bd3c5f
GRAPH=$MAIN/graph/public13
PRIVATE=$MAIN/private
EVIDENCE=$MAIN/evidence/automatic-current
NODE=$MAIN/node-v20.19.4-linux-x64/bin/node
```

Required keeper checks:

- `APP` is a clean, full-Git checkout at the exact App commit/tree above. Its
  `node_modules` entry is a symlink owned by this private checkout and points
  to `$GRAPH/node_modules`; do not replace `/home/user/work/app/node_modules`.
- `$GRAPH/node_modules` is a private, symlink-free public13 graph. It must
  contain `@banodoco/timeline-composition` version `0.0.13`, the exact App
  archive `vendor/artifacts/banodoco-timeline-composition-0.0.13.tgz` with
  SHA-256
  `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`, exactly
  77 safe regular archive members, and peers React/React-DOM `18.3.1`,
  Remotion/Player/Three `4.0.509`. Playwright and `@playwright/test` must both
  be `1.60.0`. This is the public13 graph identity; do not use the shared
  public10 graph.
- `AGENT` is clean at Agent `6efc8150` above and is run with
  `/home/user/work/venv-agent/bin/python`. `RUNTIME` is clean at Runtime
  `95bd` above and is run with `/home/user/work/venv-runtime/bin/python`.
  These venvs are read-only dependencies; `PYTHONPATH` is supplied by the
  existing harness so imports resolve from the pinned checkouts.
- Runtime `contract/artifacts.json` is the `astrid-runtime` manifest with 76
  artifacts, SHA-256
  `a902387c6a2315374f7e73511feea47da30191aba831b48820b3864b773a532d` and
  producer digest `sha256:54205b3ecb55038e416b31af936c9af26afa30dc1b05da16157ee4d861fe05ac`.
  App `runtime.lock.json` must retain source commit `95bd...` and that producer
  digest. Agent's Composition carrier is the existing public12 `0.0.12`
  artifact required by the runner; do not silently replace it with another
  carrier.
- `NODE` must be Node `v20.19.4`; the exact binary was absent from this
  machine, so this is an explicit main prerequisite. `/opt/node20` at
  `v20.20.0` is not an acceptable substitute. `PATH` must put `$MAIN`'s
  Node20.19.4 `bin` first.
- Chromium must be `/opt/pw-browsers/chromium-1194/chrome-linux/chrome`,
  version `141.0.7390.37`, SHA-256
  `85918a9937192b78da8edb51c38a7af4920ac6bd9ba19939ecb0bb724d5a1a95`, with
  `PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers`.
- `PRIVATE`, `$MAIN/home`, `$MAIN/run`, `$MAIN/cache`, and `$EVIDENCE` are
  physical mode-0700 directories. Use a short physical
  `TMPDIR=$MAIN/run/t` and verify the resolved temporary/profile/socket paths
  are under 100 characters before the run. Do not use or assume `/tmp/tl-a39`.
  The evidence directory must not be deleted after a failure.
- The fixed door port `17340` is free before admission. The existing harness
  allocates the Runtime, discovery-proxy, and Vite ports natively with port 0;
  do not hard-code replacement ports or add a readiness protocol.

## Pure preflight (before the one actual)

From the private App checkout, run the existing source-pinned startup-only
preflight. It performs identity, clean-tree, runtime-lock, 76-artifact, public
vendor, public13 archive, graph, browser, and vendor-lock checks without
starting a browser, task, Runtime, graph build, or actual. It must print
`mode: startup-only` and exit 0.

```bash
set -Eeuo pipefail
MAIN=/home/user/work/tl-auto-current-1490fbfe9
APP=$MAIN/source/app-1490fbfe9
AGENT=$MAIN/source/agent-6efc8150
RUNTIME=$MAIN/source/runtime-95bd3c5f
GRAPH=$MAIN/graph/public13
PRIVATE=$MAIN/private
EVIDENCE=$MAIN/evidence/automatic-current
NODE=$MAIN/node-v20.19.4-linux-x64/bin/node
mkdir -p "$PRIVATE" "$MAIN/home" "$MAIN/run/t" "$MAIN/cache/npm" "$MAIN/cache/pw" "$MAIN/cache/vite" "$MAIN/cache/xdg" "$EVIDENCE/preflight"
chmod 700 "$PRIVATE" "$MAIN/home" "$MAIN/run" "$MAIN/run/t" "$MAIN/cache" "$EVIDENCE" "$EVIDENCE/preflight"
cd "$APP"
env -i \
  HOME="$MAIN/home" LANG=C.UTF-8 PATH="$MAIN/node-v20.19.4-linux-x64/bin:/usr/bin:/bin" \
  ASTRID_CHECKOUT="$AGENT" ASTRID_RUNTIME_CHECKOUT="$RUNTIME" \
  ASTRID_PYTHON=/home/user/work/venv-agent/bin/python \
  ASTRID_RUNTIME_PYTHON=/home/user/work/venv-runtime/bin/python \
  PLAYWRIGHT_CHROMIUM_EXECUTABLE=/opt/pw-browsers/chromium-1194/chrome-linux/chrome \
  TIMELINE_AUTO_REAL_PROXY_RUN=1 TIMELINE_AUTO_REAL_PROXY_STARTUP_ONLY=1 \
  TIMELINE_AUTO_REAL_PROXY_APP_SHA=1490fbfe90f83c7c7c380d5cb16ccfcc0e9dcfcf \
  TIMELINE_AUTO_REAL_PROXY_APP_TREE=8e242d1497841f391b6152ecd8d204143fa03b52 \
  TIMELINE_AUTO_REAL_PROXY_AGENT_SHA=6efc81500a0e0688c2bb41e736503f0fc3e04abb \
  TIMELINE_AUTO_REAL_PROXY_AGENT_TREE=2ed2b8a12b5b3391ca221ba6ff05390f71a73556 \
  TIMELINE_AUTO_REAL_PROXY_RUNTIME_SHA=95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c \
  TIMELINE_AUTO_REAL_PROXY_RUNTIME_TREE=d3a290b407fa61e6ab2d476f50c068073f70df00 \
  TIMELINE_AUTO_REAL_PROXY_RUNTIME_PRODUCER_CHECKOUT="$RUNTIME" \
  TIMELINE_AUTO_REAL_PROXY_DEPENDENCY_ROOT="$GRAPH/node_modules" \
  TIMELINE_AUTO_REAL_PROXY_PRIVATE_ROOT="$PRIVATE" \
  TIMELINE_AUTO_REAL_PROXY_RECORD_DIR="$EVIDENCE/preflight" \
  TIMELINE_AUTO_REAL_PROXY_RUNNER_SHA256=sha256:7ea0243ab6760d5fb06d17cf7e673f338549206090799c4946d532c3926d5d1f \
  "$NODE" scripts/testing/auto-real-proxy-main95.mjs
! env | grep -E '^(NODE_OPTIONS|NODE_PATH|LD_[^=]*|PYTHONHOME)=' 
```

Also verify, without changing any shared dependency, that the private App
`node_modules` symlink resolves to the private public13 graph, the door is
free, the source tuple and `da5d6d564`/`02ac224cd` ancestry are exact, and
`npm exec -- playwright --version` reports Playwright 1.60.0 using the private
Node path. A failed preflight is a hard stop.

## One exact actual command

After the preflight passes, run this command exactly once from `APP`. The
config and test file are the existing files above; the command does not invoke
the historical runner or c497. The direct Playwright output directory is
durable so `auto-http-failures.json`, `trace.zip`, `error-context.md`, and the
console/page/request-failure context remain available after a failure.

```bash
cd /home/user/work/tl-auto-current-1490fbfe9/source/app-1490fbfe9
env -i \
  HOME=/home/user/work/tl-auto-current-1490fbfe9/home LANG=C.UTF-8 \
  PATH=/home/user/work/tl-auto-current-1490fbfe9/node-v20.19.4-linux-x64/bin:/usr/bin:/bin \
  ASTRID_CHECKOUT=/home/user/work/tl-auto-current-1490fbfe9/source/agent-6efc8150 \
  ASTRID_RUNTIME_CHECKOUT=/home/user/work/tl-auto-current-1490fbfe9/source/runtime-95bd3c5f \
  ASTRID_PYTHON=/home/user/work/venv-agent/bin/python \
  ASTRID_RUNTIME_PYTHON=/home/user/work/venv-runtime/bin/python \
  PLAYWRIGHT_CHROMIUM_EXECUTABLE=/opt/pw-browsers/chromium-1194/chrome-linux/chrome \
  PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers \
  ASTRID_APP_DIRECT_DOOR_PORT=17340 \
  TMPDIR=/home/user/work/tl-auto-current-1490fbfe9/run/t \
  npm_config_cache=/home/user/work/tl-auto-current-1490fbfe9/cache/npm \
  npm_config_offline=true \
  PWTEST_CACHE_DIR=/home/user/work/tl-auto-current-1490fbfe9/cache/pw \
  VITE_CACHE_DIR=/home/user/work/tl-auto-current-1490fbfe9/cache/vite \
  XDG_CACHE_HOME=/home/user/work/tl-auto-current-1490fbfe9/cache/xdg \
  PLAYWRIGHT_OUTPUT_DIR=/home/user/work/tl-auto-current-1490fbfe9/evidence/automatic-current \
  npm exec -- playwright test \
    --config playwright.auto-real-proxy.config.ts \
    tests/e2e/local/auto-real-proxy.spec.ts \
  > /home/user/work/tl-auto-current-1490fbfe9/evidence/automatic-current/playwright.log 2>&1
```

`env -i` intentionally leaves `NODE_OPTIONS`, `NODE_PATH`, every `LD_*`, and
`PYTHONHOME` unset for the pack-host and all harness children. Do not add a
launcher, retry loop, `--grep`, selector override, timeout override, cache
under shared `node_modules`, or cleanup command.

## Native readiness and retained failure evidence

The proof's readiness is the existing native assembly, not a new probe:

- `DirectHarness` checks the fixed door, starts the actual Runtime with a
  random native port, writes discovery/catalog/credential files in its own
  physical harness temp, and `publishProxyProfile` verifies the selected
  Astrid realm/root and `source_profile`.
- `startViteWorkspace` allocates the discovery-proxy and Vite ports natively,
  waits for `/runtime-config/v1/workspace.json` and the Vite origin, and
  assembles the existing public13 Composition archive. The page then proves
  readiness through `data-state=connected` or the existing `Generate image`
  control and observes the native event stream.
- The existing `runImageHost(..., 'register', ...)` assembles and registers
  `generation.generate_image`. The existing paused `/runtime-config/v1/operation/runtime/v1/tasks`
  route proves the command-session placement continuation is observable before
  task transmission. No fabricated port, task locator, or protocol field is
  allowed.

On any failure, preserve the whole
`/home/user/work/tl-auto-current-1490fbfe9/evidence/automatic-current` tree.
Read `auto-http-failures.json` in array order and report the first retained
non-2xx as its sanitized method, pathname, status, and optional `code`, `type`,
and `location`. The existing spec retains only relevant `/api/runtime` and
`/runtime-config/v1/operation` responses; discovery/Vite startup failures must
be reported from `playwright.log` and the retained `error-context.md` rather
than inferred from a generic console line. Keep the Playwright `trace.zip`,
`error-context.md`, console/page/requestfailed context, and `playwright.log`
together. Do not infer a Runtime or proxy cause from status 503 alone.

After the command, verify the App/Agent/Runtime commit and tree, clean status,
runner hash, graph/archive hashes, and evidence paths are unchanged. Report
the exact first non-2xx route if present; a successful run must have an empty
retained HTTP-failure list and no legacy POSTs. This is the only automatic
actual for this packet.


## HOME dispatch hold — 2026-10-21 10:40 UTC
Source1490 is qualified for this new proof boundary. Command-only custody review app-m2-auto-main-command-custody-review-r55 is checking effective direct argv/environment and executable list1. Do not consume the one actual before its verdict and any literal correction. No source gate is added and no old browser proof is requested. HOME will mark this hold cleared explicitly.
