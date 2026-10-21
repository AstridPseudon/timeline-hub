# Independent data-safety review: local skeleton/native handoff

## Verdict

Approved for the stated data-safety scope at exact candidate commit `3d51980514826bea7617bc61f587f6a60344b562`, tree `66ceb1ff5bd19df64d600e5332228466dab1fb7a`.

The candidate is four App source/test files and introduces no store, DTO, API, writer, private operation, bootstrap, pin, or type-bypass surface. No product files were changed in this review worktree.

## Safety review

- `isTransientUploadPlaceholder` in `src/tools/video-editor/lib/external-drop-utils.ts:132` accepts a skeleton only when all local facts agree: `uploading-*` ID, `uploading:` metadata asset, a live row action, and no authored `config.clips` or `clipOrder` identity. Main's `buildTrackClipOrder` does not add a newly inserted skeleton ID, so this remains true through the existing local skeleton lifecycle.
- `useAssetManagement.ts:300` omits `removeClipId` only for that proven placeholder. A missing current snapshot is not proof of a placeholder, so the existing removal intent is retained there; authored or otherwise unproven IDs still reach the original native guard.
- Native ADD's existing prepared-media guard still refuses any `removeClipId`; the authored-row regression sends `clip-authored`, returns false, shows the native refusal, and verifies the authored row remains. There is no local snapshot fallback or hidden overwrite.
- `handleFileDrop` cleanup at `external-drop-utils.ts:480` re-reads the latest `dataRef`, removes only the still-proven skeleton, and runs after accepted or refused image/video/generic placement. Upload rejection/cancel follows the existing catch/finally path, removes only that skeleton, decrements `pendingOpsRef`, and does not seek after refusal.
- If a newer edit, remote reload, selection change, or native verification epoch changes the displayed state, the existing command-session wrapper and native port fences reject stale capture/finish/submit. Cleanup then either removes the still-local skeleton from current rows or leaves changed/authored rows untouched. The row cleanup is ID-local and preserves all other latest rows.
- Existing native command guards, provider/session checks, exact selection checks, and the wrong-selection `404/409` assertion were not edited. Other prepared-media callers retain their existing semantics: `useSwitchToFinalVideo.ts`, `useAddVariantAsGeneration.ts`, and `AstridTimelineEditor.tsx` remain unchanged.

## RED -> GREEN evidence

The prior Actual13951 diagnosis recorded the real failure: an external video drop forwarded its non-persisted skeleton ID as `removeClipId`, so native ADD refused before verified selection/commit. The candidate adds the corresponding positive handoff regression and the authored replacement negative; both pass below.

## Live callers

- `src/tools/video-editor/lib/external-drop-utils.ts:handleFileDrop` — image/video/generic prepared file-drop upload and cleanup path; image/video passes the skeleton ID through the existing `dropAsset` argument.
- `src/tools/video-editor/hooks/useAssetManagement.ts:placePreparedAsset` — shared prepared-video native `commands.addClip` caller where the row-local omission is made.
- `src/tools/video-editor/hooks/useExternalDrop.ts:onTimelineDrop` is the live event adapter into `handleFileDrop`.
- Native prepared-media callers not changed: `useSwitchToFinalVideo.ts`, `useAddVariantAsGeneration.ts`, `AstridTimelineEditor.tsx`.

## Tests and checks

All commands below were run against an isolated archived checkout of the exact candidate tree, with a private Vite cache; shared dependencies remained read-only.

- `node_modules/.bin/vitest run --config config/testing/vitest.review.config.ts --no-file-parallelism src/tools/video-editor/hooks/useAssetManagement.mediaImport.test.tsx src/tools/video-editor/hooks/useExternalDrop.test.tsx src/tools/video-editor/hooks/useAssetManagement.assetDrop.test.ts src/tools/video-editor/hooks/useTimelineHistory.remote-boundary.test.tsx` — **passed, 4 files / 52 tests**.
- `node_modules/.bin/eslint src/tools/video-editor/hooks/useAssetManagement.ts src/tools/video-editor/hooks/useAssetManagement.mediaImport.test.tsx src/tools/video-editor/lib/external-drop-utils.ts src/tools/video-editor/hooks/useExternalDrop.test.tsx --max-warnings 0` — **passed**.
- `node_modules/.bin/tsc --noEmit --pretty false --project tsconfig.json` — **passed**.
- `git diff --check c45cc175a62701593af4ec2503467d681ec9c2f7 3d51980514826bea7617bc61f587f6a60344b562` — **passed**.

Not run by instruction: browser, HTTP/localhost/live sockets, full suites, or replay of the original journey.

## Decisions and blockers

No deviation from PLAN and no blocker. The literal top-level `STATUS.md` and `INBOX.md` paths were absent; I used the supplied worker brief, current App integration status, candidate report, and diagnosis report instead. The review worktree is clean.
