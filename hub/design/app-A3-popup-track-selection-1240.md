## Report

Implemented the minimal popup track-selection fix in `useClipDrag.ts`.

- Pointer selection now updates `selectedTrackId` to the clicked clip’s actual row.
- Additive/shift selection remains multi-select.
- Toggle-clearing does not invent or change a track.
- Unknown clip rows are refused unchanged.
- Production callers: `TimelineEditorCore.tsx:435` and `TimelineEditorCoreBody.tsx:425`.

RED:

```text
useClipDrag.test.tsx — 20 passed, 1 failed
Expected selectedTrackId V2, received V1
```

GREEN:

```text
79 tests passed across:
- useClipDrag.test.tsx: 24
- ClipAction.test.tsx: 45
- ShotTimelineMediaControls.test.tsx: 10

Root/App/Node TypeScript checks: passed
Scoped ESLint: passed
git diff --check: passed
```

Source: `cca3deb361e8fbbc62ddf491d5fd09c7e542b99f`  
Tree: `911956d49c42021f11d21e9cf69e9e9478ab569a`  
Parents: `d99396bca7c3853435cfa5a5991f5b1073187be4`, `8a712d39c74e92ff10886007ae5135d4f316e92e`

Only modified:

- `src/tools/video-editor/hooks/useClipDrag.ts`
- `src/tools/video-editor/hooks/useClipDrag.test.tsx`

Provider, popup component, selection store, drag helper, and protected save/contract files were unchanged. No blockers. Commit message and `DONE` marker were written; harness will commit.