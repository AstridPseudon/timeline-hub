# Refreshed-main four-case frame gate

**Prepared, unqualified staging. READY-only; no grant or actual comparison.**

Base App commit `667498cc49b4ec2b1ccd3a515eb87311c5126c93`, tree
`74d6c8033b1e006e8dbd4accc361b4e1288093e9`. This is the committed refresh source,
not an integration or owner-full qualification claim. A later source refresh
requires a new content freeze and owner tuple.

## Exact change

31 added test/config files, 3,210 lines; zero changes to previously tracked
files. Product render, download, preview, provider, package artifacts and pins
remain byte-for-byte main. No old 320784 product helpers, 45-file staging branch,
old grants, or old leased source tuple were adopted.

The necessary test helper closure comes from `tl/vw-m3-frame-capture-next-candidate`
(shared four-case registration, fixture, canvas, managed-media generation,
admission/authority/download checks, strict diagnostics, source guards, capture,
and Agent launcher adapter). Original640 media source and base Playwright config
are byte-identical to `4360c759`. The native canvas is separately explicit:
1920x1080, viewport 2000x1200, fps30; input VP8 stays 640x360. No resize, PNG
modification, theme override, codec substitution, tolerance change, or test skip.

The exact native probe/decoder buffer block from the two-file `4360c759` delta
was ported: safe positive dimensions, safe RGB byte count, 256MiB limit,
`width*height*3 + 1024` buffer, exact decoded length. Direct tests retain the
original default640 rejection and additionally accept the generated native PNG /
lossless-video equality under the explicit1920 contract. They also exercise
failed probes and the dialog/backdrop dismissal sequence.

Both specs register the same four bodies: normal Render/download, managed Player
fixture readiness, twelve-frame comparison, and planted picture mismatch only
after the full passing baseline. RGB channel error remains2 and fraction .001.
The separate native config retains Chrome155.0.8059.84 and the pinned export
headless browser. Original640 expectations remain runnable and unchanged in
meaning, including the separate output640 diagnostic.

## New-main seams and decisions

- Use main's `Render` button and common `POST /api/astrid/v1/tasks` admission.
  Main sends canonical parent/occurrence metadata and output policy; it currently
  does **not** send `params.expected_version`. The test checks immutable Runtime
  task/snapshot/dependency authority instead of importing old admission code.
- Main's `Download` is a **button** inside role `dialog`, name `Rendered film`.
  The result is `data-testid=timeline-render-player`, whose `src` is the managed
  `/api/astrid/v1/objects/{id}` URL. Clicking uses main's direct full-object fetch,
  followed by its same-page blob fallback. The test explicitly selects that
  existing fallback by making the optional save picker unavailable; it does not
  replace fetch, intercept media, or implement a downloader. Picker streaming
  remains main code with its existing tests, not newly browser-qualified here.
- The observer now supports the direct managed-object fetch, with exact alias,
  Origin, full200/noRange/noRedirect, length, digest and saved-byte equality.
  The older location+object observer contract and all its positive/negative
  tests remain intact. No location read is fabricated for the new path.
- Assert `download.suggestedFilename()` equals the authored output filename;
  inspect downloaded MP4 bytes and ffprobe without transcoding. Preserve main's
  filename and managed MP4 exactly.
- `preview-revision-label` still reads `Committed {parentRevision}`. The rendered
  dialog's `Timeline version N` description is a **local acknowledged config
  counter**, not committed-revision authority. Read it through `aria-describedby`.
  `revision-and-delivered-config.json` records that local fact separately from
  the immutable committed parent revision/digest/task authority, authored output,
  filename and delivered ffprobe configuration. No product label is rewritten.
- Capture closes `Rendered film` through its normal `Close` button, waits for
  dialog and `[data-dialog-backdrop]` detachment, then uses the existing mounted
  Player-ref seek/readiness path. After comparisons, remove only the test sizing
  style and reopen main's `Play last render` button for the existing strict
  same-case result-video diagnostics. Otherwise dialog detachment removes the
  video those diagnostics require. Native media errors stay failures.
- Main's `DirectHarness.runtimeEnv()` is private. The test launcher adapter uses
  the already-frozen absolute Runtime/Agent paths and Python environment instead
  of changing main's method visibility or copying its old harness implementation.

Source guards now require `VIEWING_FRAME_SOURCE_TUPLE` with actual owner pins:
all source commit/tree pairs, App content identity (central snapshots have
synthetic commits), official matching Runtime/generated-client bytes, selected
Agent Remotion root, and both six-file peer manifests. Both immutable0.0.12
archives must hash to
`sha256:0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`;
all77 installed package files are checked independently in both consumers.
No expected peer hashes are learned from the shared install. Finally postflight
checks graph/source/tuple identity even on setup/test/close failure, preserving
both failures; actual fixtures require held flock and absent QUIET. Native
setup checks sources before delegating to main's hosted build.

## Validation

