# OPS D141 measured-trace independent review

## Verdict

**FAIL / not ready for CAS publication or admission.** The measured-floor and trace controls pass the private isolated control harness, but the actual normal caller exposes two blocking identity mismatches.

## Complete path and first proved seam

The reviewed path is:

`request-test` → pending `TEST <full generated ID>` → `dispatcher-daemon` → `test-run <full generated ID>` → receipt validator → source/tree snapshot, cache key and lease/body admission → heavy body and trace sampler.

The first proved seam is `test-run`'s held-ID case statement. It matches only literal `8912` and `19479`, while the normal caller supplies full generated IDs. This is not a suffix-only theoretical concern: invoking the candidate in an isolated temporary root with the exact held and cancelled full IDs admitted both synthetic bodies and both reached `pass`.

### F-D141-FC-001 — blocking: held/cancelled guards do not protect actual IDs

Candidate `ops-d141-measured-floor/bin/test-run:23-25` checks exact `8912)` and `19479)` cases. The real dispatcher path passes full IDs:

- held old pristine: `rt-pin-fa9cd546-full-d141-pristine-1026005231-8912`;
- cancelled P4: `agent-p4-current-becfe-http-3legs-1026012948-19479`.

Exact-full-ID isolated subprocess result: both admission calls returned `0`, both bodies reached `pass`. The short-ID controls in `real-controls.py` do not exercise this production identity shape.

Required next command after the source correction is the normal caller route for each retained exact ID, with the existing queue/request held and no reissue, direct `--run`, environment bypass or alternate body. The old `8912` request must remain unchanged and the cancelled P4 ID must remain refused.

### F-D141-FC-002 — blocking: P5 authorization binds the wrong ID

Candidate `validate-receipt.py:207` requires `(job_id, repo, suite) == ("6934", "runtime", "d141-p5-cut")`. The existing normal request is `runtime-d141-p5-cut-1026013331-6934`. An exact-full-ID isolated receipt validation returned `3` and refused with `P5 decision is not bound to service 6934`.

Required next command is the normal existing P5 request/receipt path bound to the exact full ID `runtime-d141-p5-cut-1026013331-6934`; no bare-ID or arbitrary-suffix acceptance is valid.

## Controls that passed

- `real-controls.py` ran actual candidate subprocesses in temporary roots. It passed D141g, D141h using `full-d141-pristine-targeted15`, and bare synthetic P5 controls; floor equality/above/below, default light/core/heavy boundaries, global 4.5GB guard, one-heavy occupancy, malformed `df`, duplicate JSON keys, path/symlink/hash mismatch, and failure/cancel trace cleanup.
- D89d receipt formula is strict and inclusive at the measured floor: `max(4600000000, 4000000000 + (start - stop) + 200000000)`. Witness ownership, regular/no-follow paths, hashes, source head/tree, command hash, scope, decision and exact schema are checked.
- Heavy bodies start a five-second sampler bound to the body PID/start tick and job ID; first/periodic/final rows are fsynced and validation requires first/final plus increasing times and periodic intervals. Failure/cancel paths retain the body exit result while reaping/finalizing the sampler in the isolated harness.
- No receipt leaves the default floor/authority path in place; no arbitrary execution/source selection field is accepted in the receipt.
- The exact supported targeted-15 name is `full-d141-pristine-targeted15`, matching the corrected private 0236 recipe and the candidate allowlist. The old central `full-d141-pristine` row remains the queued 8912 row and was not changed.

The separate targeted-row validator fail-closed finding is owned by Luna0247 and is intentionally not duplicated here. Synthetic harness results are control evidence only; they are not product proof or a gate result.
