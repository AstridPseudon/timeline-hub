# VW-D09 legacy fade current-source handoff

Current Agent HEAD `4467c1c1a` did not contain the qualified public DIP
replacement lineage (`76020df2e`, `12e69cac4`, `a6a8172c3` are all non-ancestors).
Removed only the obsolete private independent-fade COVERED assertion from
`tests/core/timeline/test_onscreen_more.py`. The approved Main6 proof
`1020043344-8195` establishes DIP [16,30) and incoming-COVERED controls; the
one-sided DIP positive and public incoming-transition COVERED tests remain.

Self-contained core lane: 13 passed. Rendering host/Scene neighbors were
attempted but setup was unavailable (Node 20.19.4 and renderer peers absent).
See worker REPORT.md for the exact closure recommendation and commands.
