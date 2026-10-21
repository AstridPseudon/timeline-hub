# Run on main: App public Trim, corrected current source

Status: **HOLD — source approved; actual/browser not authorized here.**

This packet composes one original public Trim case on the current App source.
It does not run a browser, build, install, full suite, or new graph. The r41
independent review is recorded below as source-safety approval only. The
existing fixture has no browser-visible observer for the specific mounted
`ops.clipTrim` value: `public-trim-trigger` is enabled from resolved clip data,
and the existing outbox wait proves only an idle owner. The real assembly is
source-traceable, but its mounted trim-port existence is not independently
observable before the click without a test hook or fabricated Provider. Keep
the actual HELD until main supplies an existing native observer or equivalent
current real assembly evidence.

## Exact source and ancestry

The corrected product source is the r40/r41 source, which descends from the
current App integration branch. The exact r40 source ref is retained in the
packet so main cannot substitute the historical `49eb` ancestry:

| input | exact identity |
| --- | --- |
| App integration ancestor | `hub/timeline/app/tl/integration` / `tl/integration`, commit `1490fbfe90f83c7c7c380d5cb16ccfcc0e9dcfcf`, tree `8e242d1497841f391b6152ecd8d204143fa03b52` |
| corrected App source | `hub/timeline/app/tl/app-m2-public-trim-native-or-refuse-r40` (same commit as r41), `eb51ff381660a90e847c70371fcb64b8eca4d113`, tree `525ce6d726ab36d743e4504fa2e1b274bfa21b41` |
| r41 review | `hub/timeline/app/tl/app-m2-public-trim-native-or-refuse-review-r41`, same `eb51ff381660a90e847c70371fcb64b8eca4d113` / `525ce6d726ab36d743e4504fa2e1b274bfa21b41` |
| final packet branch | `hub/timeline/app/tl/app-m2-public-trim-reviewed-main-packet-r42`, published by the worker harness after its commit; main must resolve and record its full final SHA/tree before setup |

Main must verify the final packet branch is a descendant of `1490fbfe9`, and
that its product-source parent is exactly `eb51ff381`. No old `49eb` whole-tree
swap is permitted.

## Test-only material restored

The following are exact blobs from `49eb3f61a0043e1796a63181574e9b492d02bb7a`;
they are test/config support only and preserve current product code, ports,
and r40 source. The original proof body is unchanged.

| path | blob |
| --- | --- |
| `playwright.public-trim.config.ts` | `8fdac5af68ba9ef552642b968b0ef78a91ad8977` |
| `tests/e2e/local/public-trim-mounted-fixture.spec.ts` | `a3ae6394dabf1a51ff0ec893c09358936c9fb954` |
| `tests/e2e/fixtures/public-trim/FixtureControls.tsx` | `218db78a225d9bbbfaa0ec8c69fafa23d74b26f3` |
| `tests/e2e/fixtures/public-trim/index.html` | `36ec08b001ad020e7bea57adb5721f29743ecbfa` |
| `tests/e2e/fixtures/public-trim/main.tsx` | `d59232a27581a31d3cddc1a3917915c80abca15e` |
| `tests/e2e/local/support/public-trim-preflight.ts` | `1b0bf344405a0a037c498116ef033fa027d16663` |
| `tests/e2e/local/support/public-trim-preflight.test.ts` | exact original preflight test blob |

The required fixture/support files are included because the r40 current
descendant had removed them; copying only the spec/config would collect zero
tests with an import error. No assertion, selector, timeout, retry, raw-body,
reload, undo, credential, or zero-legacy line was changed.

## Independent review and current source change

r41 report: `APPROVE — source-level data safety`, reviewing
`eb51ff381660a90e847c70371fcb64b8eca4d113` against current integration
`435e76eb3f2dcaa0324ed69d4c019ab9c32bfbef`. It confirms that supported
source-only media trims route through `ops.clipTrim`; missing, stale, throwing,
or refusing ports return `ok:false` without snapshot fallback/local mutation;
placement-plus-trim retains its legacy path; and the real production carrier is
`useTimelineState → save.commands.clipTrimPort → editorOps → TimelineStore.ops.clipTrim`.
It reports 109 focused semantic/native/session passes, 17 mounted-state/Provider
passes, 79 command-session durability passes, and `git diff --check` pass. It
did not claim browser qualification.

