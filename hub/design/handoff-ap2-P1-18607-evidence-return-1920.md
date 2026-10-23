# Handoff: P1 18607 evidence return

Result: evidence-quality **PASS**; no-weakening **PASS**; actual P1 remains
**1 PASS / 1 FAIL, NO-GO**. Causal finding remains **INSUFFICIENT EVIDENCE**.

The exact safe packet is `/home/user/timeline-hub/hub/design/app-P1-18607-result-custody.safe.json`,
19,853 bytes, SHA-256
`97b088b687ec4779eb85dfc94c9ebb43d03bae30ae5ba96d608544d540e0c1e8`.
It parses, preserves the exact run/source identity, and records the raw-log
custody claim (26,440 bytes / 62 lines / SHA-256
`a83cc89c1909877b7f01dfe4c83e994a31b8450afae80767a01e87781bf3728b`) while
keeping the 18,661-byte overwritten replacement separate.

Qualified safe scope is line 10 (3,818 bytes) plus line 11 (2,800 bytes), with
internally consistent adjacent ranges and exact line/source-range hashes. The
line-12 detail is capped at 16,384 bytes and unparseable; its lost suffix is
unknown. SourceIn 0→3 and selected clip identity are observed, but mounted
head/basis, callback/capture, owner, recovery, and authoritative error cause
remain unknown. Wire observations are not mounted observations.

The first original test passed in 27.4s. The second observed 1 POST instead of
2, then hit 300s test and 300s afterEach timeouts; Agent move, 409 refusal, and
rollback were unreached. No App-owned causal seam is proven. No Runtime 409 or
Agent-move credit; historical 22122 stays separate.

The raw path is not available in this worker, so its hash is owner-reported,
not direct byte verification. If direct verification is needed, request only
the finite App file named in the report; do not rerun or reconstruct. No source
fix, diagnostic probe, publication, or duplicate test run is requested.
