# App public12/render current-safety composition

Candidate **HELD** pending the FINAL Agent12/Runtime pair. Bounded source composition completed without conflicts; no whole integration merge or actual Runtime qualification.

## Exact source and allowlist

Worktree: `/home/user/work/wt/app-m3-release12-current-safety-compose`.
Base: `tl/app-m3-render12-private-cache-review`, final HEAD `438a70b201d8309040142ed306af3d7355745138`.
Reviewed integration source: `75df44e99bed22db39430e420d82764126c9a316`.

Applied only the SDK two-file diff `8846d7189^..8846d7189` (commit `8846d7189ddc3f24e8fc7186d5f55e8949efae90`), and the six-file first-parent merge diff `75df44e99^1..75df44e99`. The latter includes the final `5685f7517` typed-422 assertion and earlier referenced/contiguous fixtures. Exact input patches are in `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-release12-current-safety-compose/notes/unit-{0,1}.patch`.

Only these eight tracked paths changed:

- `src/examples/transcript-panel-example.ts`
- `src/integrations/runtime/dataProvider.ts`
- `src/sdk/examples-governance.test.ts`
- `src/tools/travel-between-images/pages/ShotEditorView.test.tsx`
- `src/tools/travel-between-images/pages/ShotEditorView.tsx`
- `src/tools/video-editor/data/shotCompositionEditor.ts`
- `tests/e2e/local/support/harness.ts`
- `tests/integration/runtimeRestore.test.ts`

All eight final files are byte-equal to the exact `75df44e99` source, including the required three production shot files: `ShotEditorView.tsx`, `dataProvider.ts`, and `shotCompositionEditor.ts`. No conflict exception was needed. SHA-256 fingerprints and equality results: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-release12-current-safety-compose/notes/source-audit.json`.

The SDK example uses the optional public preview service, DOM anchor, timeline seconds and returned disposal. Shot saves overlay changed form fields on raw authored settings, retain opaque payloads through read/edit/publication, avoid publishing unchanged defaults, and visibly keep drafts when a form lacks complete authored content. This preserves the reviewed direct writer safety repair; it adds no native command activation.

The only harness delta is the optional `seedThreeProducts(referenceAt = THREE_PRODUCTS_REFERENCE_AT)` parameter and its use for the transition reference. Only the new settings case calls `(3)`. `THREE_PRODUCTS_REFERENCE_AT = 15`, the original M1 restore test body and every original assertion remain exact. No passing behavior test was weakened, removed, skipped or marked failing. Modern harness members and the existing public12/test-helper/track-label/privacy/opaque-history closures remain intact through the exact eight-path allowlist; no old session/cohort was copied.

Growth against the candidate base: **8 files, +612/-7, net +605 lines**. Production: four files, +83/-1, net +82; test files: +527/-4, net +523; harness: +2/-2, net zero. No report/build/temp output was added to the worktree. Whole candidate patch SHA-256: `fbe6b3bfc369a6c79a06f6ce0f20d317b311143c50b31140138c410f1b1056c1`.

## Cache-safe dependency audit

Only this worktree's ignored `node_modules` link was repointed to `/tmp/app-coherent-deps12/node_modules`. No shared package, symlink, cache or runtime/venv contents were modified. Vitest used the existing notes preload above, which derives `__dirname` from this worker's current directory, plus `--configLoader=runner --no-cache --maxWorkers=1`. This bypasses the default bundle loader and shared caches; no extra effect aliases or config semantics were added.

All **77 installed Composition files** match the immutable `vendor/artifacts/banodoco-timeline-composition-0.0.12.tgz` byte-for-byte. Artifact SHA-256: `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`. Sorted relative-path hash manifest: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-release12-current-safety-compose/notes/composition77.sha256` (aggregate `fd8c9063a3fb5da59cc4e33eecbf859f5dcb87e63ce8ddf848619bd3c20b8536`; format is `HASH  PATH\n`).

The six peer manifests (React, React DOM, Remotion, Player, Media, Layout Utils) match the prior review's hashes and remain unchanged. Full before/after file hashes, peer hashes and recursive cache metadata are in `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-release12-current-safety-compose/notes/deps-before.json` and `deps-after.json`; they compare exactly, including cache child mtimes/ctimes/sizes. Observed cache root mtimes, unchanged during this run:

```text
/home/user/work/app/node_modules/.cache: absent
/home/user/work/app/node_modules/.vite: 2026-10-20T02:56:11.866370+00:00 (1792464971866370272 ns)
/home/user/work/app/node_modules/.vite-temp: 2026-10-20T08:36:50.295585+00:00 (1792485410295585193 ns)
/tmp/app-coherent-deps12/node_modules/.cache: absent
/tmp/app-coherent-deps12/node_modules/.vite: 2026-10-20T07:51:42.787424+00:00 (1792482702787424251 ns)
/tmp/app-coherent-deps12/node_modules/.vite-temp: 2026-10-20T08:32:56.447571+00:00 (1792485176447571292 ns)
```

