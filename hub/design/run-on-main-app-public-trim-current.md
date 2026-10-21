# Run on main: App public Trim, corrected current source

Status: **READY FOR MAIN EXECUTION — source and existing-fixture readiness resolved; actual/browser not authorized here.**

This packet composes one original public Trim case on the current App source.
It does not run a browser, build, install, full suite, or new graph. The r41
independent review is recorded below as source-safety approval only. r43 now
observes the existing mounted `ops.clipTrim` value through
`useTimelineEditorOps()` and requires its native `capture`, `finish`, and
`submit` methods before the unchanged `public-trim-trigger` click. This is an
existing fixture/store observation, not a product hook or fabricated Provider;
the main run is held only for the concrete prerequisites below and its one
authorized actual.

## Exact source and ancestry

The corrected product source is the r40/r41 source, carried into the concrete
r43 fixture packet and then merged into the current App integration branch.
The exact r40 source ref is retained so main cannot substitute the historical
`49eb` ancestry. Use the integrated commit below when available; otherwise use
the exact committed r43 descendant, never a symbolic unpublished placeholder:

| input | exact identity |
| --- | --- |
| App integration ancestor | `hub/timeline/app/tl/integration` / `tl/integration`, commit `1490fbfe90f83c7c7c380d5cb16ccfcc0e9dcfcf`, tree `8e242d1497841f391b6152ecd8d204143fa03b52` |
| exact r40 product source | `hub/timeline/app/tl/app-m2-public-trim-native-or-refuse-r40`, commit `eb51ff381660a90e847c70371fcb64b8eca4d113`, tree `525ce6d726ab36d743e4504fa2e1b274bfa21b41` |
| r41 review | `hub/timeline/app/tl/app-m2-public-trim-native-or-refuse-review-r41`, same `eb51ff381660a90e847c70371fcb64b8eca4d113` / `525ce6d726ab36d743e4504fa2e1b274bfa21b41` |
| final integrated source | `tl/integration`, merge `0cc2583aaf07e89190b9344b5ac82849d6279586`, tree `320e74a93676c781e83885b86ec237b4a1465d80` |
| exact committed r43 fallback | `tl/app-m2-trim-existing-fixture-port-readiness-r43`, commit `76d1397d80b4f409c1062814b09d452e881d1748`, tree `9ac48c4d7a5152be3469781178fb9987ca95909f` |

Main must verify the selected final source is a descendant of `1490fbfe9`, that
`eb51ff381660a90e847c70371fcb64b8eca4d113` is reachable from the supplied r40
hub branch, and that the selected integrated/fallback tree is the one recorded
above. No old `49eb` whole-tree swap is permitted.

## Test-only material restored

The fixture/support files are test/config support only and preserve current
product code, ports, and r40 source. The final integrated r43 blobs are:

| path | blob |
| --- | --- |
| `playwright.public-trim.config.ts` | `8fdac5af68ba9ef552642b968b0ef78a91ad8977` |
| `tests/e2e/local/public-trim-mounted-fixture.spec.ts` | `9bc6e68e7000f4f543ad6be7b179a344b767978e` |
| `tests/e2e/fixtures/public-trim/FixtureControls.tsx` | `b498e2b45c0ae87880e5cbcb1019b5d37124c214` |
| `tests/e2e/fixtures/public-trim/index.html` | `36ec08b001ad020e7bea57adb5721f29743ecbfa` |
| `tests/e2e/fixtures/public-trim/main.tsx` | `d59232a27581a31d3cddc1a3917915c80abca15e` |
| `tests/e2e/local/support/public-trim-preflight.ts` | `1b0bf344405a0a037c498116ef033fa027d16663` |
| `tests/e2e/local/support/public-trim-preflight.test.ts` | `408a2c9758eb0672d75f40c5f63095b2901cdf5b` |

The required fixture/support files are included because the r40 current
descendant had removed them; copying only the spec/config would collect zero
tests with an import error. r43 changes only the existing fixture observation
and its pre-action readiness assertion. The original positive/source-window,
raw-body, retry/idempotency, reload, undo, credential, and `legacy=[]`
assertions remain unchanged.

Exact packet changes are therefore: r40 product changes in
`src/tools/video-editor/commands/semanticGestures.test.ts` and
`src/tools/video-editor/hooks/useTimelineCommandsService.ts`; r43 test/config
support in the seven paths listed above, with `FixtureControls.tsx` observing
`useTimelineEditorOps().clipTrim` and the spec asserting native readiness before
the original action.

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

