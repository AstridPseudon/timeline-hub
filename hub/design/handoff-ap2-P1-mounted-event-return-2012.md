# Handoff: ap2-P1 mounted event final interface correction

The App P1 test adapter now matches the published A2 mounted diagnostic seam.

## Interface consumed

- Opt-in: `window.__timelineSaveDiagnosticsEnabled === true`
- Event: `timeline:save-diagnostic`
- Required validation: `version === 1` and one of the published 21 phases
- No synthetic `scope` or `type` boundary
- Fixed fields: `version`, `sequence`, `time`, `phase`, `projectId`, `timelineId`, `clipId`, `ownerAlias`, `generation`, `sessionPresent`, `closed`, `current`, `identityPresent`, `scopeMatched`, `mountedHead`, `originalHead`, `basisStatus`, `gestureKind`, `patch`, `mountedClip`, `sourceClip`, `gestureClip`, `originalClip`, `status`, `ownerPresent`, `recoverableOwnerCount`, `intentsPendingCount`, `errorStage`, `errorCode`, `errorClass`
- Head fields: `revisionId`, `publicationId`
- Numeric fields: `from`, `to`, `at`, `hold`, `speed`, each with its `*State`
- Numeric states: `present`, `absent`, `null`, `UNKNOWN`

The adapter uses own-data descriptors, bounded scalar/ID/number allowlists, and fixed output shapes. `intentsPendingCount` and `errorClass` are deliberately forced to `UNKNOWN`; no raw event object can enter the artifact. The ring is bounded to 32 records. The artifact formatter now retains the nested mounted projections instead of flattening them away.

## Failure artifact ordering

`captureFailureContinuation` first writes the existing minimal parseable safe file. Only after that write does it read the bounded page snapshot. If a snapshot is available, it rewrites the same artifact with the actual projected records; if the page is closed or the read fails, the first file remains valid. Later IndexedDB/DOM collection stays best effort and cannot replace the original assertion.

## Evidence

Targeted Node test, both serialized typechecks, scoped ESLint, `git diff --check`, and the exact two-test Playwright listing passed. The protected first and second journey regions remain byte-identical to their required hashes. No live browser/P1 or full suite was run, so emitter-to-artifact behavior in a real page is still unverified.

The harness should commit the current worktree using the supplied commit message, then dispatch the required independent review before App merge. This worker has not committed, merged, pushed, or modified any product/emitter/harness/config/generated/dependency files.
