# Independent review: refreshed-main frame parity test port

**APPROVE test port. Actual M3 gate: READY ONLY, owner-matched sources pending.**

Reviewed `tl/vw-m3-main-refresh-parity-test-port` at
`877b7f33eb5fc8afe035d984d976683702819101` against
`667498cc49b4ec2b1ccd3a515eb87311c5126c93`. The assigned review worktree has exactly
the candidate head and remains clean. Read PLAN.md, COMMON.md and App CLAUDE.md.
No repository changes were made and no blocking test-port defect was found.

## Findings

- Exactly 31 added test/config files, 3,210 lines; no modified/deleted baseline
  files. `src`, `vendor`, package manifests/lock and runtime pins have no diff.
  All 31 hashes match the supplied delta manifest. The private review copies of
  all 31 files are byte-identical to the reviewed files.
- The cases use main's mounted Render action and common task POST, catalog digest,
  canonical parent/head/occurrence metadata and ordinary MP4 download output
  policy. This matches untouched `renderRouter.ts:915–974`. They do not import
  an old 320784 product helper or construct an admission themselves. Main does
  not send `params.expected_version`; immutable Runtime snapshot, revision,
  dependency/media, capability and output authority are checked instead.
- Main's `Rendered film` dialog contains a Download button and managed-object
  video src. The port observes its direct full-object fetch and saved blob bytes;
  exact URL alias/Origin, GET/fetch, status200, no Range/redirect, size, digest,
  filename and byte equality remain required. It explicitly selects main's
  existing blob fallback by disabling the optional save picker; picker streaming
  is outside this port's browser qualification. Existing location+object
  observer expectations are retained. The displayed local `Timeline version`
  counter is recorded separately from immutable committed-revision authority.
- Native1920 is an explicit separate canvas/config: 1920x1080, 2000x1200 viewport,
  30fps, original 640x360 VP8 source. `media.ts` and the original640 base config
  are byte-identical to `4360c759`. Original640 dimension rejection and its
  separate diagnostics remain. No comparison resize, PNG rewrite, theme override,
  codec substitution, tolerance relaxation, new xfail or test weakening occurs.
  RGB channel error2 and outside fraction .001 are exercised at both sizes.
- Capture clicks the normal Close button, waits for dialog and backdrop
  detachment, and only then inspects/seeks the mounted Player. Existing image,
  font, frame-marker, pause/frame, scale1 and DPR1 readiness assertions remain.
  The test host alone gets native sizing. The result dialog is reopened after
  comparisons for strict same-case media diagnostics. The negative picture patch
  occurs after all twelve positive frames and a fresh passing selected-frame
  baseline; output bytes and task authority are rechecked.
- The decoder probe/buffer block is byte-identical to the `4360c759` delta:
  positive safe integer dimensions, safe RGB length, 256MiB maximum,
  `width*height*3 + 1024` subprocess buffer and exact output length. Real generated
  PNG/FFV1 and VP8 decoder tests pass; these are media plumbing, not product render
  qualification.
- Guard inspection: both immutable0.0.12 archives must match the pinned sha256;
  each manifest must have exactly77 unique files; each consumer's complete
  installed file set and bytes must match. Each consumer also requires the exact
  six owner-supplied Remotion/Player peer hashes. Expected hashes are not learned
  from shared installs. The source tuple requires a freeze, full source pairs,
  App content identity, matching official Runtime/client byte pins and selected
  Agent Remotion root. Unknown browser profiles and missing inputs fail closed.
  Runtime/browser fixtures check source/dependency identity before use and in
  finally after startup/test/close failure, aggregating failures. Boundary checks
  require absent QUIET, flock marker1 and a genuinely contended central lock.
- The supplied controller accepts only `--check-ready`; it has no launch/grant
  mode. Its independent run exits78 with `actual_run:false`, `grant:false`, and
  `source_guards_ready:false`. No old grant/tuple is reused. **A fresh reviewed
  manager controller/grant and complete environment-directory freeze remain
  external prerequisites**, not guards this staging controller supplies. This
  approval does not authorize a run or certify a future launch controller.

## Independent validation

All offline execution used a newly built private graph, with real node_modules
and scoped parent directories and read-only resolved package leaf links. No
shared dependency graph, venv, runtime, install or cache was changed. Test/config
sources were copied from this review worktree, not taken from the author's graph.
A preload throws on TCP connect/listen and UDP bind/connect. Cache/temp paths
were private. Node was the existing20.19.4 binary.

Exact command abbreviations:

