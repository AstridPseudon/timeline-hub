# App M3 cap port review file list

- Base actual SHA: `3599fc49ad76dfdd7847ab4c813fc9317a0304eb`
- Base actual tree: `74130f681f6b0c87a7c61cb33d4ae6a092c03046`
- Frozen cap final SHA: `93696b62f30cf86eac632f975a80de4851489c17`
- Frozen cap final tree: `8465cfeec6a77ed66b6a150205ddca768476e8e4`
- Patch: `app-cap-integrated-root-port.patch`
- Working-tree delta: 22 files, 19 modified and 3 added.

## Files

Modified:

- `src/tools/travel-between-images/components/ShotTimelinePreview.test.ts`
- `src/tools/travel-between-images/components/ShotTimelinePreview.tsx`
- `src/tools/travel-between-images/components/shotTimelineDataProvider.ts`
- `src/tools/video-editor/components/PreviewPanel/RemotionPreview.tsx`
- `src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewSurface.lifecycle.test.tsx`
- `src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewSurface.test.tsx`
- `src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewSurface.tsx`
- `src/tools/video-editor/data/DataProvider.ts`
- `src/tools/video-editor/data/canonicalCompositionState.ts`
- `src/tools/video-editor/data/shotCompositionProjection.ts`
- `src/tools/video-editor/hooks/useTimelineCommandSession.projection.test.tsx`
- `src/tools/video-editor/hooks/useTimelineCommandSession.ts`
- `src/tools/video-editor/hooks/useTimelinePersistence.test.tsx`
- `src/tools/video-editor/hooks/useTimelinePersistence.ts`
- `src/tools/video-editor/hooks/useTimelineSave.draftConfig.test.ts`
- `src/tools/video-editor/hooks/useTimelineSave.draftConfig.ts`
- `src/tools/video-editor/lib/canonicalRenderBounds.ts`
- `src/tools/video-editor/lib/serialize.test.ts`
- `src/tools/video-editor/lib/serialize.ts`

Added:

- `src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewSurface.storedCap.test.tsx`
- `src/tools/video-editor/data/canonicalCompositionState.mainImageCap.test.ts`
- `src/tools/video-editor/data/mainImageCap.fixture.json`

## Application check

The patch applies to a clean archive of base SHA `3599fc49ad76dfdd7847ab4c813fc9317a0304eb` without rejects. The final worktree has no `.rej` or `.orig` files. Consumer review remains required before merge; this artifact makes no pixel/parity claim.
