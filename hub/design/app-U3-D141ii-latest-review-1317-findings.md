# U3 D141ii independent findings

Verdict: FAIL for the submitted applicability map; qualified source resolution and targeted validation PASS. No source fix was made.

## MAP-001 — protected single journey is mapped incorrectly

The author labels the gallery AddToTimeline path as the protected “single” journey. The accepted 24271 journey is the original mounted `p2-transition-none-single` test in `tests/e2e/local/three-products.p2-tour.spec.ts`: `P2 mounted transition None single: raw clear preserves opaque data/order and guarded Undo`. Its gesture is `openCommandTimeline` → click `.clip-action[data-clip-id=<transitionClipId>]` → Effects tab → transition combobox → `None`; it asserts raw transition removal, opaque data/order preservation, reload, and guarded Undo. Gallery AddToTimeline is unrelated incoming UI and cannot receive credit for 24271.

## MAP-002 — changed mounted editor boundaries were omitted

The author map marks parent, bulk, P1, and popup unaffected and treats placement as editor-chrome-only. Actual mounted paths execute changed shared boundaries:

- Parent 16601 uses the P2 mounted single parent-move test and executes changed `TimelineCanvas` layout/tool-cluster boundaries.
- Single 24271 and bulk 27060 use the same mounted editor; the raw transition handler is unchanged, but the mounted canvas/shell boundaries are changed.
- Placement 9168 traverses `ShotTimelinePreview` → changed `TimelineEditorCore` → changed `TimelineCanvas`/`useTimelineState` → changed `useExternalDrop`; its file branch reaches unchanged `handleFileDrop` and `occurrence.add-media`.
- Popup 27026 mounts `ShotTimelinePreview`, which renders changed `TimelineEditorCore` when frame detail is shown. ADD/SWAP controls remain unchanged, but the shared editor boundary is executed.
- P1 32161 opens the mounted editor and executes changed canvas/shell boundaries during split and Timing-tab trim.
- RegisterAsset 10328 traverses changed `useTimelineState` → `useExternalDrop`; the image-file branch is retained while the removed text-tool branch is bypassed.
- P3 6447 directly exercises changed `AgentChat`, `TimelineCanvas`, shell, and render-control paths.

The exact per-ID map, changed hunks, source selectors, pin observations, and later-reproof applicability are in `affected-proofs.json`.

## Checks that passed

Elements source/test deletion matches the upstream deletion. Both meaningful AgentChat test blocks remain. The manifest retains local Runtime `95d98f...` and incoming Agent `e1c751...`; `runtime.lock.json` has no current delta. No test was weakened or newly added by this review.
