# Handoff: ap2-P1-current16398 causal triage

## Disposition

Current original P1 run is **FAIL / not qualified**, with two independent boundaries:

1. The first test reaches an accepted split, an accepted Agent track label, and a merged trim (HTTP 200, `status=merged`) before failing at `three-products.p1-chain.spec.ts:824`. The right clip still has `app.astrid.for: 8`.
2. The second test observes only the accepted split POST. At `:891`, `traffic.posts.length` is 1 rather than 2 after 300 seconds; `agentHead` is null and no Agent move or Runtime refusal occurred.

## First failure owner

The current App hold split is the smallest responsible seam. The seed authors `app.astrid.for: 8`; `editor-utils.ts:306-319` spreads the hold clip into the right half, and the test's accepted-split assertions at `:783-786` prove that the inserted right clip retains the raw namespace. The subsequent mounted trim is a `doc.patch` whose asserted effect is `from: 0 -> 3` (`:798-801`), while the intervening Agent command is only a track label. C0 raw preservation therefore explains the observed merged `{astrid:{for:8}}`; no retained wire body proves that the trim sent an explicit remove.

This is not the old Agent mirror seam and not a Runtime merge defect. The P1 absence oracle remains intentionally unchanged. If the settled source-window/absence semantics stand, App must correct the split effect and record the explicit clear while retaining all unknown/raw fields and full effects. Changing the oracle to accept presence would redefine P1 and is not an approved fix.

## Second failure owner

Proof/App diagnosis owns the next step. The existing funnel awaits `timelineLocalSaveHandoff.capture` before transport (`useTimelinePersistence.ts:676-677,1009-1012`); capture/head/source/session refusal or owner adoption can explain a noPOST, but the redacted retained result does not identify which. The route did not hold an unseen request, because the test holds only after observing a POST. Do not assign this to Agent or Runtime without a real second request/response.

Next acceptance is exact retained error/state evidence or one independently qualified diagnostic run that records the existing capture/outbox/owner boundary. If a complete second v2 POST is observed, then evaluate the actual Runtime response; otherwise keep the limitation.

## Constraints preserved

No production/test/fixture changes, assertion weakening, refusal substitution, new executor/capture/transport/schema/pin/tuple, or original-chain rerun was made. The full v2 request/reply contract, raw preservation, effects, reads, merge, idempotency, history, undo, and absence assertions remain unchanged.
