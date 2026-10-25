# D140 final handoff

Verdict: **FAIL_SOURCE** at composition head
`d7727b99fb9cb063d4c0ee73fdfa54d752666135` (tree
`222476a7f8eea57f46402ab4fefabce4e2b8a703`).

The candidate’s six source corrections are supported by targeted tests and
independent private real-script controls. One finding remains: receipt
authentication is still generic and forgeable. A producer-free synthetic
`timeline.synthetic-forged/v1` JSON passed the source-receipt check when a
private git shim reported the expected tuple. The receiver must use the actual
normal receipt formats and require their producer/digest/source closure before
this packet can become `PASS_SOURCE`.

The exact source tuple remains Agent `41ad/f103/569/635f`; current Agent
`547e1045` and Runtime `0ca306df` are explicitly stale/mismatched observations,
not receipts. Farm installed schema, current tuple receipts, child, service,
and core outputs are `UNKNOWN`/`NOT_READY` until the Farm owner performs its
own census. This review created no Farm inputs and makes no readiness claim.

Recommended next step: tighten the three receipt parsers against the known
queue/checkout/kit/provision/D73 receipt schemas and add a private subprocess
negative test proving the forged producer-free JSON is rejected, then rerun
this one final review.
