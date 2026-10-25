# D124 independent actual10721 verdict

Verdict: **NO-GO**. D55b requires all eight original P2 gestures to pass. The actual sampled full tour has 5 PASS, 2 FAIL, and 1 serially NOT_RUN; readiness is a separate PASS.

The first failed predicates are:

- Element edit: `tests/e2e/local/three-products.p2-elements-assets.spec.ts:1052`, dialog status did not contain `applied`; browser/backend outcome is UNKNOWN.
- Popup SWAP: `tests/e2e/local/three-products.p2-popup.spec.ts:495`, expected HTTP 200, received 409 with safe reason `history_unavailable`; lower backend attribution is UNKNOWN.
- `registerAsset`: `tests/e2e/local/three-products.p2-elements-assets.spec.ts:1133`, serially NOT_RUN after the element failure.

The five PASS originals have source-level assertions for canonical closure/readback, history records, reload, guarded native inverse, and zero legacy traffic, and their terminal XML tails are clean. No credit is borrowed from earlier runs or attachments.

Element timing verdict: **UNKNOWN**. The browser diagnostic records POST/path and key presence but not the safe idempotency-key hash. The candidate Runtime request has a UTC anchor, PID birth/namespace/ordinal, queue and handler-entry observations, but no proven browser join, request-wall denominator, handler completion, response, or backend outcome. Arrival and exact lock wait are unsupported. No native 1.75 attribution or dominant-cost claim is made.

Custody passed: the normal and preflight IDs, durable-plan hash, D66 manifests/XML hashes, four clean pinned checkouts, service versions, original source hashes, and reviewed helper hash were verified read-only. No source/test/generated/pin changes were made, and no original/browser/full/native suite was rerun.