```sh
APP=/home/user/work/wt/vw-m3-main-refresh-parity-port-review
O=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
W="$O/workers/vw-m3-main-refresh-parity-port-review"
G="$W/private-graph"
N=/tmp/vw-m3-agent-gate-node20.19.4/bin/node
```

From `$G`, each command exited0:

```sh
TMPDIR="$PWD/tmp" TSX_DISABLE_CACHE=1 PWTEST_CACHE_DIR="$PWD/cache" "$N" --require ./no-sockets.cjs --import tsx run-offline.mjs
TMPDIR="$PWD/tmp" TSX_DISABLE_CACHE=1 PWTEST_CACHE_DIR="$PWD/cache" "$N" --require ./no-sockets.cjs --import tsx --test tests/e2e/timeline/viewing-parity/*.test.ts
TMPDIR="$PWD/tmp" PWTEST_CACHE_DIR="$PWD/cache-list-original640" "$N" --require ./no-sockets.cjs node_modules/playwright/cli.js test --list --config playwright.viewing-parity.config.ts
TMPDIR="$PWD/tmp" PWTEST_CACHE_DIR="$PWD/cache-list-native1920" "$N" --require ./no-sockets.cjs node_modules/playwright/cli.js test --list --config playwright.viewing-parity.normal-profile-native1920.config.ts
```

Results: **243/243 Node tests (the reported assertions), 11/11 file-level tests,
4 listed cases per config**; zero failures/skips/cancelled/todo. The list commands
perform discovery only; global setup, browser, Runtime and real cases did not run.

From `$APP`:

```sh
node node_modules/eslint/bin/eslint.js tests/e2e/timeline/viewing-parity playwright.viewing-parity.config.ts playwright.viewing-parity.native-codec.config.ts playwright.viewing-parity.normal-profile-native1920.config.ts tests/e2e/timeline/player-export-frame-parity.spec.ts tests/e2e/timeline/player-export-normal-profile-native1920.spec.ts --report-unused-disable-directives --max-warnings 0 --no-cache
node node_modules/typescript/lib/tsc.js -p "$W/typecheck.json" --noEmit
node node_modules/typescript/lib/tsc.js -p "$W/typecheck-main-baseline.json" --noEmit
cmp "$O/design/handoff-vw-m3-main-refresh-parity-port-review-typecheck.log" "$O/design/handoff-vw-m3-main-refresh-parity-port-review-typecheck-main-baseline.log"
git diff --check 667498cc HEAD
git apply --reverse --check "$O/design/handoff-vw-m3-main-refresh-parity-test-port-test-only.patch"
node --check "$O/design/handoff-vw-m3-main-refresh-parity-test-port-controller.mjs"
env -u VIEWING_FRAME_SOURCE_TUPLE "$N" "$O/design/handoff-vw-m3-main-refresh-parity-test-port-controller.mjs" --check-ready
```

ESLint, cmp, whitespace, reverse-patch check and controller syntax: exit0.
Both TypeScript commands: exit2, **one identical existing TS2352 at
`tests/e2e/local/support/harness.ts(630,45)`**. The extension-fixture cast to
`typeof publication.parent_composition.config` conflicts because its inferred
`clips` type is `never[]`. The baseline command includes only the untouched
harness closure; that file is byte-identical to `667498cc`. The candidate command
includes all new parity TS/config/spec files plus their dependencies. Their
complete diagnostics compare byte-equal. **No new diagnostic; typecheck is not
green.** READY-only command: expected exit78, with all owner-pending inputs.

Read-only Git/Python checks separately verified the31-file status and hash list,
empty product/pin diff, byte equality with original640 and decoder reference,
private copies, real graph/scope parents and clean review worktree. Results are
in the sibling `source-checks.json`. All validation logs use this report's flat
absolute `handoff-vw-m3-main-refresh-parity-port-review-` prefix.

## Decisions, limits and next step

Kept this strictly read-only and offline. Did not fix the baseline type cast,
change product code, supply pins, generate a grant, or request a central test.
No plan decision needed changing and nothing blocks the test-port approval.

Actual M3/gate6 Player/export equality, native UI download and PCM remain
unverified. Owners must publish the matching App/Agent consumer12 sources,
artifacts and peer manifests, official Runtime/client pair, then the manager must
freeze final content/environment and supply a fresh reviewed grant/controller
with finally postflight, exclusive flock and absent QUIET. Any subsequent source
refresh needs a new freeze. Only that authorized central run can qualify media
parity. No browser/render/socket/service/full/install/network or Git mutation was
performed; no central four-case grant was created.
