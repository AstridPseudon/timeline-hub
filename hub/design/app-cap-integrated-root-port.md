# App M3 stored-cap port onto the actual root

## Scope

Ported the complete frozen cap delta from `b1ef4b9b910ba72375c34cf319692f90d22edc25` through `93696b62f30cf86eac632f975a80de4851489c17` (final tree `8465cfeec6a77ed66b6a150205ddca768476e8e4`) onto actual root `3599fc49ad76dfdd7847ab4c813fc9317a0304eb` (root tree `74130f681f6b0c87a7c61cb33d4ae6a092c03046`).

The port is join-only. Applying the exact `b1 -> 93696` patch to a fresh `3599` archive reproduced this worktree byte-for-byte, apart from worktree-only `.agents`, `.aws`, `.codex`, and `node_modules` entries. No original root guards were rebased, and no public13 or automatic-placement ancestry was imported.

## Delivered behavior

- Keeps one derived `storedOccurrenceDurationMs` scalar for render selection while preserving editor/read geometry.
- Carries the existing verified raw composition basis through serializers and draft arguments.
- Uses identity-based raw counterparts, preserving same-name opaque/prototype/null/order fields and refusing ambiguous or missing bases while retaining the draft.
- Delivers config, transition vector, provenance, and extent atomically for stored 4000/4500 selections.
- Preserves initial hydration, recovery, cache, preload, and private-mode IndexedDB readiness.
- Applies the two ES2020-safe own-property fixes, including the popup path.

## Evidence

Command:

```text
git diff --check && ./node_modules/.bin/vitest run --no-cache --config config/testing/vitest.config.ts \
  src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewComposition.initialRead.test.tsx \
  src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewSurface.lifecycle.test.tsx \
  src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewSurface.test.tsx \
  src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewSurface.storedCap.test.tsx \
  src/tools/video-editor/hooks/useTimelineCommandSession.projection.test.tsx \
  src/tools/video-editor/hooks/useTimelinePersistence.test.tsx \
  src/tools/video-editor/hooks/useTimelineSave.draftConfig.test.ts \
  src/tools/video-editor/lib/serialize.test.ts \
  src/tools/video-editor/data/canonicalCompositionState.mainImageCap.test.ts \
  src/tools/travel-between-images/components/ShotTimelinePreview.test.ts
```

Result: 10 test files passed, 219 tests passed. No full suite, project-wide TypeScript check, build, browser, socket, install, or pixel/parity claim was made.

## Review boundary

The single review patch is `app-cap-integrated-root-port.patch`; its companion manifest is `app-cap-integrated-root-port-FILELIST.md`. Both are against actual root `3599fc49ad76dfdd7847ab4c813fc9317a0304eb` / tree `74130f681f6b0c87a7c61cb33d4ae6a092c03046`. Do not merge until Viewing consumer review.
