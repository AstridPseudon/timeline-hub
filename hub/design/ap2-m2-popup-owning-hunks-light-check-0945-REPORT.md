# HOME09:20 owning-hunk review — popup occurrence ADD

Verdict: **HOLD exact owning lines in `useAssetManagement.ts` and `useExternalDrop.ts`; do not approve candidate r46 as-is.** The candidate ref resolved successfully:

`6fcddfcb34a32e516e527160478ec1aa567ec1e9` (`tl/app-m2-popup-current-occurrence-source-frontier-r46`), parent `b030ca517c0867b6a56400e605d3b7f263d84a2a`.

Scope was limited to the two requested App2-owned files and their prepared-media neighbours. I did not review or requalify the unchanged parent implementation, and made no source edits.

## Exact holds

1. **Async refusal is accepted and the upload skeleton is removed too early.**

   Candidate `useAssetManagement.ts:401-443` starts `selectionPromise`, uses `void selectionPromise.then(...).catch(...)`, and returns `true` synchronously. A provider read, capture, `finish`, or `submit` refusal therefore still tells `handleFileDrop`/the caller that placement succeeded. The existing file-drop path then removes its transient skeleton immediately, while the occurrence command is still pending; `onTimelineDrop` may also seek as if the edit was accepted. This violates negative acceptance, await/intent, and skeleton lifetime/removal.

   Minimal correction: return the promise and resolve `true` only after capture/finish/submit succeeds; resolve `false` on the caught refusal after the visible toast. Keep the existing caller-owned skeleton cleanup so it runs after the awaited result.

2. **The occurrence row loses the prepared-media target's resolved time.**

   At `useAssetManagement.ts:363-376`, `previewPreparedMediaCommand` may snap the drop to an edge or choose a compatible track. At `useAssetManagement.ts:418-425`, the captured raw row uses `track: resolvedTrackId` but `at: time`, the original unsnapped request. The occurrence command can therefore write a different time from the visible preview. Use the preview clip's resolved authored `at` (and retain the resolved track) in the exact row; do not invent a second placement policy.

3. **The fallback selection read is not an owning-hunk-safe carrier and is not typed by the current parent.**

   `useAssetManagement.ts:343-400` accesses `runtime.provider.getProjectMediaSelection`, but the current `DataProvider` type exposed by `VideoEditorRuntimeContext` has no such member. This is a compile-time contract break in this hunk. More importantly, when `prepared.mediaSelection` is absent it performs a late catalog lookup after the target preview instead of refusing without the exact immutable selection carried at preparation. That can select/rebind a different source and violates exact selection/source preservation.

   Minimal correction: make the occurrence ADD seam require `prepared.mediaSelection`; if it is absent, visibly refuse before preview/capture. If a provider read is genuinely required, it needs an explicitly owned, typed carrier upstream and must be frozen before this hook's placement continuation; that is outside this light owning-hunk review and must not be improvised here.

4. **`useExternalDrop.ts` forwards a property to a function that does not accept it.**

   `useExternalDrop.ts:117-136` passes `occurrenceId` into the current parent `handleFileDrop` signature, which has no `occurrenceId` parameter. This is an excess-property/type error. The occurrence-aware `dropAsset` callback already closes over the port and occurrence identity in `useAssetManagement`, so this is also redundant overlap rather than a missing seam.

   Minimal correction: remove the `occurrenceId` forwarding and its now-unused `dispatchTimelineDrop` plumbing/dependency entries. Do not widen `external-drop-utils.ts` just to duplicate the closure-owned identity path.

5. **The early `current` guard changes the current parent prepared-video ADD behavior.**

   `useAssetManagement.ts:335-339` now refuses before the existing native prepared-video `commands.addClip` branch. The parent branch previously invoked its command service even when this local `dataRef` snapshot was unavailable; its own session/store is the owning source of current state. This copied guard belongs only to the occurrence preview and ordinary image placement paths.

   Minimal correction: leave the parent video ADD branch's existing entry behavior intact and obtain/check `current` only for the occurrence and existing local prepared-media paths.

## Owning hunks that otherwise fit

- The optional `clipId` added by `buildPlacePreparedMediaCommand` is compatible with the current parent prepared-media command and is unused by the ordinary parent path when omitted.
- `buildOccurrenceMediaAddRow` supplies the occurrence contract's reserved child identity, media alias, track, hold, and video source window shape. Its caller must use the resolved preview time and must not report success before the port submit completes.
- The explicit missing-port refusal and visible error in the occurrence branch are directionally correct. Keep that refusal before any occurrence placement capture.
- The occurrence owner/track references remain in the existing bound port/session seam; this review does not re-review the owner/epoch implementation outside these hunks.

## Evidence / commands

- `git show --stat --summary 6fcddfcb34a32e516e527160478ec1aa567ec1e9` — confirmed the exact 16-file, +950 candidate and parent.
- `git diff 6fcddfcb34a32e516e527160478ec1aa567ec1e9^ 6fcddfcb34a32e516e527160478ec1aa567ec1e9 -- src/tools/video-editor/hooks/useAssetManagement.ts src/tools/video-editor/hooks/useExternalDrop.ts` — reviewed only the requested owning hunks.
- Read-only parent-contract inspection confirmed `handleFileDrop` has no `occurrenceId` parameter and `DataProvider` has no `getProjectMediaSelection` member.
- No tests, browser/build/daemon/socket/full/install/actual/service runs were performed, per task. The candidate's provided prior `267` targeted-pass evidence was not rerun or requalified here.

## Next step

Return the candidate for the five minimal corrections above, then re-run the already-provided targeted evidence on the corrected source. This report does not qualify the candidate's actual behavior or any unchanged parent proof.
