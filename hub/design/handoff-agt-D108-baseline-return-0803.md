# F-D108 baseline correction return (0803)

Status: **complete, source-only**. This is the first return on author branch
`tl/agt-F-D108-baseline-prep-0756` after the independent 0758 FAIL review.

## Result

The authentic upstream924 XML was parsed directly from:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D60-snapshot-return-1342/evidence/upstream-full-9244377.xml`

SHA-256: `2941565205663912985f766210bfead7db42264976fabee7dc899d03d4f4657f`.
The complete index has 12,517 testcase rows in XML order, preserving raw
`classname::name`, source file/line from the authentic `9244377` tree when
uniquely resolvable, exact testcase outcome, failure/error/skip kind/type,
source location when retained, failure text/message hashes, XML blob hash,
and an explicit canonicalization method. No raw IDs were collapsed; the XML
has zero duplicate raw-ID groups. There are no separate `<subtest>` XML
nodes. The suite total arithmetic is 13,083 = 12,517 testcase nodes + 566
subtests. Testcase outcomes are 12,396 PASS, 91 FAIL, 14 ERROR, and 16 SKIP;
these sum to 12,517 and agree with the retained service summary. The
upstream terminal is FAIL/exit 1, not PASS.

The all-current-selector table covers all 9,268 retained selectors: 2,956
exact XML joins and 6,312 absent exact selectors. Absent selectors retain
explicit no-match, name-only, body-equal, and ambiguity fields; full
parameter strings and all candidate parameterized raw IDs/outcomes are kept
without collapsing. Absent rows remain UNKNOWN. The current failure
classification and current core-open count remain withheld until the MAIN
terminal. D13 ENV and both D23 deferred identities remain explicit.

The historical 276-row comparison is separate prior evidence (75 exact: 66
FAIL/9 PASS; 201 UNKNOWN) and is not overwritten. D63 rename order 129 remains
same-function-name-only; order 181 remains same-function-name-and-body-text,
with its missing per-row D63 evidence references added to the return JSON and
join evidence. Neither counterpart observation closes a current regression.
Full-run Runtime isolation remains UNCERTAIN under the D54 custody correction.

Published artifacts:

- `design/handoff-agt-D108-baseline-prep-0756.md/.json` — non-F successor correction; F-prefixed historical artifacts preserved.
- `design/handoff-agt-D108-baseline-return-0803-upstream-index.tsv` — `d6ed7dc547645742c405e9b9288e00617f33e5f8ee378233b46fc621affd226a`.
- `design/handoff-agt-D108-baseline-return-0803-current-joins.tsv` — `0fbcdf46e9272a2a3bd1e3f275cfa09f2887e50bef848f41c68c2c71a8ef12c5`.
- `design/handoff-agt-D108-baseline-return-0803.json`.

Evidence-only source artifacts are under
`workers/agt-F-D108-baseline-return-0803/evidence/`.

No body, collection, pytest, imports, fixtures, services, browsers, install,
probes, source/product/test/registry/generated edits, caller changes, or
authority/guard changes were made.

## Canonical custody repair (0820)

The full index now matches the retained author evidence byte-for-byte, including
all 23 `tools/astrid-rename` file/line mappings (XML ordinals 12309–12331),
verified against real upstream Git blobs and AST definition lines.
The original 0803 summary is unchanged at SHA-256
`7af40efb74bc171142e5a89f7cc25b17c710001c7dba61bb8e04c971764dbfd7`. Its zero ambiguous-source count is stale:
the canonical index explicitly retains two ambiguous AST bases (ordinals 9439
and 9440), each with both valid definition lines; 12,515 bases are exact and
none are unresolved. This does not change the zero ambiguous current joins.

Pre-repair publication bytes are retained in
`workers/agt-F-D108-baseline-custody-sol-0820/evidence/preimages/`.
The historical F0756, 0758 review, and 0813 review remain unchanged.
Final custody and all 23 source pairs are recorded in
`design/handoff-agt-D108-baseline-custody-sol-0820.json`.
