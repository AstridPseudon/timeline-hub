# App2 M2 File-only occurrenceADD caller proposal

Status: unapplied and dormant until the HOME newborn adapter/carrier is integrated.

## What was prepared

- Added an App-side `submitPreparedOccurrenceMedia` caller helper in the temporary diff.
- The helper preserves the original five-field `MediaSelection`, passes the explicit `ownerRef` and serializer-provided raw child row to the existing `OccurrenceAddMediaCapturePort`, then awaits the verified-media read before `finish` and `submit`.
- Added an optional `getOccurrenceAddMediaBirth` resolver contract. HOME must provide the real `{ ownerRef: occurrence:<id>, row }` from its existing serializer/newborn absent-hold adapter; the App caller does not infer occurrence, child track, first occurrence, display ID, latest media, or a DTO/store.
- Restricted the native path to File image/video preparation. If the optional occurrence caller is present, refusal stays false and does not fall through to the ordinary parent-media writer. Transient upload skeleton cleanup is guarded in `finally`.
- Gallery generation routes, missing-original-selection handling, ordinary parent media, popup retirement, SWAP, and other file kinds remain separate/unmodified in the proposal.
- The HOME-owned `useTimelineState` wiring was intentionally not edited. Until HOME passes `occurrenceAddMediaPort` plus its serializer resolver into asset management and forwards the resulting File caller to external-drop handling, this proposal is inert.

## Evidence

All commands ran in the App worker worktree with the shared dependency tree treated as read-only.

- `./node_modules/.bin/tsc --noEmit --pretty false` — passed.
- `./node_modules/.bin/eslint src/tools/video-editor/hooks/useAssetManagement.ts src/tools/video-editor/lib/external-drop-utils.ts src/tools/video-editor/hooks/useExternalDrop.ts src/tools/video-editor/hooks/useAssetManagement.mediaImport.test.tsx --max-warnings 0` — passed.
- `./node_modules/.bin/vitest run --no-cache --config config/testing/vitest.config.ts src/tools/video-editor/hooks/useAssetManagement.mediaImport.test.tsx src/tools/video-editor/hooks/useAssetManagement.assetDrop.test.ts src/tools/video-editor/hooks/useExternalDrop.test.tsx src/tools/video-editor/commands/occurrenceMediaCapture.test.ts src/tools/video-editor/hooks/useTimelineCommandsService.test.ts` — passed: 4 files, 50 tests.
- `./node_modules/.bin/vitest run --no-cache --config config/testing/vitest.config.ts src/tools/video-editor/commands/commitSession.test.ts src/tools/video-editor/commands/parentClipAddCapture.test.ts` — passed: 2 files, 91 tests.
- `git diff --check` — passed after the temporary diff and after restoration.

During iteration, the first caller run caught one rejection-handling failure in the existing “file placement rejects” test; the temporary helper return was then awaited so the surrounding catch preserved the prior false result. The final targeted run above passed.

One exploratory Vitest invocation with `--configLoader runner` was not usable on this repo because its config references CommonJS `__dirname`; the successful targeted run used the repo config with `--no-cache` and the default bundled config loader.

## Review and handoff

Independent reread of the temporary diff confirmed that it touched only the four allowed App caller/test files, did not edit HOME state/provider/popup passthrough or competing parent-media row-local code, and did not add browser/full-suite/pin/launcher work. Product changes are restored; the companion `-UNAPPLIED.patch` is the only record of the proposal.

Blocked for activation only by the missing HOME newborn adapter/carrier on this integration base. Recommended next step: integrate HOME's committed adapter using `adaptNewbornOccurrenceMediaRow(row, kind)`, then wire the exact optional contracts above and rerun the same targeted suite on the paired tree.