r37 evidence remains terminal and must not be replayed: one original actual,
zero tests passed, first visible boundary at
`public-trim-mounted-fixture.spec.ts:143`, `posts[0]` undefined after the
unchanged trigger click, no post-click commit POST. The retained trace/log and
error context are the evidence for that boundary. r38 identified the missing
mounted native trim-port readiness carrier; r40 made the public facade fail
closed on missing/refusing native acceptance.

## Exact current pins for main

Main must use the existing qualified pins and refuse any mismatch:

- Agent/Astrid: `6efc81500a0e0688c2bb41e736503f0fc3e04abb`, tree
  `2ed2b8a12b5b3391ca221ba6ff05390f71a73556`.
- Runtime/public14: `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`, tree
  `d3a290b407fa61e6ab2d476f50c068073f70df00`; `contract/artifacts.json` has
  exactly 76 artifacts and producer version
  `sha256:54205b3ecb55038e416b31af936c9af26afa30dc1b05da16157ee4d861fe05ac`.
- Composition/C13: package `0.0.13`, archive SHA-256
  `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`,
  exactly 77 regular archive members; no public10/public12 substitution.
- Existing vendor source identity required by the original preflight:
  `091aa23ec83ea05ffd3b0115a640230d51c8c429`, tree
  `e3ae90fe482ba6cad6c3f94069127faf76ebceb6`.

The App checkout, Agent checkout, Runtime checkout, and private dependency
graph must be clean and physically private to the main run. Shared
`/home/user/work/app/node_modules`, shared venvs, and shared caches are
read-only and must not be used as write targets.

## Main-owned prerequisites

Use a short physical mode-0700 root, for example:

```text
MAIN=/home/user/work/tl-app-public-trim-current-r42
APP=$MAIN/source/app-current
AGENT=$MAIN/source/agent-6efc8150
RUNTIME=$MAIN/source/runtime-95bd3c5f
GRAPH=$MAIN/graph/c13
PRIVATE=$MAIN/private
EVIDENCE=$MAIN/evidence/public-trim-current
NODE=$MAIN/node-v20.19.4-linux-x64/bin/node
```

Main must materialize or verify, without installation/build during this task:

- `NODE` is exactly Node `v20.19.4`; the present worker machine only exposes
  `/opt/node20` `v20.20.0`, so that is not an acceptable substitute.
- Chromium is `/opt/pw-browsers/chromium-1194/chrome-linux/chrome`, version
  `141.0.7390.37`, SHA-256
  `85918a9937192b78da8edb51c38a7af4920ac6bd9ba19939ecb0bb724d5a1a95`, with
  `PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers`.
- `$GRAPH/node_modules` is the existing private, symlink-free C13 graph with
  the archive/hash and 77-member checks above. Do not extract/install/copy
  into a path resolving to shared node_modules.
- `$PRIVATE`, `$MAIN/run`, `$MAIN/run/t`, `$MAIN/home`, `$MAIN/cache`, and
  `$EVIDENCE` are physical mode-0700 directories. Resolve the profile,
  socket, and temporary paths and require each to be shorter than 100
  characters. Preserve `$EVIDENCE` after any failure.
- The existing direct door port `17340` is free; Runtime, discovery-proxy,
  and Vite ports are allocated by the existing harness with native port 0.
  Do not hard-code replacements or add a readiness protocol.
- The existing credential file, realm, actor, project scope, and Origin
  guards are present and must remain exact. Keep `NODE_OPTIONS`, `NODE_PATH`,
  every `LD_*`, and `PYTHONHOME` unset in the pack-host environment.

## Pure preflight evidence in this worker

Using private cache directories only:

```bash
env -i HOME=/tmp/tl-app-m2-public-trim-r42-preflight/home LANG=C.UTF-8 \
  PATH=/opt/node20/bin:/usr/bin:/bin \
  npm_config_cache=/tmp/tl-app-m2-public-trim-r42-preflight/npm-cache \
  npm_config_offline=true \
  VITE_CACHE_DIR=/tmp/tl-app-m2-public-trim-r42-preflight/vite-cache \
  XDG_CACHE_HOME=/tmp/tl-app-m2-public-trim-r42-preflight/xdg-cache \
  npm exec -- playwright test \
    --config playwright.public-trim.config.ts \
    --list
```

