# Parent duplicate-generation source retention triage

## Verdict

Proposal0232 inspected the current `743d3464d` integration tree, but the
reported missing `MediaSelection` propagation was caused by an approved
row-local source hunk being absent from that tree. It was not evidence that
the reviewed producer design was wrong. The shared preparation/session epoch
carrier from `767fcce2b` is present in current; the row-local selection and
native-consumer hunk from `50b8ed25e` was not.

The second finding is real and independent: Main's existing catalog adapter
still has no accepted duplicate-generation operation or catalog carrier. The
current adapter remains a visible `bridgeCapabilityUnavailable` refusal. No
normal accepted catalog gesture is possible on this tree. This is distinct
from a remaining film/timeline snapshot writer.

## Source comparison

- Current base: `743d3464d` (`hub/timeline/app/tl/integration`).
- Approved donor: `50b8ed25ef37122cd11b6265eadf0fa91be64541`, which adds the
  original Runtime `MediaSelection` type/carrier, producer-await head fences,
  `prepareGenerationAsset` use, and focused editor assertions.
- Approved epoch donor: `767fcce2b26f20686c7f10ae5d9d94b81bea7c07`, whose shared
  `commitSession` and `useTimelineCommandSession` preparation API is already
  present in current (`commitSession.ts:60-73,367-383` and
  `useTimelineCommandSession.ts:271-284`).
- Current `0d5009e18` parent preparation-selection join only carries
  `mediaImport.mediaSelection`; it does not restore the duplicate-generation
  result field or handler path.
- `50b8ed25e` is not an ancestor of `743d3464d`; the current first-parent
  history contains the HOME joins but not that donor's row-local source.

## Change made

Ported only the owned row-local donor hunk:

- `src/tools/video-editor/adapters/app/generationLookup.ts:1-14` now types the
  optional immutable `MediaSelection` on a duplicated result. The adapter's
  existing refusal is unchanged.
- `src/tools/video-editor/hooks/useAssetManagement.ts:41-46,250-259` carries
  that selection through `prepareGenerationAsset`, preserving existing
  `mediaImport` behavior.
- `src/tools/video-editor/components/AstridTimelineEditor.tsx:544-625` now:
  - captures the displayed timeline snapshot and the existing shared
    `parentClipAddMedia.prepare()` basis before the producer await;
  - refuses changed display/head/projection or session epoch/basis;
  - prepares the producer result with its original selection;
  - submits exactly one existing `commands.addClip({ preparedAsset,
    afterClipId })` intent;
  - refuses visibly if the producer result has no original selection;
  - never calls `registerGenerationAsset` or the old registration planner.
- `AstridTimelineEditor.document-shots.test.tsx` retains all existing
  assertions and adds focused coverage for selection propagation/no legacy
  registration, changed displayed head, changed native preparation epoch, and
  exact-placement refusal.

No Provider, command-session, Runtime, endpoint, DTO, catalog, timing, or
shared-file edit was made.

## Handler and fallback trace

The live duplicate-generation path is:

`ClipAction.tsx:241-251` (`Duplicate generation`) ->
`TimelineEditorCoreBody.tsx:807` -> `TimelineEditorCore.tsx:839` ->
`AstridTimelineEditor.tsx:544` ->
`generation-utils.ts`/`generationLookup.ts:17` ->
`useAssetManagement.prepareGenerationAsset` ->
`useTimelineCommandsService.addClip` -> existing
`parentClipAddMedia` capture/verify/submit.

The prepared fallback at `useTimelineCommandsService.ts:475-540` accepts only
video, requires a Runtime selection and a non-negative `time`, and explicitly
refuses `afterClipId` at lines 481-484. The handler preserves the requested
exact-after-clip shape; it does not guess an insertion time or convert to
append. Therefore the current real result, if supplied, still produces a
visible exact-placement refusal until the existing native carrier supports
that placement.

The shared current carrier is wired through
`useTimelineState.ts:1255-1265` -> `VideoEditorProvider.tsx:747-752` and the
session wrapper at `useTimelineCommandSession.ts:271-284`. Those are HOME-owned
and were not edited.

## Legacy-writer reachability

For this specific `Duplicate generation` menu gesture, no legacy snapshot
writer remains reachable after this port: the handler does not call
`registerGenerationAsset`, `patchRegistry`, `planGenerationAssetRegistration`,
or any `publish`/composition writer. If the adapter refuses, the handler
stops before preparation. If a real result lacks the original selection, it
stops before `addClip`. If exact placement is unsupported, the existing native
command returns a visible refusal without a fallback writer.

Other, distinct flows still have registration callers, including pinned shot
group synchronization and `useAddVariantAsGeneration.ts`; those are not the
`Duplicate generation` context-menu gesture and were not broadened or retired
by this task.

## HOME seam request

Please retain the current shared `parentClipAddMedia` Provider/session
forwarding while joining this row-local port. If the accepted catalog producer
is later supplied, HOME must either add exact `afterClipId` support to the
existing native parent-media carrier or preserve the current visible refusal.
Do not translate this gesture to guessed append/time placement, add a new
catalog endpoint/DTO/authority, or edit shared Provider/session files in this
row.

## Evidence

- `./node_modules/.bin/vitest run --no-cache --config config/testing/vitest.config.ts src/tools/video-editor/components/AstridTimelineEditor.document-shots.test.tsx src/tools/video-editor/hooks/useAssetManagement.mediaImport.test.tsx src/tools/video-editor/commands/parentClipAddCapture.test.ts`
  — **3 files, 26 tests passed**.
- `./node_modules/.bin/eslint src/tools/video-editor/adapters/app/generationLookup.ts src/tools/video-editor/hooks/useAssetManagement.ts src/tools/video-editor/components/AstridTimelineEditor.tsx src/tools/video-editor/components/AstridTimelineEditor.document-shots.test.tsx --report-unused-disable-directives --max-warnings 0`
  — **passed**.
- `./node_modules/.bin/tsc --noEmit --pretty false` — **passed**.
- `git diff --check` — **passed**.

Not run: browser, localhost/live socket, central mounted gate, full suite,
catalog/external-provider test, or actual accepted duplicate. No accepted
workflow, placement, reload/undo, retry, or writer-deletion claim is made.

## Recommended next step

Keep the duplicate row open. The next prerequisite is an approved real catalog
producer/fixture that returns the original five-field Runtime selection,
followed by HOME-owned exact placement support and one central mounted run.
Do not close the broad parent row from this source-only port.
