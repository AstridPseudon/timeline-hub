# AP2-M2 parent25174 Main-coordinate reconciliation

## Decision

Upstream Main also centers an external file drop. The parent25174 failure was
therefore a fixture-coordinate mismatch, not a current-production regression.
Production remains unchanged, including the independently valid reordered-row
planner correction. The smallest justified correction is row-local: the
mounted File-drop fixture now sends pointer-time `22.5`, so Main's default
five-second centered preview resolves the original desired left edge at `20`.

## Main/current evidence

This App worktree has no `origin/main` ref; its configured remote is `hub`.
The App refresh merge `fbd184674e158034001bb8f88e94a9fa46c53339` records
upstream Main as parent `83717af0c756ed3d4cf12a744f648849f3d1b153`, which was
inspected directly. Main has no `getDropPosition` symbol; the equivalent path
is `computeDropPosition`.

- Main `src/tools/video-editor/hooks/useExternalDrop.ts:550-601` records raw
  external `event.clientX/clientY` during File drag-over and passes them to the
  coordinator.
- Main `src/tools/video-editor/lib/external-drop-utils.ts:813-827` refreshes
  from those raw coordinates on finalization, or uses the drop event's raw
  coordinates as fallback.
- Main `src/tools/video-editor/hooks/useDragCoordinator.ts:138-170` forwards
  `clipOffsetX` only when a caller supplies it.
- Main `src/tools/video-editor/lib/drop-position.ts:106-131` defaults
  `clipDuration` to `5`, computes
  `effectiveOffsetX = (clipDuration * pixelsPerSecond) / 2` when
  `clipOffsetX` is absent, then subtracts that offset before converting the
  pointer coordinate to time.
- Main `src/tools/video-editor/hooks/useClipDrag.ts:198-207` supplies
  `session.pointerOffsetX` for internal clip drags. This preserves the direct
  neighbour internal-drag semantics and is distinct from external File drops.

Current integration has the same external coordinate semantics at
`src/tools/video-editor/hooks/useExternalDrop.ts:550-599`,
`src/tools/video-editor/lib/external-drop-utils.ts:844-858`, and
`src/tools/video-editor/lib/drop-position.ts:106-131`. The current-vs-Main
`drop-position.ts` delta is only the rendered-track/row alignment correction;
there is no coordinate-offset change.

The shared fixture helper at `tests/e2e/local/support/app.ts:212-235` converts
its `time` argument directly to `clientX` (`box.x + (time - from) *
pixelsPerSecond`); it does not claim that the argument is a clip left edge.
Thus the original `20` call encoded a pointer at 20, which Main resolves to
17.5. With V1 occupied at 15–18, that overlaps V1 and the existing planner
correctly reroutes to free S1 before the native occurrence guard refuses.

## Change

Changed only `tests/e2e/local/three-products.spec.ts:1471,1487`:

```ts
const manualDropPointerAt = 22.5;
await dropFileOnTimeline(/* unchanged real File-drop inputs */, manualDropPointerAt);
```

The exact original assertions remain: the positive native row is expected at
`track: V1`, `at: 20`, `clipType: media`, with collision/opaque-data/native
fence/wire assertions intact. No production helper, shared support helper,
Runtime/Agent wire, budget, or native guard was changed.

The shared support helper is HOME-owned. A future tiny clarity-only proposal
for its owner is to rename the final parameter from `time` to `pointerTime`
(or add an explicit left-edge parameter); no shared-helper edit was made here.

## Evidence

- Transported the retained report byte-identically from
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/design/ap2-m2-parent25174-first-causal-boundary-0923-REPORT.md`
  to this directory.
- SHA-256 source and destination: `911ea703135bb7b063f601ce1ca40b43600f8f2f42c85d6bb55ad33f22e95ebf`.
- `git diff --check`: passed.
- Browser, build, daemon/socket, actual mounted journey, full suite, install,
  and central test service: not run, per task instruction.

## Next action

The App manager should review/merge this fixture-only coordinate correction.
The HOME owner may clarify the shared helper's pointer-time contract later;
no production coordinate correction is warranted by parent25174.
