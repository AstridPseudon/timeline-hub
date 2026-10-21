# App2 M2 producer custody repair review

## Verdict

**REQUEST CHANGES / HOLD.** The committed repair closes the seven behavioral
defects from review0240 in source and support logic, but it does not close the
required no-blank-EOF condition. `tests/e2e/local/support/producer-ownership.ts`
still ends with two newline bytes (`}\n\n`, line 300), leaving a blank line at
EOF. `git diff --check HEAD^ HEAD` is clean only because the parent already had
the same trailing blank line; it is not evidence that the repaired file has no
blank EOF.

Reviewed commit `384add7e37ad31f55482afc758681b43b159388b` (tree from the
committed repair branch, based on `tl/ap2-m2-producer-proof-custody-defects-repair-0247`).
The repair changes only:

- `tests/e2e/local/producer-ownership-live.spec.ts`
- `tests/e2e/local/support/producer-ownership.ts`

No production source, DTO, authority, provider, store, writer, or route was
changed. No source edit was made by this review.

## Required custody controls

The following controls are present and passed static review:

- Head and revision reads use the dedicated `seed.timelineId`, not the harness
  timeline.
- Transcript IDs use the existing `sourceItemId@carrierClipId` occurrence
  identity and the existing caption-ID helper.
- Protected foreign/user IDs are asserted present before the initial deep raw
  value/order comparison; later comparisons use the same protected baseline and
  explicit presence checks in the shared assertion helper.
- Scene checks require the fresh deterministic Scene IDs and reject every
  protected target. The tested Scene callers select existing owned output only.
- The lost-ack helper uses `route.fetch({ maxRetries: 0 })`, requires a real
  Runtime HTTP 200 `accepted` or `rebased` response, then aborts only the
  browser acknowledgement. The retry compares the exact raw request body and
  exact `Idempotency-Key`.
- Refusal detection is scoped to alerts newly produced by the current action.
  Refusal remains visible, protected state is checked unchanged, and the test
  adds `no-accepted-ownership-proof`; it does not turn refusal into accepted
  ownership.
- No old pre-acceptance hold harness, response fulfillment/continuation, or
  invented authority/provider/store appears in the repaired files.

## Live callers

The proof exercises existing mounted callers only:

- `renderTranscriptAsCaptions` in
  `src/tools/video-editor/dev/transcript-lane/extension.ts`.
- `createShotsFromMarkers` and `moveExistingShotsToMarkers` through
  `ScenePhaseMarkersPanel` in
  `src/tools/video-editor/dev/scene-phase-markers/extension.ts`.

## Checks

Passed:

- `node_modules/.bin/eslint --no-cache --no-warn-ignored --max-warnings 0 tests/e2e/local/producer-ownership-live.spec.ts tests/e2e/local/support/producer-ownership.ts`
- `node_modules/.bin/tsc --noEmit --pretty false`
- `git diff --check HEAD^ HEAD`
- One-case Playwright collection with a disposable minimal config:
  `node_modules/.bin/playwright test --config .producer-ownership-collection.config.ts --list`
  — `Total: 1 test in 1 file`.
- Static negative/control sweep: all custody controls passed except the
  no-blank-EOF check described above.

The repository-wide Playwright config was not used as evidence: it excludes
local journey specs and its isolated-port preflight failed before collection.

Not run by instruction: browser execution, localhost/live sockets, Runtime
gate, full suite, actual acceptance, source activation, merge qualification,
and installation.

## Decision and next step

Keep this as a **future source-only route-proof scope**, not an accepted route
or merge qualification. The native host-field carrier is still absent, so no
actual producer acceptance or writer retirement can be claimed. First remove
the extra EOF newline, then repeat lint, diff-check, static negatives, and
one-case collection. After the native carrier and matched Agent/Runtime/App
cohort exist, run the single central browser case; retain the visible atomic
refusal if the route still refuses.
