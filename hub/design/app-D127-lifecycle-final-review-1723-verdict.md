# D127 verdict

## Source: PASS

The source-consistent validator is accepted against frozen Runtime helper `231ddb5a6605b535d26172d34439ebe7b90804de`, helper SHA256 `4ee0424b63f1f9847995a605dc1050ad7cb8ca75f4d64b8c36d851cfe723f41e`. The source selector passed D105 plus both D127 tests. The differential test covers 16 flag combinations, 128 observable phase shapes, 16 retention pairs, 13 direct callback recipes (the prior 12 plus the source-derived completed-without-handler case), and 53 generated summaries. Normal and legacy `6c9` arms, exact keysets, privacy, fixed bounds, retention/loss accounting and no-write custody remain intact.

The accepted predicates follow helper source: handler entry closes the queue; `pending_at_stop` may retain ended/raised queue state; response count has priority over dispatch error for `completed`; completion timing remains nullable after dispatch error; and missing dispatch boundaries remain explicit UNKNOWN/null. No blanket phase/count rule, generic optionalization, budget relaxation or unknown-field acceptance was introduced.

## Positive controls: PARTIAL

`D78 bootstrap` passed once after a fresh decimal admission of `5,032,046,592` bytes. The existing `P2 Runtime observer bootstrap` selector was admitted at `5,031,952,384` bytes and run exactly once, but stopped before observer bootstrap because the exact qualified Agent checkout has no `.venv/bin/python`. It is recorded as NOTRUN_AFTER_SETUP_REFUSAL, not as a product failure; no retry or alternate interpreter was used.

## Integration: NOTRUN

No integration, full, browser, native, family, SWAP, collector, service replay or tour run was performed. This review made no repository changes, self-GO or merge request.
