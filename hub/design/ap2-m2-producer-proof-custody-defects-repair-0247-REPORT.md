# App2 M2 producer proof custody repair

## What changed

Repaired only the two producer proof files from preparation0210:

- `tests/e2e/local/producer-ownership-live.spec.ts`
- `tests/e2e/local/support/producer-ownership.ts`

The proof now:

- reads the dedicated seeded timeline through the exact `seed.timelineId` for both head and revision reads;
- derives transcript caption IDs from the actual `sourceItemId@carrierClipId` occurrence identity;
- asserts every protected foreign/user clip exists before any raw-field and order comparison;
- requires Scene create/move requests to target the fresh Scene-owned clip IDs and rejects any protected target;
- uses `route.fetch({ maxRetries: 0 })` against the real Runtime, waits for an actual `accepted`/`rebased` response, then discards only that browser acknowledgement;
- records and compares the original retry request body and `Idempotency-Key` exactly;
- scopes refusal detection to alerts newly produced by the current action, avoiding stale refusal alerts;
- preserves the visible atomic-refusal branch and adds a `no-accepted-ownership-proof` annotation whenever acceptance is not demonstrated;
- removes the preparation branch's EOF blank line.

No fallback writer, API, DTO, schema, authority, or production source was added. The native carrier remains pending, so this change does not activate or qualify the producer route.

## Live callers

The proof exercises existing mounted callers only:

- `renderTranscriptAsCaptions` in `src/tools/video-editor/dev/transcript-lane/extension.ts`;
- `createShotsFromMarkers` and `moveExistingShotsToMarkers` through `ScenePhaseMarkersPanel` in `src/tools/video-editor/dev/scene-phase-markers/extension.ts`.

No live caller implementation changed.

## Checks

Passed:

- `node_modules/.bin/eslint --no-cache --no-warn-ignored --max-warnings 0 tests/e2e/local/producer-ownership-live.spec.ts tests/e2e/local/support/producer-ownership.ts`
- `node_modules/.bin/tsc --noEmit --pretty false`
- `git diff --check d19d9727a`
- Source-owned negative checks: confirmed no old harness-head reads, no `holdCommandRequests`, no route continuation/fulfillment, and required real fetch/body/key/presence/owned-target/refusal-annotation controls.
- Exact one-case Playwright collection using a private temporary config: `Total: 1 test in 1 file`.

The first collection attempt with the repository-wide config could not allocate its isolated port and was not treated as evidence. No browser or Runtime request was made.

Not run by instruction: browser execution, localhost/live sockets, full suite, actual gate, install, source activation, and merge qualification.

## Decisions and blockers

- Kept the refusal branch instead of manufacturing accepted output because the approved native carrier is still pending.
- Used the existing carrier-qualified occurrence identity and existing Scene shot-ID helper; no new identity or ownership authority was invented.
- The accepted/reloaded success path and real lost-ack route remain unverified until the native carrier and matched Runtime/Agent/App cohort are available.

## Recommended next step

After the native carrier is approved and matched, run this single case centrally. Record either the accepted/reloaded ownership proof or the explicitly annotated refusal result; do not claim source activation or writer retirement from static checks alone.