Result: **PASS — exactly 1 test in 1 file, zero failures.** This used local
Node `v20.20.0` only because Node 20.19.4 is unavailable here; main must use
20.19.4. The first list attempt before restoring the required original
test-only dependencies failed with the retained import error and zero tests;
it was corrected by restoring those exact original blobs, not by changing the
proof.

Pure preflight test:

```bash
env -i HOME=/tmp/tl-app-m2-public-trim-r42-preflight/home LANG=C.UTF-8 \
  PATH=/opt/node20/bin:/usr/bin:/bin \
  npm_config_cache=/tmp/tl-app-m2-public-trim-r42-preflight/npm-cache \
  npm_config_offline=true \
  /opt/node20/bin/node --import ./node_modules/tsx/dist/esm/index.mjs \
  --test tests/e2e/local/support/public-trim-preflight.test.ts
```

Result: **PASS**, exit 0. The initial `npm exec -- tsx --test` attempt was not
used as evidence because shared-environment tsx IPC attempted a forbidden
socket; the direct Node/tsx-loader command passed without changing source or
shared dependencies.

## Held exact main command

After the missing native readiness observer is resolved and all prerequisites
above pass, main may execute exactly once from the final packet-branch App
checkout. The command is direct `npm exec -- playwright`; it intentionally
does not use the historical broken npm-script argv wrapper:

```bash
cd "$APP"
env -i \
  HOME="$MAIN/home" LANG=C.UTF-8 \
  PATH="$MAIN/node-v20.19.4-linux-x64/bin:/usr/bin:/bin" \
  ASTRID_CHECKOUT="$AGENT" \
  ASTRID_RUNTIME_CHECKOUT="$RUNTIME" \
  ASTRID_PYTHON=/home/user/work/venv-agent/bin/python \
  ASTRID_RUNTIME_PYTHON=/home/user/work/venv-runtime/bin/python \
  TIMELINE_BUNDLE_AGENT_HEAD=6efc81500a0e0688c2bb41e736503f0fc3e04abb \
  TIMELINE_BUNDLE_RUNTIME_HEAD=95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c \
  PRIVATE13_NODE_MODULES="$GRAPH/node_modules" \
  VITE_TIMELINE_COMPOSITION_ROOT="$GRAPH/node_modules/@banodoco/timeline-composition" \
  PLAYWRIGHT_CHROMIUM_EXECUTABLE=/opt/pw-browsers/chromium-1194/chrome-linux/chrome \
  PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers \
  ASTRID_APP_DIRECT_DOOR_PORT=17340 \
  TMPDIR="$MAIN/run/t" \
  PWTEST_CACHE_DIR="$MAIN/cache/pw" \
  VITE_CACHE_DIR="$MAIN/cache/vite" \
  XDG_CACHE_HOME="$MAIN/cache/xdg" \
  npm_config_cache="$MAIN/cache/npm" \
  npm_config_offline=true \
  PLAYWRIGHT_OUTPUT_DIR="$EVIDENCE/browser-artifacts" \
  npm exec -- playwright test \
    --config playwright.public-trim.config.ts \
    tests/e2e/local/public-trim-mounted-fixture.spec.ts \
  > "$EVIDENCE/playwright.log" 2>&1
```

The command must collect exactly one test, pass with zero failures, and retain
the original success/source-window/reload/undo/retry/raw-body/idempotency,
credential, and `legacy=[]` assertions unchanged. It must also prove native
trim acceptance through the current real mounted assembly/fixture; no test
hook or fabricated Provider may satisfy that prerequisite.

On any failure, stop once, preserve the entire evidence directory, and report:
the first non-2xx method/path/status plus `code`/`type`/`location` when
available, the first page/console/request-failed/error-context boundary, the
Playwright trace, raw request/response context, and the executed/failed test
count. Do not retry, change selectors/timeouts/assertions, or infer a Runtime
cause from a generic 503. No actual was run for this packet.