r43 resolves the former readiness-observer hold using the existing mounted
fixture closure: `main.tsx` mounts the real `BrowserVideoEditor`,
`RuntimeDataProvider`, `PUBLIC_TIMELINE_SERVICE_HOOKS`, and scoped host
services; `FixtureControls.tsx` reads `useTimelineEditorOps()` from the real
store; and `openFixture()` requires
`{ nativeClipTrimPortReady: true }` before the unchanged trigger click. The
reported source-only checks were Playwright list (one test), preflight (one
pass), ESLint, and `git diff --check`; no browser/actual/full/build/install/new
graph run was claimed.

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

Use a short physical mode-0700 root, for example. The exact Agent/Runtime
paths below are required by the existing `public-trim-preflight.ts` guard;
do not replace them with unverified copies while claiming the same proof:

```text
MAIN=/home/user/work/tl-app-public-trim-current-r43
APP=$MAIN/source/app-current
AGENT=/home/user/work/wt/agt-pin-6efc8150
RUNTIME=/home/user/work/wt/rt-pin-95bd3c5f
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
  `TMPDIR`, `XDG_RUNTIME_DIR`, `XDG_CACHE_HOME`, Playwright/Vite/npm cache,
  and every runner socket path; require each resolved path to be shorter than
  100 characters. Preserve `$EVIDENCE` after any failure.
- The existing direct door port `17340` is free; Runtime, discovery-proxy,
  and Vite ports are allocated by the existing harness with native port 0.
  Do not hard-code replacements or add a readiness protocol.
- The existing credential file, realm, actor, project scope, and Origin
  guards are present and must remain exact. Keep `NODE_OPTIONS`, `NODE_PATH`,
  every `LD_*`, and `PYTHONHOME` unset in the pack-host environment.

The existing runner guards are part of the proof: `verifyPublicTrimSourceTuple`
must remain active, including clean exact Agent/Runtime pins, vendor provenance,
`runtime.lock.json`, the 76-artifact Runtime manifest, the C13 archive/hash and
77 regular-member check, private `PYTHONPATH` resolution, and the existing
credential/realm/actor/project/Origin checks. Main may use its own isolated
verified dependency graph, but shared node_modules, venvs, and caches remain
read-only; no guard may be bypassed.

Pure environment/path validation, before either Playwright command (no browser,
build, install, graph generation, or actual):

```bash
env -i \
  PATH=/usr/bin:/bin \
  MAIN="$MAIN" NODE="$NODE" CHROME=/opt/pw-browsers/chromium-1194/chrome-linux/chrome \
  PRIVATE="$PRIVATE" EVIDENCE="$EVIDENCE" GRAPH="$GRAPH" \
  /bin/bash -eu -c '
    test "$("$NODE" --version)" = v20.19.4
    test -x "$CHROME"
    test "$(sha256sum "$CHROME" | awk "{print \$1}")" = 85918a9937192b78da8edb51c38a7af4920ac6bd9ba19939ecb0bb724d5a1a95
    for path in "$MAIN" "$PRIVATE" "$MAIN/run" "$MAIN/run/t" "$MAIN/home" "$MAIN/cache" "$MAIN/cache/pw" "$MAIN/cache/vite" "$MAIN/cache/xdg" "$MAIN/cache/npm" "$EVIDENCE"; do
      test -d "$path"
      test ! -L "$path"
      test "$(realpath "$path")" = "$path"
      test "$(stat -c %a "$path")" = 700
      test "${#path}" -lt 100
    done
    test -d "$GRAPH/node_modules"
    test -z "$(find "$GRAPH/node_modules" -type l -print -quit)"
    while IFS= read -r -d "" socket; do
      resolved=$(realpath "$socket")
      test "${#resolved}" -lt 100
    done < <(find "$MAIN/run" -type s -print0)
  '
```

The existing harness must keep all allocated socket paths under `$MAIN/run`;
the final `find` check is repeated after allocation and after teardown.

## Pure preflight evidence in this worker

Using private cache directories only:

```bash
env -i HOME=/tmp/tl-app-m2-trim-existing-fixture-port-readiness-r43/home LANG=C.UTF-8 \
  PATH=/opt/node20/bin:/usr/bin:/bin \
  npm_config_cache=/tmp/tl-app-m2-trim-existing-fixture-port-readiness-r43/npm-cache \
  npm_config_offline=true \
  VITE_CACHE_DIR=/tmp/tl-app-m2-trim-existing-fixture-port-readiness-r43/vite-cache \
  XDG_CACHE_HOME=/tmp/tl-app-m2-trim-existing-fixture-port-readiness-r43/xdg-cache \
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
env -i HOME=/tmp/tl-app-m2-trim-existing-fixture-port-readiness-r43/home LANG=C.UTF-8 \
  PATH=/opt/node20/bin:/usr/bin:/bin \
  npm_config_cache=/tmp/tl-app-m2-trim-existing-fixture-port-readiness-r43/npm-cache \
  npm_config_offline=true \
  VITE_CACHE_DIR=/tmp/tl-app-m2-trim-existing-fixture-port-readiness-r43/vite-cache \
  XDG_CACHE_HOME=/tmp/tl-app-m2-trim-existing-fixture-port-readiness-r43/xdg-cache \
  /opt/node20/bin/node --import ./node_modules/tsx/dist/esm/index.mjs \
  --test tests/e2e/local/support/public-trim-preflight.test.ts
