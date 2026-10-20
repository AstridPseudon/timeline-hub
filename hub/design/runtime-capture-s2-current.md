# Runtime capture S2 current gate

Updated 2026-10-20 by `rt-m3-capture-s2-current-gate`.

## Port

The reviewed composition `dcdd8e8a2d3b3998c616490309337d97e24fc20b` was ported from base `8609333456b9537339ee1a5dfc7ffd9609242de8` onto published Runtime S2 `2c4ac180c2220bdad966bc01e95ad230e99ce26a`, tree `7ab412cc4bcbe517efcfa806e092336390312e18`.

The only product source change is `runtime_protocol/capture_validation.py`, SHA256 `572d4c8ec61e2705ce56aa3d5733b500c64ba06b9e5addca885bd457388f6b75`. The three approved capture test files are byte-exact to the reviewed composition. Only these four paths differ from published S2; official artifacts/views/connector/main/F1F2/producer bytes are preserved.

This is the approved candidate-basis validation composed with the approved all-alias claim-identity validation. It retains one Agent-owned projector/verifier, adds no schema or stored state, and leaves external RenderRequest/SDK gaps strict.

## Current Agent pairing

Current Agent integration is `cf7448ed6c1298b172d004914cfe2bb8c99048e7`. The extracted `RuntimeCommitService.capture_candidate_inputs` method is byte-identical to merged ports `0d9d0764` and `73d8a237`, and frozen approved source `92427b3a`: 359 bytes, SHA256 `1e55abe0f789d54d95c7eaa655601ab6e9cc9a88abcff3cc18c65bded6393cb2`.

The actual current host-caller pairing cannot close because the old/frozen `RenderRequest` caller has no `verified_source` attribute. The four candidate host assertions therefore remain an external Agent/native-caller propagation gap. This is recorded truthfully; no Runtime policy or original expectation was weakened.

## Gates

The prior exact approved composition service evidence, using fixed Agent `92427b3a`, is:

- paired capture: 141 passed;
- claim matrix: 25 passed;
- ordinary snapshot: 41 passed, 170 deselected;
- commit integration: 9 passed.

On the final-base port's current snapshot tree `530e1c121cf3015a2702491cbdfd90d439c736e6`:

- named targeted lane: 41 passed, 170 deselected in 22.20s;
- named commit integration: 9 passed in 13.63s;
- the available `capture-agent92427b3a-integration` name runs all marked Runtime integration tests rather than the bounded 141 selection. It produced 8 failed, 240 passed, 2 skipped, 5,418 deselected, and 76 errors in 343.71s. It is not qualification for this bounded unit. The four capture host failures are the missing `RenderRequest.verified_source`; other failures/errors are unrelated activation, ordinary HTTP, packaging/setup, and historical-admission environment cases.

No full suite was run or requested. See the worker report at `workers/rt-m3-capture-s2-current-gate/report.md` for exact request IDs, commands, and boundaries.


## Manager correction — exact current selections completed
The earlier omitted --files broad run is superseded for bounded qualification by exact manager requests on SAME tree530e1c121cf3015a2702491cbdfd90d439c736e6, commit0a04782e9a5c5420b2d506d393cd79d8d5b47418:

- candidate141: rt-m3-capture-s2-current-gate-capture-agent92427b3a-integration-1020113920-30103, 141 PASSED/65.19s;
- claim identity6: ...1020113920-29820, 6 PASSED/5.04s;
- original aliases19: ...1020113937-23120, 19 PASSED/7.23s.

All exit0; ordinary41 and commit9 above are also green on this tree. These are actual final-source results, not reused prior860 claims. Product file hash equals independently approved composition572d4c8e..., exactly four approved changed paths. Unit is source-approved/merge-ready after current release qualification ordering; original external RenderRequest/SDK propagation requirements still OPEN. Root performed no repository edits or hidden schema changes.
