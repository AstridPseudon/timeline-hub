# App stored-cap 8488 owner port

## Source and scope

- Working branch: `tl/app-m3-stored-cap8488-main574-public13-owner-port`
- Current base HEAD: `d12d0909746c552dee6dac7b5d8459e8e1f27679`
- Current base tree: `c91e3c07f293658aa0f26dd180ac464c45b71559`
- Frozen producer source reviewed: `3a4350f9d9a578f817568d5fe348c5d750595129` (Root 3599..3a)
- Frozen corrected consumer source reviewed: `8488f9c1c2e3eafd924720e5bcd49a950798ffed` (parent 3a)
- Public13 artifact: `vendor/artifacts/banodoco-timeline-composition-0.0.13.tgz`, SHA-256 `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`
- Uncommitted patch SHA-256: `8ea2d609fc1e8bdcebec0521fd3c89d5ca510bc697ebb56e70b1ebb861f3b6d8`

The producer and corrected consumer commits were used as frozen source references; neither is an ancestor of the current integration tip, so no old root ancestry was merged. The port changes exactly these 11 consumer-owned files:

```text
src/tools/video-editor/components/PreviewPanel/TimelineFramePreview.test.tsx
src/tools/video-editor/components/PreviewPanel/TimelineFramePreview.tsx
src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewComposition.ts
src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewSurface.lifecycle.test.tsx
src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewSurface.tsx
src/tools/video-editor/components/PropertiesPanel/VideoEditorAssetPanelSurface.tsx
src/tools/video-editor/hooks/useClientRender.ts
src/tools/video-editor/hooks/useRenderState.ts
src/tools/video-editor/hooks/useTimelineState.ts
src/tools/video-editor/lib/canonicalRenderBounds.test.ts
src/tools/video-editor/lib/canonicalRenderBounds.ts
```

## Implementation decisions

- Kept one derived `storedOccurrenceDurationMs` in existing `canonicalTiming`; render-only copies use the stored value only when it is finite, non-negative, and below the effective duration, otherwise each clip falls back to its effective bound.
- Threaded the paired config/fact, compiled transition vector, and bounded duration atomically through Player, still preview, and client render.
- Preserved current App2 `elementPort`/generic ports and current-root label hydration. The lifecycle neighbor's two stale label expectations were adapted to the current output projection; stored-cap private-copy identity and all positive geometry assertions remain.
- Preserved the current `canonicalRenderBounds` surface, including App2 removal of the obsolete `boundCanonicalRenderConfig`; no old producer file was copied wholesale.
- No package, lockfile, pin, DTO, store, persisted `renderConfig`, second compiler, editor semantics, browser, or physical pixel/audio claim was added.

## Evidence

All Vitest commands used a private public13 alias/config under `/tmp`, `--configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism`, and the shared node_modules remained read-only.

- Producer, consumer, serialization, recovery, and source-clock controls: **15 files, 288 tests passed**.
- Corrected consumer sublane plus selected client-render tests: **4 files, 56 passed, 44 name-filtered skips**.
- Public13 evaluator probe: **passed**; 4000 ms gives root draw duration 120, opacity at frame 105 = 0.5, frame 120 empty; 4500 ms gives duration 135, opacity 1, frame 120 active.
- Scoped ESLint on all 11 changed files: **passed**, no findings.
- `git diff --check`: **passed**.
- One allowed `tsconfig.app.json --noEmit` run: **failed on existing/current-root App2 command diagnostics and shared public12 declarations** (`computeMediaTrim`, `encodedEnvelopeSource`, and `getSanitizedPlaybackRate` unavailable in the shared 0.0.12 types). No diagnostic named any of the 11 changed files. No retry or source weakening.

Not run: full suite, browser/e2e, install, live sockets, build, physical frame capture, or PCM/pixel parity.

## Handoff limits

This is an uncommitted working-tree port only. The harness should commit it. Manager review must recheck the current gate/source-consumer cohort before integration; this report makes no integration, ledger, full-suite, or parity claim.
