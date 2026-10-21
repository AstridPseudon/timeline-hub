# Producer source-two-file current HOME report

## Result

Ported the reviewed producer test/capture source onto current HOME. The only
worktree changes are:

- `tests/e2e/local/producer-ownership-current-pin.spec.ts`
- `tests/e2e/local/support/producer-ownership-current-pin.ts`

The original test body and assertions are retained. The settled corrections are
present: retired `transcript-lane-chip` selector to the mounted
`transcript-lane-occurrence` marker, authored `at` intent versus native wire
`on`, and the existing four-verb zero-legacy request detector. No live callers
changed (NONE).

I did not port `scripts/testing/run-producer-public13-list.sh`, the producer
Playwright config, or any bespoke launcher, custody, hash-packet, framework,
pin, graph, install, App documentation, or `.gitignore` content.

## Independent review

Independent source review passed after the final edit:

- exactly two added paths;
- no exact old selector or old native `args: { at: 1 }` oracle;
- occurrence selector and native `args: { on: 1 }` oracle present;
- detector observes POST/PUT/PATCH/DELETE against the established legacy
  film-save suffixes;
- no producer config or public13 launcher exists in the worktree;
- existing production imports resolve by source inspection;
- final lint and whitespace checks passed.

The prior 0903 independent approval and 0908 zero-legacy review were used as
the source authority; no behavior assertion was removed or weakened.

## Verification

Targeted existing capture/member/extension-ownership controls:

```text
./node_modules/.bin/vitest run --no-cache --config config/testing/vitest.config.ts \
  src/tools/video-editor/commands/genericPatchCapture.test.ts \
  src/tools/video-editor/dev/transcript-lane/__tests__/transcriptLane.test.tsx \
  src/tools/video-editor/dev/transcript-lane/__tests__/fixtureProvider.test.ts \
  src/tools/video-editor/dev/scene-phase-markers/__tests__/patch-building.test.ts \
  src/tools/video-editor/dev/scene-phase-markers/__tests__/ScenePhaseMarkersOverlay.test.tsx \
  src/tools/video-editor/dev/scene-phase-markers/__tests__/panel-transition.test.tsx \
  src/tools/video-editor/lib/timeline-patch.test.ts \
  src/tools/video-editor/lib/timeline-reader.test.ts \
  src/tools/video-editor/lib/managed-object-guard.test.ts
```

PASS: 9 files, 508 tests.

```text
./node_modules/.bin/eslint --no-cache --no-warn-ignored --max-warnings 0 \
  tests/e2e/local/producer-ownership-current-pin.spec.ts \
  tests/e2e/local/support/producer-ownership-current-pin.ts
```

PASS.

```text
./node_modules/.bin/tsc -p tsconfig.app.json --noEmit --pretty false
```

FAIL: current HOME reports unrelated App errors in
`src/tools/travel-between-images`, `src/tools/video-editor`, and Composition
API consumers. The log is
`/tmp/producer-current-tsc.log`. `tsconfig.app.json` includes `src` and
excludes e2e tests; none of the reported diagnostics is in the two added files.

Exact discovery-only command (no actual/browser run):

```text
./node_modules/.bin/playwright test \
  tests/e2e/local/producer-ownership-current-pin.spec.ts --list
```

FAIL before test collection: the existing config could not allocate
`PLAYWRIGHT_PORT` after 80 attempts. Log:
`/tmp/producer-current-list.log`. No producer actual, browser, localhost,
socket, build, launcher, central integration journey, or full suite ran.

Final file lint/diff checks reported no whitespace diagnostics. No build output
or cache was left in the worktree.

## Remaining block

The true remaining carrier block is unchanged: the current generic/native
capture path does not carry the full app-bearing, non-scalar producer
`clip.update` payload for transcript/Scene ownership updates, so the mounted
route's accepted producer proof remains unqualified and may visibly refuse
atomically. The ordinary central fallback remains a separate path and was not
changed or claimed here.

