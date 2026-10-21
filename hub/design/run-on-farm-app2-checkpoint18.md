# App2 18Z real journeys — farm handoff

Status: **HOLD**. This is one farm handoff for the existing parent-viewport,
producer-current, and selected-seed App2 journeys. It does not authorize a
local run. The farm prepares a clean source snapshot and existing dependency
paths, then uses the existing runners. No bespoke launcher, runner copy,
keeper, install, graph extraction, or hash/receipt ceremony is part of this
packet.

## Current source tuple

Use these exact `tl/integration` hub refs for the farm snapshot. These are
source identities, not a claim that any of the three old journey packets has
already been rebound to them.

| repo | hub ref | commit | tree |
| --- | --- | --- | --- |
| App | `timeline/app/tl/integration` (`hub/timeline/app/tl/integration`) | `c85da5427944d26242c71e503516d8d203a5f7a7` | `8666399f23cd10adde62e36b3429aea4bf7375de` |
| Agent | `timeline/agent/tl/integration` (`hub/timeline/agent/tl/integration`) | `c9ac7c7b0e862ad32a919db33859c5fcbf58ad99` | `cab0a2aa34ba6dae880657eb484979039e206049` |
| Runtime | `timeline/runtime/tl/integration` (`hub/timeline/runtime/tl/integration`) | `cc7410a1fa9bd5acc703abfd1b8fde0cf3d00365` | `1c8473c9e73fde02f9943b975eac171ac2757069` |
| Composition | `timeline/composition/tl/integration` (`hub/timeline/composition/tl/integration`) | `6c4d9342189b69d488b41f609b64aa2918eda955` | `f529869d1438b1704e14aaba68278a16be360bac` |

The existing Runtime producer consumed by the retained App runners is the
published immutable Runtime `0.2.14`, commit
`95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`, tree
`d3a290b407fa61e6ab2d476f50c068073f70df00`. The farm must use the existing
protected graph selected for that runner, not the shared App install. Its
Composition declaration must be checked from the graph actually resolved by
the runner; a shared `0.0.8` or `0.0.10` declaration is **INVALID**.

## Existing environment and paths

The farm supplies `APP_ROOT` as a clean captured snapshot of the App tuple
above; it must not be `/home/user/work/app` and must report the exact commit
and tree before invoking a runner. Use the already-protected graph and
read-only environments:

```text
NODE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node
AGENT_PYTHON=/home/user/work/venv-agent/bin/python
RUNTIME_PYTHON=/home/user/work/venv-runtime/bin/python
GRAPH_ROOT=/home/user/work/app-m3-private13-normal-lock-install-units-r6-owned
GRAPH=$GRAPH_ROOT/node_modules
GRAPH_READY=$GRAPH_ROOT/READY
GRAPH_LEASE=$GRAPH_ROOT/LEASE
CHROMIUM=/opt/pw-browsers/chromium-1194/chrome-linux/chrome
BROWSER_LOCK=/home/user/work/.app-m1-browser.lock
APP_TSC_LOCK=/home/user/work/.app-tsc.lock
```

Before READY, verify the clean `APP_ROOT`, exact current tuple, executable
Node/Agent/Runtime paths, existing graph READY/LEASE, physical graph path,
Chromium, private short `TMPDIR`/`XDG_RUNTIME_DIR`, and free space. Resolve
the Composition declaration from `GRAPH`, and require its package version and
files to come from that graph. Do not accept resolution through
`/home/user/work/app/node_modules`, or a declaration that says `0.0.8`/`0.0.10`.
No graph copy or dependency edit is allowed.

The required project checks are the real App checks, serialized as follows;
report every remaining diagnostic and its owning dependency:

```sh
flock -w 600 /home/user/work/.app-tsc.lock \
  node_modules/.bin/tsc -p tsconfig.app.json --noEmit
node_modules/.bin/eslint --no-cache --no-warn-ignored --max-warnings 0 \
  tests/e2e/local/three-products.spec.ts \
  tests/e2e/local/three-products.selected-param-dev.spec.ts \
  tests/e2e/local/producer-ownership-current-pin.spec.ts \
  tests/e2e/local/support/producer-ownership-current-pin.ts
```

An empty-root check is not a green result. These are targeted source checks;
the worker does not run the browser journeys, a full suite, a build, an
install, or a new launcher.

## Existing journey selectors

Preserve every original assertion in the existing specs. Use only the
existing runner and its selector; do not rewrite a spec to fit the current
tuple.

