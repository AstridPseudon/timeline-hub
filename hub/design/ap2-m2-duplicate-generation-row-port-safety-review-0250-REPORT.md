# Duplicate-generation row-local source review

## Verdict

Approve `1bac66b9d9efae15becd641ed338de3fb70152ad` for the exact source-only,
row-local scope. Its tree is
`543762374e7a3cfee004b29547f963d850ed89cb`. It is based directly on HOME
`743d3464d1ed548986f29249bd9b4215baccf9bb` (tree
`82a556ccb651d4a4c5ab4f1380394d0670f16568`) and changes exactly these four
files:

- `src/tools/video-editor/adapters/app/generationLookup.ts`
- `src/tools/video-editor/hooks/useAssetManagement.ts`
- `src/tools/video-editor/components/AstridTimelineEditor.tsx`
- `src/tools/video-editor/components/AstridTimelineEditor.document-shots.test.tsx`

The candidate restores the row-local portion of approved donor
`50b8ed25ef37122cd11b6265eadf0fa91be64541` (tree
`10d13a26dafb50c44ef16d623b52d57c784f415b`) while retaining the shared
preparation/session epoch carrier from `767fcce2b26f20686c7f10ae5d9d94b81bea7c07`
(tree `65fe7c4020b62ba329b7b31839e8e44c67ba59b5`). The prior proposal had
inspected the current HOME tree, where the donor's row-local hunk was absent;
this was a dropped source hunk, not evidence that the reviewed design was
wrong.

## Source correctness

The candidate preserves the immutable five-field Runtime `MediaSelection`
from the duplication result through `prepareGenerationAsset` and into the
single prepared-media `addClip` intent. It captures the displayed data
identity/signatures, head, projection, and the existing shared
`parentClipAddMedia.prepare()` basis before the producer await. After the
await it refuses if displayed data/head/projection or the shared session
epoch/basis changed. It does not recapture a newer selection, invent one, or
use a mutable catalog lookup as authority.

The handler passes `afterClipId` unchanged. It supplies no guessed time and no
append fallback. In the current native command service, a prepared asset with
`mediaSelection` takes the native branch, where `afterClipId` is explicitly
refused before time/placement preparation. The candidate surfaces that refusal
and does not route to the old registered-asset path.

The Main catalog adapter still visibly refuses: `duplicateGenerationAsset`
throws the existing `bridgeCapabilityUnavailable` error. Therefore this
candidate does not qualify an accepted catalog duplication workflow, native
exact placement, reload/undo, retry, or a mounted/browser journey.

No Runtime/App DTO, endpoint, catalog authority, Provider/session implementation,
timing, or `duplicateIndependentShot` deletion was added. The shared Provider
and session carrier remains HOME-owned and is only consumed by this row-local
port.

## Menu-path callers and legacy reachability

The live menu path is:

`ClipAction.tsx:241-251` (`Duplicate generation`) ->
`TimelineEditorCoreBody.tsx:807` -> `TimelineEditorCore.tsx:839` ->
`AstridTimelineEditor.tsx:544-625` -> `generation-utils.ts` /
`generationLookup.ts` -> `useAssetManagement.prepareGenerationAsset` ->
`useTimelineCommandsService.addClip` -> the existing `parentClipAddMedia`
capture/verify/submit carrier.

For this specific menu path, the candidate no longer calls
`planGenerationAssetRegistration`, `registerGenerationAsset`, `patchRegistry`,
or any composition `publish` writer. If the adapter refuses, if the result
has no original selection, or if exact placement is unsupported, the handler
stops with a visible refusal. Other distinct flows still have registration
callers, including pinned-shot-group synchronization and
`useAddVariantAsGeneration.ts`; this review does not broaden their deletion.

## HOME applicability and limits

The current HOME worktree is `tl/integration` at
`743d3464d1ed548986f29249bd9b4215baccf9bb`; `808ef7ebf` is an ancestor of
that tree. HOME also has pre-existing untracked vendor symlinks, which this
review did not touch. The candidate is therefore applicable as a small
forward port onto current HOME, subject to the normal HOME merge/join process;
it is not already in HOME.

The current acceptance boundary remains unchanged: Main has no accepted
generation-duplication catalog producer/fixture, and native prepared parent
media explicitly refuses `afterClipId`. Keep the duplicate row open. The next
step is an approved real catalog producer returning the original Runtime
selection, followed by HOME-owned exact placement support or an intentional
continued refusal, then one central mounted gate. Do not claim accepted
catalog/native placement or close the broad parent/duplicate row from this
source-only review.

## Evidence

On an isolated temporary materialization of candidate `1bac66b9d` with the
shared App `node_modules` symlinked read-only:

- `./node_modules/.bin/vitest run --no-cache --config config/testing/vitest.config.ts src/tools/video-editor/components/AstridTimelineEditor.document-shots.test.tsx src/tools/video-editor/hooks/useAssetManagement.mediaImport.test.tsx src/tools/video-editor/commands/parentClipAddCapture.test` — **3 files, 26 tests passed**.
- `./node_modules/.bin/eslint src/tools/video-editor/adapters/app/generationLookup.ts src/tools/video-editor/hooks/useAssetManagement.ts src/tools/video-editor/components/AstridTimelineEditor.tsx src/tools/video-editor/components/AstridTimelineEditor.document-shots.test.tsx --report-unused-disable-directives --max-warnings 0` — **passed**.
- `./node_modules/.bin/tsc --noEmit --pretty false` — **passed**.
- `git diff --check 743d3464d..1bac66b9d` and `git show --check 1bac66b9d` — **passed**.
- Candidate-to-HOME changed-file count — **4**, with no assertion deletions in the document-shots test.

Not run: browser, localhost/live socket, central mounted gate, full suite,
external catalog/provider tests, or actual accepted duplication. No acceptance
or deletion claim is made.
