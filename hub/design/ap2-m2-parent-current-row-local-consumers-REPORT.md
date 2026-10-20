# AP2-M2 parent current row-local consumers

## Result

Ported the current-source row-local consumer delta onto
`tl/ap2-m2-parent-current-shared-packet` at `f7e4f762fed1e92069652f048f61f7efd806466a`.

Changed only the approved App consumer/state/test surface:

- `src/tools/video-editor/adapters/app/generationLookup.ts`
  - Carries the immutable Runtime `MediaSelection` on duplicated-generation results.
- `src/tools/video-editor/hooks/useAssetManagement.ts`
  - Forwards a caller-supplied original selection into prepared generation assets,
    retaining media-import selection fallback.
- `src/tools/video-editor/components/AstridTimelineEditor.tsx`
  - Uses the prepared native asset path for generation duplication instead of
    registering a legacy catalog asset.
  - Captures document identity/signatures/head/projection and the existing
    parent-add session preparation before the duplication await.
  - Refuses stale document/session results before preparation or enqueue, keeps
    the raw `afterClipId` carrier, and preserves the visible exact-placement
    refusal in the current command service.
  - Supplies final-video preparation with the existing swap preparation fence.
- `src/tools/video-editor/hooks/useSwitchToFinalVideo.ts`
  - Freezes final-video selection before preparation, preserves the target
    fingerprint, and forwards original Runtime selection from media import to
    the native replacement attempt.
  - A missing original selection or stale preparation is refused visibly.
- `src/tools/video-editor/hooks/useTimelineState.types.ts` and
  `useTimelineState.ts`
  - Mount the current shared packet's preparation-only swap carrier into the
    editor ops surface.
- `src/tools/video-editor/components/AstridTimelineEditor.document-shots.test.tsx`
  - Adds success, stale-head, and stale-session-generation coverage for native
    generation duplication; verifies no legacy registry write.

No `commitSession.ts`, `useTimelineCommandSession.ts`, Provider/dataProvider,
Runtime door, outbox, or `useTimelineOps` core files were edited.

## Source map and current-source harness candidate

The candidate source is this worktree branch:

```text
tl/ap2-m2-parent-current-row-local-consumers
base: tl/ap2-m2-parent-current-shared-packet
base tip: f7e4f762fed1e92069652f048f61f7efd806466a
donor reference: tl/ap2-m2-parent-new-ports-current-delta-packet
donor native commits: 9f98fb702, f71dcd2b5, ab429f33c
```

The donor's add-media consumer behavior was adapted from `ab429f33c` and its
final-video preparation behavior from `f71dcd2b5`. The current shared packet's
preparation fences are consumed as-is.

## Settled-boundary blocker

The exact donor's native replacement service branch requires
`ParentClipSwapMediaCapturePort` with `capture`, `finish`, and `submit`, plus
`parentClipSwapCapture.ts` and the swap executor additions to
`parentClipAddCapture.ts`. The current shared packet instead exports only
`ParentClipSwapMediaPreparationPort` (`prepare` and
`assertPreparationCurrent`) from `commitSession.ts`, and the current tree has
no swap capture helper. The task explicitly forbids editing the command-session
files and limits this worker to row-local consumers/state mounts/direct tests.

Therefore this candidate does not fabricate a swap producer or silently fall
back to append: the final-video native replacement attempt reaches the existing
visible `replaceClipId` refusal until App lands the separate shared producer
adapter. This is a real integration blocker, not an unverified claim.

Required follow-up shared patch, owned by App:

1. Extend the shared command-session carrier with the reviewed swap
   capture/finish/submit port and preserve its legacy-clean fence.
2. Land the reviewed `parentClipSwapCapture.ts` plus the current-root swap
   executor/helper delta.
3. Update `useTimelineCommandsService` to consume the detached original
   selection for native swap, while retaining raw `afterClipId` refusal.
4. Resolve the `useTimelineState` mount conflict by preserving this exact
   preparation mount and the full capture port together.

Merge order is shared packet first, then this row-local candidate, then the
App-owned shared swap producer adapter. No legacy row retirement or fallback
activation is claimed here.

## Verification

Passed:

```text
node node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/components/AstridTimelineEditor.document-shots.test.tsx src/tools/video-editor/hooks/useAssetManagement.mediaImport.test.tsx src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx src/tools/video-editor/hooks/useTimelineCommandSession.projection.test.tsx
→ 4 files / 62 tests passed

node node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/commands/parentClipAddCapture.test.ts src/tools/video-editor/commands/commitSession.test.ts src/tools/video-editor/contexts/VideoEditorProvider.test.tsx src/tools/video-editor/hooks/useTimelineState.history-authority.test.tsx src/tools/video-editor/hooks/useTimelineState.visual-seam.test.ts src/tools/video-editor/hooks/useAssetManagement.mediaImport.test.tsx
→ 6 files / 164 tests passed

./node_modules/.bin/eslint --no-cache --max-warnings 0 src/tools/video-editor/adapters/app/generationLookup.ts src/tools/video-editor/hooks/useAssetManagement.ts src/tools/video-editor/hooks/useTimelineState.types.ts src/tools/video-editor/hooks/useTimelineState.ts src/tools/video-editor/hooks/useSwitchToFinalVideo.ts src/tools/video-editor/components/AstridTimelineEditor.tsx src/tools/video-editor/components/AstridTimelineEditor.document-shots.test.tsx
→ passed

git diff --check
→ passed
```

The locked project typecheck was run:

```text
./node_modules/.bin/tsc -p tsconfig.app.json --noEmit --pretty false
→ exit 2, existing current-root baseline only
```

Its diagnostics are the known Composition package export/type failures in
preview/audio/render files and `lib/config-utils.ts`; no diagnostic points at
the changed consumer/state files.

Not run: full suite, browser/e2e, localhost/live sockets, dependency/pin
changes, or external-provider qualification.

## Status

Blocked only on the missing shared swap capture/finish/submit carrier described
above. The add/generation consumer candidate is source-verified and targeted
green; do not mark the whole parent-media native swap task complete until the
App-owned shared adapter is merged and its direct replacement tests pass.
