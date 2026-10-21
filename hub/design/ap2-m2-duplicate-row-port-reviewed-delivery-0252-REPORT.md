# Duplicate row port report

## Result

Applied the safety-approved row-local duplicate-generation retention port.

Task-owned source changes are limited to:

- `src/tools/video-editor/adapters/app/generationLookup.ts`
- `src/tools/video-editor/hooks/useAssetManagement.ts`
- `src/tools/video-editor/components/AstridTimelineEditor.tsx`
- `src/tools/video-editor/components/AstridTimelineEditor.document-shots.test.tsx`

The port carries the original Runtime `MediaSelection`, captures and verifies the displayed timeline/head/projection and existing parent add-media preparation epoch across the producer await, preserves `afterClipId), and refuses without legacy registration when the native path cannot represent exact placement. No Provider/session/catalog operation, public DTO, endpoint, placement policy, activation behavior, or broad `duplicateIndependentShot` deletion was added.

## Forward/base state

- Safety-reviewed candidate: `1bac66b9d9efae15becd641ed338de3fb70152ad`, tree `543762374e7a3cfee004b29547f963d850ed89cb`.
- Candidate/base parent: `743d3464d1ed548986f29249bd9b4215baccf9bb`, tree `82a556ccb651d4a4c5ab4f1380394d0670f16568`.
- Current HOME `/home/user/work/app): `1be92c689c77efc3fe1d82eced116e86459139cf`, tree `25dae9904066fc0b92a6bfe3c50ab4c0ae2c6a4d). It is two commits ahead of the worker base.
- The two current-HOME forward files were carried byte-for-byte: `trackReorderCapture.ts` and `trackReorderCapture.test.ts).
- The provided merge-forward harness was attempted, but Git could not create `.git/worktrees/.../ORIG_HEAD.lock` because metadata is read-only in this sandbox. No direct Git metadata workaround was used. The final source is ready for the manager/harness to commit and submit; the final commit SHA is therefore pending harness commit.

## Live menu-path callers

`ClipAction.tsx:241-251` (Duplicate generation) -> `TimelineEditorCoreBody.tsx:807` -> `TimelineEditorCore.tsx:839` -> `AstridTimelineEditor.tsx:544-625` -> `generation-utils.ts` / `generationLookup.ts` -> `useAssetManagement.prepareGenerationAsset` -> `useTimelineCommandsService.addClip` -> existing `parentClipAddMedia` capture/verify/submit carrier.

This path no longer calls `planGenerationAssetRegistration`, `registerGenerationAsset`, `patchRegistry`, or a composition publish writer. Other distinct flows still have registration callers, including external drop and pinned-shot-group synchronization; they were intentionally left unchanged.

## Checks

- `./node_modules/.bin/vitest run --no-cache --config config/testing/vitest.config.ts src/tools/video-editor/components/AstridTimelineEditor.document-shots.test.tsx` — passed, 1 file / 11 tests.
- `./node_modules/.bin/vitest run --no-cache --config config/testing/vitest.config.ts src/tools/video-editor/commands/trackReorderCapture.test.ts` — passed, 1 file / 8 tests.
- `git diff --check` — passed.
- The safety review independently verified the exact candidate with 26 focused tests, four-file ESLint, TypeScript no-emit, and diff checks; those were not rerun after the source-only forward because the task forbids unchanged requalification.
- Not run: full suite, browser, localhost/live sockets, central mounted gate, external catalog/provider acceptance, or actual accepted duplication.

## Acceptance boundary

Main still refuses `duplicateGenerationAsset` through the unavailable catalog adapter, and native prepared parent media explicitly refuses `afterClipId`. This source port does not claim accepted duplication, native exact placement, reload/undo, retry, or deletion of the broader parent/duplicate-independent-shot path. The next required work is an approved real catalog producer returning the original Runtime selection plus HOME-owned exact-placement support (or an intentional continued refusal), followed by the central mounted gate.

