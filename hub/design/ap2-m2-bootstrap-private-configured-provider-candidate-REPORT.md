# AP2-M2 private configured-provider bootstrap candidate

Status: **private candidate complete; owner activation remains pending**.

## What changed

Applied the exact private RuntimeDataProvider adapter proposal to the current
App candidate. The configured `AstridRuntimeClient` now remains the provider's
client and is used for the existing create, history, immutable-read, and
commit ports passed to `initializeBootstrapTimeline`. `createDefaultTimeline`
delegates through that provider adapter. The fresh-create fixture removes its
global `fetch` fallback and installs only the existing outbox/lock test
globals, proving the configured transport owns the native request.

Changed files:

- `src/integrations/runtime/dataProvider.ts`
- `src/integrations/runtime/createDefaultTimeline.ts`
- `src/integrations/runtime/createDefaultTimeline.test.ts`

No endpoint, DTO, generated operation, store, outbox field, public package pin,
legacy publisher fallback, or shared AppRuntimeDataProvider seam was changed.
The existing constrained create/repair, outbox pre-create reservation and
discovery, same-ID recovery/readback, and opaque-content protections remain in
`bootstrapInitialization.ts`.

## Source fingerprint

- Base/current source before edits: `db10eac8e` (`feat(app): port bootstrap consumer onto current root`).
- Proposal patch SHA-256: `1e9a2a792a5a3c69a13edcbba8c5aae91c23b09b021284831c6f448d9f33541f`.
- Candidate working diff SHA-256: `753076141ade30c7d91f76cd670a6a0ee6742048669bbfd10cce23bd42016ea0`.
- `git apply --reverse --check` against the proposal passed. The proposal
  artifact stops at one unchanged context line, so its raw hash differs from
  the complete working diff; the changed hunks are identical.

## Verification

- `node node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism src/integrations/runtime/bootstrapInitialization.test.ts src/tools/video-editor/commands/bootstrapCapture.test.ts src/tools/video-editor/commands/commitOutbox.test.ts src/integrations/runtime/createDefaultTimeline.test.ts src/integrations/runtime/client.test.ts src/integrations/runtime/clientSharedSession.test.ts`
  - **PASS** — 6 files, 158 tests.
- `npm run typecheck:strict-probe`
  - **PASS** — strict-islands TypeScript check.
- `node node_modules/eslint/bin/eslint.js --no-cache --max-warnings=0 src/integrations/runtime/createDefaultTimeline.test.ts src/integrations/runtime/createDefaultTimeline.ts src/integrations/runtime/dataProvider.ts`
  - **PASS**.
- `git diff --check`
  - **PASS**.

## Decisions and remaining boundary

No new design decision was made; the supplied proposal and PLAN boundaries
were followed exactly. This remains private pending matched Agent `3c4` and
Runtime `202` qualification plus explicit owner activation. Public package
13 remains unchanged. No browser, localhost/live socket, Runtime-door,
full-suite, public release, dependency install, or activation was run.

Recommended next step: the orchestrator should review this candidate with the
paired private Agent/Runtime sources, then run the qualified real provider
boundary journey before any owner activation or legacy-writer retirement.