| journey | existing selector | required body |
| --- | --- | --- |
| Parent viewport/manual drop | `tests/e2e/local/three-products.spec.ts:1410` — `M2 real mounted manual video drop: Runtime selection refusal is closed, native ADD recovers exactly, and undo preserves opaque data` | strict selection refusal, native `clip.add-media`, lost-ACK retry, restart/recovery, undo, opaque/order/source/epoch/ACK/hold, and zero-legacy assertions |
| Producer current | `tests/e2e/local/producer-ownership-current-pin.spec.ts` — `removes only stale owned transcript output and moves only owned scene output` | existing-output ownership/refusal, protected raw rows/order, reload, real lost-ACK retry, and guarded undo; no fresh-creation claim |
| Selected seed | `tests/e2e/local/three-products.selected-param-dev.spec.ts` — `local DEV selected PARAM uses admitted P1 through P2 removal, refusal, retry, reload and undo` | original P1/P2, refusal, exact retry/body/key, reload/recovery, undo, and zero-legacy assertions |

The existing runner identities are not currently closed for the current App
tuple. The old parent runner is bound to App
`6707a30f14bf3a5ee19cb9e481b7dbd95b77522a` / tree
`6ff32d797f0e774b8574274a3494ce8755fa160c`; the old selected runner to App
`0cc2583aaf07e89190b9344b5ac82849d6279586` / tree
`320e74a93676c781e83885b86ec237b4a1465d80`; and the old producer handoff to
App `5863411a8c2400db719b5385002b05af0a2b3891` / tree
`31b0f77c6ef4e9fdbeff3e4f88cc4705f0891e89`. Those tuples are historical
packet identities only. Until the farm proves an existing runner accepts the
current App commit/tree and the matching Agent/Runtime/Composition paths,
the result is HOLD; do not claim current-source evidence from an old tuple.

## Existing `env -i` invocation

After the farm has resolved the existing runner's own current-source binding,
invoke it directly from the captured `APP_ROOT` with the existing sanitized
environment. The farm may substitute only its prepared absolute `APP_ROOT`,
run root, evidence root, graph archive path, and the existing runner path:

```sh
cd "$APP_ROOT"
env -i \
  HOME="$RUN_ROOT/home" \
  LANG=C.UTF-8 \
  PATH=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin:/usr/local/bin:/usr/bin:/bin \
  NODE="$NODE" \
  TMPDIR="$RUN_ROOT/tmp" \
  XDG_RUNTIME_DIR="$RUN_ROOT/xdg" \
  NORMAL014_PROFILE=final95 \
  NORMAL014_APP_SOURCE=parent \
  NORMAL014_USE_BASE_PYTHON=1 \
  NORMAL014_PYTHON_BASE="$AGENT_PYTHON" \
  NORMAL014_LOCKED_GRAPH="$GRAPH_ROOT" \
  NORMAL014_LOCKED_GRAPH_ARCHIVE="$GRAPH_ARCHIVE" \
  APP_ROOT="$APP_ROOT" \
  NORMAL014_RECORD_ROOT="$EVIDENCE_ROOT" \
  NORMAL014_RUN_ROOT_PARENT="$RUN_ROOT" \
  ASTRID_PYTHON="$AGENT_PYTHON" \
  ASTRID_RUNTIME_PYTHON="$RUNTIME_PYTHON" \
  PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers \
  PLAYWRIGHT_CHROMIUM_EXECUTABLE="$CHROMIUM" \
  sh "$EXISTING_RUNNER" run
```

For selected and producer, retain their existing mode/runner entrypoint and
selector bindings; do not wrap either invocation in another shell launcher.
The farm scheduler may serialize jobs, but must not add an outer
`flock -n /home/user/work/.app-m1-browser.lock`.

## Single-layer browser-lock prerequisite

Parent590's cause was double browser-lock acquisition, not product behavior:
the old farm command held `flock -n /home/user/work/.app-m1-browser.lock`
around a runner whose existing App driver already takes
`flock -w 600 /home/user/work/.app-m1-browser.lock` immediately around
Playwright. The outer owner waited for the child; the child waited for the
outer owner, so Playwright never launched. The inner runner lock is the sole
browser-stage owner. This is a prerequisite for every three journeys.

The 1209 parent/selected lock correction and the 1216 producer reverse-
translation diagnosis are retained setup evidence, not journey results. A
producer fixture translation failure before dispatch is not producer behavior.

## Superseded packets and HOLD boundary

This handoff supersedes the old execution-routing packets, without deleting
their evidence:

- `ORCH/design/run-on-main-app2-parent-viewport.md`
- `ORCH/design/run-on-main-app2-producer-current.md`
- `ORCH/design/run-on-main-app2-selected-seed.md`

Keep those files and their retained reports/packets, including the Parent590
first-failure report, `ap2-m2-parent-selected-single-lock-source-1209-REPORT.md`,
and `ap2-m2-producer-after-reverse-first-byte-diagnosis-1216-REPORT.md`.
They are historical evidence and must not be relabelled as current-source
passes. This packet stays **HOLD** until the farm has an exact current-source
binding for each existing runner, has passed the project tsc/lint checks and
independent review, and can invoke the runner with single-layer lock
ownership. No browser/full result is claimed here.