Prior shared-cache activity is retained and disclosed, never cleaned or described as historically untouched. Root, evaluation and theme-api imports resolve. Public `DEFAULT_THEME` remains the complete navy/Arial/cyan `banodoco-default` value (1920x1080, 30 fps, 450 ms fade); export inspection is in `notes/controls.log`.

## Exact checks and results

All commands ran from the assigned worktree. Vitest: **23 files, 1,138 tests passed**, zero failed/skipped/todo:

- Focused shot lane: **5 files / 74 passed**.
- SDK governance + hover: **2 files / 630 passed**.
- Shot/provider/settings neighbors: **4 files / 125 passed**.
- Preview, label, command projection, current renderer and render controls: **12 files / 309 passed**.

```sh
node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/app/notes/snapshot-vitest-runner.cjs node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 src/tools/travel-between-images/pages/ShotEditorView.test.tsx src/tools/video-editor/data/shotCompositionEditor.test.ts src/tools/video-editor/data/shotCompositionEditor.opaqueRemap.test.ts src/tools/travel-between-images/providers/VideoTravelSettingsProvider.test.tsx src/shared/state/createEntityStore.test.ts

node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/app/notes/snapshot-vitest-runner.cjs node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 src/sdk/examples-governance.test.ts src/tools/video-editor/components/PropertiesPanel/TranscriptPanel.hover.test.tsx

node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/app/notes/snapshot-vitest-runner.cjs node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 src/integrations/runtime/dataProvider.test.ts src/tools/video-editor/data/shotCompositionProjection.test.ts src/tools/video-editor/data/shotCompositionAdapter.test.ts src/tools/travel-between-images/settings.test.ts

node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/app/notes/snapshot-vitest-runner.cjs node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewComposition.commandProjection.test.tsx src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewComposition.initialRead.test.tsx src/tools/video-editor/commands/trackLabelCapture.test.ts src/tools/video-editor/commands/trackLabelGesture.test.ts src/tools/video-editor/hooks/useTimelineOps.trackLabel.test.ts src/tools/video-editor/hooks/useTimelineCommandSession.projection.test.tsx src/tools/video-editor/compositions/TimelineRenderer.test.tsx src/tools/video-editor/compositions/TimelineRenderer.sequence.test.tsx src/tools/video-editor/compositions/TimelineRenderer.shots.test.tsx src/tools/video-editor/compositions/TimelineRenderer.dynamic.test.tsx src/tools/video-editor/hooks/useRenderState.test.tsx src/tools/video-editor/components/TimelineRenderControls.test.tsx
```

Additional checks, all exit zero:

```sh
node node_modules/eslint/bin/eslint.js src/examples/transcript-panel-example.ts src/integrations/runtime/dataProvider.ts src/sdk/examples-governance.test.ts src/tools/travel-between-images/pages/ShotEditorView.test.tsx src/tools/travel-between-images/pages/ShotEditorView.tsx src/tools/video-editor/data/shotCompositionEditor.ts tests/e2e/local/support/harness.ts tests/integration/runtimeRestore.test.ts
node --test config/vite/timelineCompositionPackage.test.mjs
node scripts/quality/check-known-failures.mjs
node scripts/quality/check-no-smoke-tests.mjs
git diff --check
```

ESLint: no output. Package boundary Node test: **1/1 passed**. Known failures: three existing authorized markers, zero forbidden. Placeholder smoke check: passed. Detailed logs and exact commands are under `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-release12-current-safety-compose/notes`; `run-focused.py` records per-lane exit codes in `test-results.json`. Dependency audit command: `python /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-release12-current-safety-compose/notes/audit-deps.py`, run before/after, exact snapshots equal. Static original-M1 body containment, default15 and source byte comparisons also passed.

Inherited source-only public12/render evidence (233 + 357 + nine Node helper files) remains the prior review's evidence; this task did not rerun or recast those counts. The current candidate's additional focused evidence is the set above.

## Remaining pin, limits and next step

Root `package.json`, lockfile, package pins, native writer activation and `runtime.lock.json` are unchanged. Runtime **0.2.8 is the existing PLACEHOLDER, not the FINAL matching pair**: `runtime.lock.json` source commit remains `1ad39f5c4bf834736bb2ee04b031eebbcdb11ce0`, producer version `sha256:4010d93be2a8bfc7cc051c383e165ff81835c3d12ba9a137279741b7883748a7`; generated contract metadata stays `0.2.8`. Agent12 is not pinned/qualified here.

No full suite, actual Runtime gate, browser, build, project tsc, install, localhost or socket suite was requested or run. The composed Runtime restore/settings integration test is preserved in source but **unexecuted here**; its prior historical-pair pass is not evidence for this candidate's final pair. Native MP4/download, frame/audio parity and planted mismatch are also unverified here. Draft refusal retention is in-memory, not a new crash-safe guarantee.

No new design decision, blocker or evidence against PLAN. The only routine choice was to apply the two exact diffs without conflict edits and retain the approved runtime pin placeholder. Orchestrator should review/commit this eight-file unit, keep the whole candidate HELD, then select the FINAL Agent12/Runtime pair and authorize the matching integration/render qualification. No git commit/merge/rebase/checkout/push/ref mutation performed.
