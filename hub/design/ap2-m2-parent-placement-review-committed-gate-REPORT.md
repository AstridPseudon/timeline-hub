# Parent placement committed-gate review

## Decision

**Blocked; no parent gate was requested.** The required locked-graph reproduction did
not pass. Its wrapper returned exit 2 because the exact locked graph App tree failed
TypeScript compilation. The ordinary graph probe returned 0, but the wrapper exits on
the TypeScript failure, so there is no safe graph proof on which to authorize the one
parent gate.

The required lead report
`design/ap2-m2-locked-graph-wrapper-owner-rerun-REPORT.md` was not present when this
review completed. The central result is retained and is sufficient to identify the
blocker:

- Suite: `app-ap2-m2-locked-graph-wrapper-owner-rerun-integration-1020214324-22557`
- Command registered by the lead: `bin/request-test integration:app ap2-m2-locked-graph-wrapper-owner-rerun-integration --no-cache`, followed by `wait-test`
- Source tree reported by the central service: `d6aa0af87d200c19f2b53a412d634f1ff716367e`
- Wrapper result: exit `2` after 63 seconds; `tsc_status=2`, `ordinary_probe_status=0`
- Archive guard: source SHA `895c628ab0727c8975247310fd0319b0f546a8d032a57072c9e364e20965ca30`
- The wrapper's exact TypeScript errors are in the central log. They are in
  `elementCapture.ts`, `elementGesture.ts`, `genericPatchCapture.ts`,
  `occurrenceDuplicateCapture.ts`, and `AstridElementParams.tsx` (nullable/undefined
  arguments, JSON narrowing, and readonly `clear` typing).

Therefore I did **not** call `bin/request-test ap2-m2-parent-positive-real-causal-repair`
and did not run the old parent-drop target or any full/local browser/socket suite.

## Read-only delta review

Reviewed commit `54c145906` (`fix(timeline): preserve native drop position and
surface refusals`) against base `9de0e009f5c50d45de402727b8eb889ee4cb7199`.
The delta is five files only; this worktree remains clean and no source was edited.

- `useTimelineCommandsService.ts` plans against a shallow placement copy with
  `uploading-*` display actions removed, while `port.capture` still receives the
  original `current`. The detached native row retains its source window and adds
  only the native `hold` carrier. Existing media-selection, mounted-session,
  target-time, row-shape, and native capture/finish/submit guards remain present.
- `useAssetManagement.ts` still returns the native refusal and does not call the
  fallback writer or `applyEdit`; it now surfaces the refusal message through the
  existing error toast. The focused refusal test checks the original data remains
  unchanged and the toast is emitted.
- The added service test covers both placeholder-present and placeholder-absent
  cases, checks the requested position (`at: 20`), checks the native row shape and
  `hold`, and confirms the displayed current data is unchanged.
- `three-products.spec.ts` now requires the verified selection response to be HTTP
  200 and its body selection to equal the ordinary selection. The request observer
  increments `attempts` before `route.fetch`; `posts` is appended only after fetch
  and JSON decoding. The positive path checks `attempts === 1` and one completed
  post before deliberately losing that response, then checks exact retry bytes/key
  after reload/runtime restart. This keeps sent-request evidence distinct from
  response counting under intentional lost ACK.
- The negative refusal, original head/history, retry/reload/recovery, undo,
  opaque-data, and zero-legacy-save assertions remain in place. No silent fallback,
  partial local save, selection/owner/head/epoch/range/draft/skeleton guard, or
  no-double-write assertion was removed or weakened in this delta.

The new diagnostic fields (`alerts`, session-recovery text, and draft state) are
collected in the first polling assertion but are not acceptance criteria themselves;
the later exact request, retry, history, and payload assertions carry the acceptance
claim. I found no data-loss or weakened request-attempt assertion requiring a source
change.

## Test evidence

Not run by this worker: no source edits were made, and the conditional exact-source
gate was forbidden after the failed graph proof.

Lead-reported validation for commit `54c145906` (not independently rerun here):

- `node --require ./vitest-runner.cjs node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/hooks/useTimelineCommandsService.parentMedia.test.ts src/tools/video-editor/hooks/useAssetManagement.mediaImport.test.tsx src/tools/video-editor/hooks/useAssetManagement.assetDrop.test.ts src/tools/video-editor/hooks/useExternalDrop.test.tsx src/tools/video-editor/hooks/useTimelineState.history-authority.test.tsx src/tools/video-editor/contexts/VideoEditorProvider.test.tsx src/tools/video-editor/commands/parentClipAddCapture.test.ts src/tools/video-editor/commands/commitSession.test.ts src/integrations/runtime/dataProvider.test.ts src/integrations/runtime/mediaImport.test.ts`: **274 passed**;
- `node node_modules/eslint/bin/eslint.js --no-cache --max-warnings 0 src/tools/video-editor/hooks/useTimelineCommandsService.ts src/tools/video-editor/hooks/useTimelineCommandsService.parentMedia.test.ts src/tools/video-editor/hooks/useAssetManagement.ts src/tools/video-editor/hooks/useAssetManagement.mediaImport.test.tsx tests/e2e/local/three-products.spec.ts`: **exit 0**;
- `node node_modules/typescript/bin/tsc --noEmit --pretty false --incremental false`: **exit 0**;
- `git diff --check`: **exit 0**.

The lead's central locked-graph result above is the only reproduction evidence used
for this gate decision. The deleted central32057 trace/error context remains
unrecoverable; its zero response count is not treated as proof of zero POST attempts.

## Next step

The orchestrator should retain the central wrapper log, resolve or otherwise account
for the locked graph's TypeScript failure, and obtain the required passing
`ap2-m2-locked-graph-wrapper-owner-rerun-REPORT.md`. Only then should this exact
source delta be reconsidered for the single narrowed
`ap2-m2-parent-positive-real-causal-repair` gate.