```

Result: **PASS**, exit 0. The initial `npm exec -- tsx --test` attempt was not
used as evidence because shared-environment tsx IPC attempted a forbidden
socket; the direct Node/tsx-loader command passed without changing source or
shared dependencies.

## Exact main commands

After all prerequisites above pass, main must run the mandatory direct list
check, then execute the actual exactly once from the selected concrete
integrated/fallback App checkout. Both commands are direct `npm exec --
playwright`; they intentionally do not use the historical broken npm-script
argv wrapper. The list check must report exactly one test in one file and zero
failures before the actual is authorized:

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
  XDG_RUNTIME_DIR="$MAIN/run" \
  PWTEST_CACHE_DIR="$MAIN/cache/pw" \
  VITE_CACHE_DIR="$MAIN/cache/vite" \
  XDG_CACHE_HOME="$MAIN/cache/xdg" \
  npm_config_cache="$MAIN/cache/npm" \
  npm_config_offline=true \
  npm exec -- playwright test \
    --config playwright.public-trim.config.ts \
    --list
```

Required list result: exactly 1 test in 1 file, zero failures. The actual
command is:

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
  XDG_RUNTIME_DIR="$MAIN/run" \
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

## Source/graph postflight

After the one actual, record and verify without changing the evidence tree. For
the integrated source, the following must pass:

```bash
R40_SHA=eb51ff381660a90e847c70371fcb64b8eca4d113
R40_HUB_BRANCH=refs/remotes/hub/timeline/app/tl/app-m2-public-trim-native-or-refuse-r40
C13_ARCHIVE="$APP/vendor/artifacts/banodoco-timeline-composition-0.0.13.tgz"
git -C "$APP" merge-base --is-ancestor "$R40_SHA" "$R40_HUB_BRANCH"
test "$(git -C "$APP" rev-parse HEAD)" = 0cc2583aaf07e89190b9344b5ac82849d6279586
test "$(git -C "$APP" rev-parse HEAD^{tree})" = 320e74a93676c781e83885b86ec237b4a1465d80
test -z "$(git -C "$APP" status --porcelain --untracked-files=normal)"
test "$(git -C "$AGENT" rev-parse HEAD)" = 6efc81500a0e0688c2bb41e736503f0fc3e04abb
test "$(git -C "$AGENT" rev-parse HEAD^{tree})" = 2ed2b8a12b5b3391ca221ba6ff05390f71a73556
test "$(git -C "$RUNTIME" rev-parse HEAD)" = 95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c
test "$(git -C "$RUNTIME" rev-parse HEAD^{tree})" = d3a290b407fa61e6ab2d476f50c068073f70df00
test "$(jq '.artifacts | length' "$RUNTIME/contract/artifacts.json")" = 76
test "$(sha256sum "$C13_ARCHIVE" | awk '{print $1}')" = 9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738
test "$(tar -tzf "$C13_ARCHIVE" | awk 'NF && $0 !~ /\/$/ {n++} END {print n+0}')" = 77
test -z "$(find "$GRAPH/node_modules" -type l -print -quit)"
```

If the main run uses the exact committed r43 fallback, record its SHA/tree
(`76d1397d8` / `9ac48c4d7a5152be3469781178fb9987ca95909f`) instead of the
integrated pair above; do not relabel one as the other. In both cases preserve
the exact r40 reachability check, clean source checkouts, and symlink-free
private graph. Shared installs/caches must have no writes.

On any failure, stop once, preserve the entire evidence directory, and report:
the first non-2xx method/path/status plus `code`/`type`/`location` when
available, the first page/console/request-failed/error-context boundary, the
Playwright trace, raw request/response context, and the executed/failed test
count. Do not retry, change selectors/timeouts/assertions, or infer a Runtime
cause from a generic 503. No actual was run for this packet.
