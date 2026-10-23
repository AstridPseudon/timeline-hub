# Handoff: app-F-save-serialize-projection-1054

Status: **BLOCKED** after fixing the unset-volume regression.

Base `7e0af6c9cda5a81a89505b006fcd653d4a5fc770`. Changed only `src/tools/video-editor/data/shotCompositionProjection.ts`: projected `volume` is now absent when source gain/volume and mute are absent; explicit numeric gain/volume, zero, and mute remain effective.

Evidence: projection test `27/27`; mandated focused post-check `140/144` with four residual failures (three serializer/signature assertions and one raw `__proto__` assertion); scoped ESLint PASS; App tsc PASS; `git diff --check` PASS.

The serializer failures are caused by forbidden `src/tools/video-editor/lib/timeline-data.ts`: `assembleTimelineData` derives labels into `resolvedConfig.clips` but hashes the pre-label `canonicalResolvedConfig`. The raw opaque failure is caused by forbidden `src/tools/video-editor/data/shotCompositionEditor.ts`: `remapOwnedItemReferences` assigns a recursive own `__proto__` key through `{}`/`next[childKey]`, changing the prototype. `ShotTimelinePreview.tsx` is not on that direct provider publish path. Do not weaken the existing expectations; expand scope or dispatch the owning fixes.
