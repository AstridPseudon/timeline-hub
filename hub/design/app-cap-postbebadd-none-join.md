# App stored-cap postbebadd/None join

## Source

- Current root: `c57dcc26162642f503532f143ceb96bb185273aa`.
- Applied the approved candidate delta from `0d5009e18bee8e29f894dabf5db501a0fcea750f` to `6b7afe3ad28e6a899a09b15fbfaa5e79f4b05214` (candidate tree `32dc0de053ffb98d718077a111994181ae03ea15`). The delta is exactly the 30-file union: 22 producer files plus 11 corrected consumer files, with three shared paths.
- Preserved current MAINbebadd, native `None` scalar, label5404/current-root changes, corrected media carrier, Generic/Element projectors, and source/PCM guards. No whole current shared file was replaced.
- One lifecycle hunk was resolved against current `resolvedConfig` wrappers by changing the accepted assertion to compare `boundCanonicalRenderConfig(acceptedClosure.resolvedConfig)`.
- Added a bounded fail-closed serializer guard and regression in the existing cap serializer files: a projected config containing `storedOccurrenceDurationMs` now refuses `serializeForDisk`/`serializeResolvedTimelineEdit` without a verified raw basis. Raw-backed serialization still strips only the derived scalar and restores raw same-name metadata, nulls, opaque keys, own `__proto__`, and ordering.

## Evidence

All Vitest runs used the composed worktree, the private public13 dependency overlay, the private Vite cache config, `--configLoader=runner --no-cache`, one worker, and no shared dependency/cache writes.

- Cap + serializer controls: 3 files, 50 tests passed.
- Lifecycle/session/graph/projection controls: 11 files, 254 tests passed. The previously reported eight MAIN574 label failures now pass on the current-root composition.
- Scalar/generic/element/duplicate/add controls: 9 files, 130 tests passed.
- Timeline/commit/render/PCM neighbor controls: 8 files, 272 tests passed.
- Total targeted evidence: 31 files, 706 tests passed.
- Scoped ESLint over the 30 cap paths (JSON fixture excluded as non-configured) and scalar/generic/element controls: exit 0.
- `git diff --check`: exit 0; no reject/orig files remain.

The exact successful Vitest command prefix was:

```text
env -u ASTRID_CHECKOUT node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-complete-stored-cap-producer-consumer-current-join/notes/dirname-preload.cjs /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-complete-stored-cap-producer-consumer-current-join/private13/node_modules/vitest/vitest.mjs run --config /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-complete-cap-postbebadd-none-join/private-cache-v13.config.mjs --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism
```

The four successful invocations appended these file groups to that prefix:

```text
src/tools/video-editor/lib/serialize.test.ts src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewSurface.storedCap.test.tsx src/tools/video-editor/lib/canonicalRenderBounds.test.ts

src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewComposition.initialRead.test.tsx src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewSurface.lifecycle.test.tsx src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewSurface.test.tsx src/tools/video-editor/components/PreviewPanel/TimelineFramePreview.test.tsx src/tools/video-editor/data/canonicalCompositionState.test.ts src/tools/video-editor/data/shotCompositionProjection.test.ts src/tools/video-editor/hooks/useTimelineCommandSession.projection.test.tsx src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx src/tools/video-editor/hooks/useTimelinePersistence.test.tsx src/tools/video-editor/hooks/useTimelineSave.draftConfig.test.ts src/tools/travel-between-images/components/ShotTimelinePreview.test.ts

src/tools/video-editor/commands/clipScalarCapture.test.ts src/tools/video-editor/commands/clipScalarGesture.test.ts src/tools/video-editor/commands/commitSession.clipScalar.test.ts src/tools/video-editor/commands/commitSession.genericPatch.test.ts src/tools/video-editor/commands/elementCapture.test.ts src/tools/video-editor/commands/genericPatchCapture.test.ts src/tools/video-editor/commands/occurrenceDuplicateCapture.test.ts src/tools/video-editor/commands/occurrenceDuplicateGesture.test.ts src/tools/video-editor/commands/parentClipAddCapture.test.ts

src/tools/video-editor/lib/clipDisplayNames.test.ts src/tools/video-editor/lib/timeline-data.test.ts src/tools/video-editor/commands/commitSession.test.ts src/tools/video-editor/hooks/useTimelineOps.test.ts src/tools/video-editor/hooks/useTimelineOps.trackLabel.test.ts src/tools/video-editor/hooks/useRenderState.test.tsx src/tools/video-editor/compositions/continuousPCM.contract.test.tsx src/tools/video-editor/compositions/continuousPCM.lifetime.test.tsx
```

## Limits / handoff

- No project `tsc`, full suite, build, install, browser/e2e, localhost/live socket, actual render, or frame/audio parity run was performed. The ten known App2 type diagnostics remain peer-owned and are not claimed fixed.
- This is source-gate evidence only; it makes no frame/PCM parity claim.
- Viewing seam review remains requested. No integration merge or branch/ref mutation was performed by this worker.