All commands used the assigned App worktree or the worker's private graph.
Private `node_modules` and scoped parent directories are real directories with
read-only package leaf links; no shared dependency, cache or graph was repaired
or qualified. Offline code imports do not consume the product Composition graph.

Exact path abbreviations for the commands below:

```sh
APP=/home/user/work/wt/vw-m3-main-refresh-parity-test-port
O=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
W="$O/workers/vw-m3-main-refresh-parity-test-port"
G="$W/private-graph"
N=/tmp/vw-m3-agent-gate-node20.19.4/bin/node
```

From `$G`:

```sh
TMPDIR="$G/tmp" TSX_DISABLE_CACHE=1 PWTEST_CACHE_DIR="$G/cache" "$N" --require ./no-sockets.cjs --import tsx run-offline.mjs
TMPDIR="$G/tmp" TSX_DISABLE_CACHE=1 PWTEST_CACHE_DIR="$G/cache" "$N" --require ./no-sockets.cjs --import tsx --test tests/e2e/timeline/viewing-parity/*.test.ts
TMPDIR="$G/tmp" PWTEST_CACHE_DIR="$G/cache-list-original640" "$N" --require ./no-sockets.cjs node_modules/playwright/cli.js test --list --config playwright.viewing-parity.config.ts
TMPDIR="$G/tmp" PWTEST_CACHE_DIR="$G/cache-list-native1920" "$N" --require ./no-sockets.cjs node_modules/playwright/cli.js test --list --config playwright.viewing-parity.normal-profile-native1920.config.ts
```

Results: **243/243 assertions PASS**, **11/11 file-level tests PASS**, and **4 cases
listed per config**. Zero skipped/cancelled/todo. The runner imports all eleven
Node test files. `no-sockets.cjs` throws on TCP connect/listen or UDP bind/connect;
these successful commands establish side-effect-free discovery/imports. Generated
ffmpeg PNG/FFV1/VP8 tests are decoder/media plumbing, not product rendering.

From `$APP`:

```sh
node node_modules/eslint/bin/eslint.js tests/e2e/timeline/viewing-parity playwright.viewing-parity.config.ts playwright.viewing-parity.native-codec.config.ts playwright.viewing-parity.normal-profile-native1920.config.ts tests/e2e/timeline/player-export-frame-parity.spec.ts tests/e2e/timeline/player-export-normal-profile-native1920.spec.ts --report-unused-disable-directives --max-warnings 0 --no-cache
node node_modules/typescript/lib/tsc.js -p "$W/typecheck.json" --noEmit
node node_modules/typescript/lib/tsc.js -p "$W/typecheck-main-baseline.json" --noEmit
cmp "$O/design/handoff-vw-m3-main-refresh-parity-test-port-typecheck.log" "$O/design/handoff-vw-m3-main-refresh-parity-test-port-typecheck-main-baseline.log"
git diff --check
git apply --reverse --check "$O/design/handoff-vw-m3-main-refresh-parity-test-port-test-only.patch"
node --check "$O/design/handoff-vw-m3-main-refresh-parity-test-port-controller.mjs"
"$N" "$O/design/handoff-vw-m3-main-refresh-parity-test-port-controller.mjs" --check-ready
```

ESLint PASS. Both TypeScript commands exit2 with the **same single existing
TS2352 diagnostic in untouched `tests/e2e/local/support/harness.ts:630`**;
`cmp` exits0. No new type diagnostics; typecheck is not green. Diff/patch/syntax
checks PASS. Each new file also passed
`git diff --no-index --check -- /dev/null <file>` with no whitespace output.
READY check exits78 as expected, reports all owner-pending inputs, and creates
no grant/marker/run. An initial offline run exposed the now-fixed config/profile
ordering assumptions; only the final source results above are cited.

## Remaining inputs and next step

App owner must publish final consumer12 commit/tree, artifact and six peer pins
including this test port (or refresh it onto the later main first). Agent owner
must publish matching consumer12 source, artifact, host helper and six peer pins.
Runtime owner supplies the official matching source/generated-client pair and
byte pins. Manager freezes the resulting App content and full selected environment
(Node20.19.4, Chrome155/export-browser/Playwright bytes), reviews the source guards,
and supplies a **fresh** launch controller/grant under exclusive
`/tmp/timeline-viewing-browser.lock`, absent QUIET and finally postflight. The
READY-only controller here deliberately has no launch mode and cannot reuse old
grants. The nullable tuple template is not a runnable tuple.

No browser, Runtime, HTTP, socket, product render, central four-case run, full
suite, network/install, shared write, commit, merge, checkout or push was run.
Actual matching12 Player/export frames, native download and PCM remain unverified;
there is no gate6/M3/adoption/integration claim. Preparation is complete; actual
qualification remains owner-pending by design.

Flat artifacts share this report's absolute prefix: `test-only.patch`,
`delta.json`, `contract.json`, `source-tuple.template.json`, `controller.mjs`, and
validation `*.log`. No repository documentation was added.
