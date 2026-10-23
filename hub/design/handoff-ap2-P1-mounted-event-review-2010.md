# Handoff: P1 mounted event adapter review — FAIL

Reviewed `ede6294adef5a48351c43787ea502840f4e529aa` on `b221388d3`.

The adapter is not mergeable. The actual published A2 producer (`201044ee6`, provenance only; not present in the reviewed target) emits the design’s version-1 event detail without `scope` or `type`. The reviewed adapter requires both, so a complete source-derived sample is rejected before projection. The reviewed target has only a test-generated init/listener in `beforeEach`; it has no production emitter or production listener boundary.

Exact correction map:

- Producer/design top-level keys: `version`, `sequence`, `time`, `phase`, `projectId`, `timelineId`, `clipId`, `ownerAlias`, `generation`, `sessionPresent`, `closed`, `current`, `identityPresent`, `scopeMatched`, `mountedHead`, `originalHead`, `basisStatus`, `gestureKind`, `patch`, `mountedClip`, `sourceClip`, `gestureClip`, `originalClip`, `status`, `ownerPresent`, `recoverableOwnerCount`, `intentsPendingCount`, `errorStage`, `errorCode`, `errorClass`.
- Current adapter retains only `version`, `sequence`, `time`, `phase`, `projectId`, `timelineId`, `clipId`, `ownerAlias`, `generation`, `status` (and invented `scope`/`type`). It drops all other producer keys.
- Current `mountedHead`/`originalHead` projection drops nested `revisionId`/`publicationId`, yielding `{}`. Current projection also drops `patch`/clip numeric values and every `*State` key because those containers/keys are absent from the allowlist.
- `phase` accepts arbitrary text; IDs are redacted rather than validated to the settled identifier rule; absent fields are omitted rather than explicit `UNKNOWN`.

Offline witness: authentic sample rejected; with artificial scope/type, `mountedHead` became `{}`, `patch`/clip fields disappeared, and `evil.phase` was accepted. Targeted Node test, all three typechecks, scoped ESLint, Playwright `--list` (exactly two), diff/path/own-commit audits all passed. No browser/full/live run was made.

See the worker report for line-level references and exact commands. Correct the producer/consumer interface without inventing a second envelope, add an authentic source-derived sample through the actual registered listener into the existing artifact path, then request a fresh independent review.
