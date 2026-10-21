# App2 M2 producer ownership active-route repair

## What changed

Repaired the ownership-carrier gap from safety review 0202 within the assigned App files only:

- Transcript caption `clip.update.app` now carries `managedBy` beside `__generated__`. The compiler preserves this update payload, so a reloaded reader sees the fresh caption as owned and the next regeneration can update it.
- Scene Phase `clip.update.app` now carries `managedBy` in both fresh-shot builders. The existing `clip.add` metadata remains for direct patch consumers, but ownership no longer depends on the compiler retaining add metadata.
- Existing foreign-owned/user guards and all prior positive/negative assertions remain intact.
- No shared `useTimelineOps`, generic capture, timeline-patch compiler, DTO, pin, timing policy, or writer was changed.

## Live callers

No live caller implementation changed. The affected route callers remain:

- `transcriptLaneExtension` at `src/tools/video-editor/dev/transcript-lane/extension.ts:775`, which calls `buildTranscriptCaptionPatch`.
- `createShotsFromMarkers` at `src/tools/video-editor/dev/scene-phase-markers/extension.ts:805-806`, which calls either fresh-shot builder.
- `alignShotsToTransitions` and `ScenePhaseMarkersPanel` continue to enter `createShotsFromMarkers` for fresh Scene output.

## RED/GREEN evidence

The 0202 safety review recorded the candidate RED as two expected failures: transcript non-owned deterministic-ID update and Scene Phase foreign/user alignment. Its pre-repair candidate GREEN was 8 files / 492 tests, but it did not prove fresh output ownership after compiler acceptance and reload.

This repair adds two focused route proofs. Each builds fresh producer output, compiles it with the existing compiler, reloads through `buildTimelineData` and `createTimelineReader`, verifies `managed === true` and the extension ID, performs a second owned operation, and deep-compares protected foreign/user clip config entries before and after.

Final GREEN:

```text
8 test files, 494 tests passed
```

The focused Scene/transcript rerun after the final assertion was 2 files / 85 tests passed.

## Test commands

Passed:

```text
node --import 'data:text/javascript,globalThis.__dirname=process.cwd()+"/config/testing"' node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/dev/transcript-lane/__tests__/transcriptLane.test.tsx src/tools/video-editor/dev/transcript-lane/__tests__/fixtureProvider.test.ts src/tools/video-editor/dev/scene-phase-markers/__tests__/patch-building.test.ts src/tools/video-editor/dev/scene-phase-markers/__tests__/ScenePhaseMarkersOverlay.test.tsx src/tools/video-editor/dev/scene-phase-markers/__tests__/panel-transition.test.tsx src/tools/video-editor/lib/timeline-patch.test.ts src/tools/video-editor/lib/timeline-reader.test.ts src/tools/video-editor/lib/managed-object-guard.test.ts
# 8 files, 494 tests passed
```

```text
node_modules/.bin/eslint --no-cache --no-warn-ignored --max-warnings 0 src/tools/video-editor/dev/transcript-lane/extension.ts src/tools/video-editor/dev/transcript-lane/__tests__/transcriptLane.test.tsx src/tools/video-editor/dev/transcript-lane/__tests__/fixtureProvider.test.ts src/tools/video-editor/dev/scene-phase-markers/extension.ts src/tools/video-editor/dev/scene-phase-markers/__tests__/patch-building.test.ts src/tools/video-editor/dev/scene-phase-markers/__tests__/ScenePhaseMarkersOverlay.test.tsx src/tools/video-editor/dev/scene-phase-markers/__tests__/panel-transition.test.tsx eslint.strict-debt.js
# passed
```

```text
git diff --check
# passed
```

The initially prescribed `/tmp/ap2-vitest-runner.cjs` wrapper was absent in this environment, and direct `--configLoader=runner` first failed because the repo config uses CommonJS `__dirname`. The final command supplied only that config compatibility value via Node `--import`; no repo or dependency files were changed.

## Active generic route limitation

The app-bearing producer batch remains `mixed` for `classifyGenericPatch`. The active generic capture port supports structural `clip.add` but does not support the app-bearing `clip.update`; `useTimelineOps` therefore sends the mixed batch to generic capture, which atomically refuses it. This refusal was preserved and explicitly asserted. The exact native prerequisite is a supported native capture member for carrying the ownership/provenance app fields (or an equivalent approved native producer carrier). This worker did not bypass or modify that path.

## Blocked / next step

No browser, localhost, Runtime-door, socket, or full-suite run was performed, per task boundary. The required mounted `/tools/video-editor` live route proof—accepted submission, reload, retry/reload, and byte-for-byte foreign/user preservation—remains required before merge. The focused compiler/reader proof is not a substitute for that live proof.
