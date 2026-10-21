# App automatic-placement qualified cut frontier

Date: 2026-10-21 UTC  
Scope: one bounded D01 automatic-placement cut; source audit only.  
App source audited: `df4c86b08c390db932b19cac3d1ad36fb55b6f15` (`tl/integration` at this worker), with `02ac224cd3c0d376f08b6129f58ded624f3e400d` (`guard initial placement admission across requester wakes`) confirmed as an ancestor.  
Existing ledger row: `D01-app-placement` in the App deletion ledger blob `e0df0332c21658bd871c5f9422c597fb0019ae67`.

## Verdict

No deletion hunk is qualified or prepared. The exact legacy `undefined` auto-position branch is still entered by live manual/catalog callers, so removing it would remove behavior outside the native generated-task replacement. The D01 row remains **in-progress** and the placement writer remains retained.

This is a bounded blocker, not a claim that the native path is absent. The native generated-task path and the legacy path are separate today; the legacy branch is shared below the caller boundary.

## Native replacement traced

The current native requester/session path is:

1. `src/tools/video-editor/commands/commitSession.ts:227-228` creates `createSessionPlacementRequester` on the current Runtime operation and the existing command outbox.
2. `src/tools/video-editor/commands/editorImagePlacement.ts:41-124` requires the explicit raw occurrence/lane, stores the original head/read closure, auto-approval policy, owner/anchor/fallback, and reserved clip ID, and reserves the exact normal task body/key before admission.
3. `src/tools/video-editor/commands/placementRequester.ts:212-249` resumes the saved task, requires the succeeded task and selected output, reads managed outputs and the five-field media selection, then invokes the requester capture with the saved scope and lifecycle checks.
4. `src/tools/video-editor/commands/nativePlacementCapture.ts:24-72` reads the original saved document, verifies the saved policy/bindings and exact media pin, and returns the existing native command payload.
5. `src/tools/video-editor/commands/sessionPlacement.ts:9-29` accepts only the native `placement.create` or image `occurrence.add-media` result and links it to the ordinary session payload. `commitSession.ts:214-228` transmits that placement through the pinned operation's normal commit path.

The existing original actual that demonstrates this replacement is:
`tests/e2e/local/auto-real-proxy.spec.ts:311-506`, test
`real operation proxy automatic image placement survives reconnect, lost ACK retry, reload and guarded undo`.
Its existing assertion at `:500` requires `legacy` to be empty, while `:501-505` requires task, managed-output, verified-media-selection, and commit operation traffic. This source was not run in this audit because the task explicitly forbids browser/actual qualification; therefore no new pass is claimed here.

## Legacy branch and exact blockers

The bounded candidate is the `timelineFrame === undefined` branch in
`src/shared/lib/placement/documentPlacement.ts:242-248`, reached through
`src/shared/lib/placement/placementService.ts:172-190`. It appends after the
last occupied clip. It is not a generated-task requester branch, and the
native requester does not call it.

It nevertheless has live callers that use the same branch:

- `src/shared/hooks/shots/useShotGenerationMutations.ts:344-370`,
  `usePositionExistingGenerationInShot`, calls `placeGeneration` without
  `timelineFrame`. `src/tools/image-generation/hooks/useImageGenActions.ts:75-85`
  selects this path for an existing unpositioned catalog generation. This is
  the exact manual/catalog caller preventing deletion of the undefined branch.
- `src/shared/hooks/shots/addImageToShotHelpers.ts:31-55` forwards its optional
  `timelineFrame` to `placeGeneration`. Its default positioned callers omit
  the field: `src/features/tasks/components/TasksPane/hooks/useShotActions.ts:55-86`
  and the positioned branch at
  `src/tools/image-generation/hooks/useImageGenActions.ts:86-93`; those enter
  the same undefined auto-position branch. The travel-image drop path also
  reaches this helper with no frame at
  `src/tools/travel-between-images/hooks/workflow/useVideoTravelDropHandlers.ts:135-141`.
- `src/shared/components/ImageGenerationForm/hooks/legacyMigrations/useGenerationBackfillMigration.ts:119-123`
  and `src/shared/components/ImageGenerationForm/hooks/referenceUpload/referenceDomainService.ts:252-256`
  call `placeGeneration` without a frame as migration/reference-upload
  placement. They are not native generated-task approval consumers.

The same `placeGeneration` service also owns pooled/manual behavior: the
`timelineFrame: null` path in `documentPlacement.ts:237-240`, plus
`unplaceGeneration`'s pooled restoration at
`placementService.ts:208-223`, and explicit frame/batch promotion through
`batchUpdatePlacementFrames`. Therefore deleting the whole service or its
legacy CAS target would also cut pooled and explicit/manual/catalog consumers;
the task's no-refactor/no-invented-coverage boundary rules out doing that here.

## Required next qualification

First qualify the existing actual above on the approved current App/Agent/Runtime
tuple. Then separately migrate or retire the exact manual/catalog callers listed
above (including pooled and explicit-frame behavior) before deleting either the
shared `placeGeneration` service or the `undefined` branch. Until that caller
boundary is removed, the existing D01 ledger row should stay open. No
unapplied deletion hunk is supplied because the indivisible branch still has
live callers.

## Commands and limits

Read-only commands used:

```text
sed/rg/nl over PLAN.md, the current App sources, placement callers, and native requester/session files
git merge-base --is-ancestor 02ac224cd HEAD  # exit 0
git show -s --format='%H %T %s' 02ac224cd HEAD
git cat-file -p e0df0332c21658bd871c5f9422c597fb0019ae67
```

No product files, tests, branches, refs, dependencies, caches, or shared
worktrees were changed. No unit/browser/actual/full/build/install/graph suite
was run; no requalification of the unchanged `209` evidence was attempted.
