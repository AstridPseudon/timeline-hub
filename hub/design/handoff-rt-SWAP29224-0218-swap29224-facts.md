# SWAP29224 retained facts

## Safe result

The single retained normal original was a `POST` timeline-commit request for the mounted popup SWAP category. It received HTTP `503`, with safe error code `not_ready`, reason `runtime_unavailable`, and message:

> Timeline commit outcome unavailable; retry the exact request

This is the observed response, not the intended accepted commit reply. The intended accepted status was `200` with `data` and `receipt`; neither an accepted reply nor a receipt is retained for the SWAP. Do not infer a backend failure from the frontend message alone.

Readiness passed. The case ran for `71.801s`; the normal artifact ran from `2026-10-25T01:47:06.714Z` to `2026-10-25T01:50:50.678Z` (`223.964s`). The single original was not retried or replayed.

## Runtime phase correlation

The retained phase ledger is `d66/runtime-private/p2-commit-phase.jsonl` (12,841 bytes; SHA-256 `6607b3c859ee0152b986053b1200327f391e7cd0c9b1492c2fa2ee04ec18e307`). Its safe records correlate as follows:

| ordinal | provider | accept | receipt | response |
|---:|---|---|---|---|
| 1 | start `1867.126`, end `3082.299` | start `2716.093`, end `3082.133` | start `2724.588`, end `3081.731` | start/end `3414.210`/`3414.365`, status 200; second start/end `3414.692`/`3415.307`, status 200 |
| 2 | start `8875.476`, end `17533.416` | start `13220.504`, end `17531.893` | start `13329.666`, end `17528.237` | start/end `22329.466`/`22330.025`, status 200; second start/end `22331.328`/`22334.960`, status 200 |
| 3 | start `27926.997` only | not retained | not retained | not retained |

For ordinal 3, the earliest retained missing phase is immediately after `provider/start`. Authorization records continue through count 9 ending at `34057.745ms`, but there is no retained provider-end, accept, receipt, or response record afterward. The frontend later reports the 503 unavailable outcome; the retained ledger does not provide a safe Runtime response-phase record for ordinal 3.

## Exact limits

- The historical tuple remains App `3a2d6067`, Agent `0d142f`, Runtime `a3cd1a`, Composition `635f4de`; no retargeting or D88b inference was made.
- The App branch supplied for correlation is `tl/rt-P2-SWAP-reviewed-submit-0145`.
- The test location is `tests/e2e/local/three-products.p2-popup.spec.ts:949:1`; its SHA-256 was unchanged before/after: `09f5e2c2ea2a207575534a88adf2847d68cdd389caa5d145580100f21302b2b9`.
- The original 45-second limit and fresh-validation/no-write/no-leak guards remain exact requirements. Because the request refused before the later tail, this result does not claim reload, undo, or those later acceptance assertions passed.
- Raw authorization, request body, idempotency key, URLs, request identifiers, private stack traces, and trace contents are not exported.

## Artifact correlation

The central normal artifact is `d66.tgz` (105,611,701 bytes; SHA-256 `0689ae1468cdb463036864304e5f0e8b57b562d6d4da5a9ed45131a2d0c5c9c3`). Its manifest records readiness exit 0 and normal exit 1. No product, test, helper, schema, or generated files were changed for this evidence-only handback.
