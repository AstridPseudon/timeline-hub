# RT08 interim port independent review

Reviewed `07dc1d05f011556540881595f7b00b901c191321` over `b92d3e7a05eec65c142294ef4873edd059e9b31d` and the three allowed Runtime
product paths. Decision: **REJECT without patch**.

Blocking defect: `runtime_protocol/timeline_materialization.py:145` iterates
`items.values()` as `for i, j`, although the validated `item_id_map` is a
string-to-string mapping. A normal map such as
`{"source-item-1": "derived-item-1"}` raises `ValueError: too many values to
unpack (expected 2)`, so item-bearing authenticated materializations cannot
pass. The reviewed `42a7203…` provenance source contains the same defect.

Author evidence remains valid for the non-item controls: 14 occupancy, 10
legacy occupancy, 230 port/contract tests, generator/artifact checks, and all
76 published artifacts byte-identical to `b92`. An independent public-floor
subset passed 8 tests, and the direct counterexample reproduced the failure.

Next step is a minimal source correction plus a positive item-bearing
materialization regression, followed by the same focused evidence and a new
independent review. No public DTO, operation, artifact, or activation change
is authorized by this review.
