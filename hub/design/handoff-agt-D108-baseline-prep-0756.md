# D108 baseline-prep successor correction

This is the exact non-F successor publication for `agt-F-D108-baseline-prep-0756`.
The historical F-prefixed author/reviewer artifacts remain unchanged. This
correction adds the full upstream924 testcase index and the all-current-selector
join table; it does not reinterpret the historical 276-row D54a comparison.

## Authenticated inputs

- XML: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D60-snapshot-return-1342/evidence/upstream-full-9244377.xml`
- XML SHA-256: `2941565205663912985f766210bfead7db42264976fabee7dc899d03d4f4657f`
- Upstream Agent commit/tree: `92443771676ef2bbb547d0a103d708fa8bec4c63` / `a81a8c7f262e4416dcdefc0720fd760e026d766b`
- Current retained selectors: `9268` rows, SHA-256 `1fe99f7c09a5324fbd8c029e07a6c5def2406f1a4274e6448ea3febaba1856b1`
- Current inventory: `9268` nodes / `409` files, aggregate SHA-256 `7ac5cdd0bfa2b811f9a0a4fb719d9a28ef6080d2bb879ed29fe54fc1a6882b69`

## Corrections

The complete XML-derived index is `12517` testcase rows in XML order 1..12517; raw IDs are retained without duplicate collapse. The XML contains no separate `<subtest>` elements. Its suite total is `13083` = `12517` testcase nodes + `566` subtests. Testcase outcomes are `{'ERROR': 14, 'FAILED': 91, 'PASSED': 12396, 'SKIPPED': 16}` and match the retained terminal receipt: 12,396 PASS, 91 FAIL, 14 ERROR, 16 SKIP, 566 subtests. The terminal is FAIL (exit 1), not PASS.

All `9268` retained current selectors are indexed: `2956` exact XML joins and `6312` absent exact selectors. Absent rows retain explicit no-match/name-only/body-equal/ambiguous results and full parameterized candidate IDs; absent rows remain UNKNOWN and do not become PASS.

The prior 276-row comparison remains separate: 75 exact XML matches (66 FAIL, 9 PASS) and 201 UNKNOWN, SHA-256 `72534d6e122d282310f9275952f9711abd73c4a3ff8194e6eb5d56b6867cf917`. D13 ENV and both D23 deferred identities remain retained. D63 rows 129 and 181 remain observations only; row 181 has a per-row reference in the return JSON/table. No current failure classification or current core-open count is published before the MAIN terminal. Full-run Runtime isolation remains UNCERTAIN under the D54 custody correction.

No body, collection, pytest, imports, fixtures, services, browsers, install, probes, source/product/test/registry/generated edits, or caller/authority changes were made.

## Canonical publication custody (0820)

- Full index: `design/handoff-agt-D108-baseline-return-0803-upstream-index.tsv`,
  SHA-256 `d6ed7dc547645742c405e9b9288e00617f33e5f8ee378233b46fc621affd226a`; byte-identical to retained author evidence.
- Current joins: `design/handoff-agt-D108-baseline-return-0803-current-joins.tsv`,
  SHA-256 `0fbcdf46e9272a2a3bd1e3f275cfa09f2887e50bef848f41c68c2c71a8ef12c5`; unchanged.
- Original 0803 evidence summary SHA-256:
  `7af40efb74bc171142e5a89f7cc25b17c710001c7dba61bb8e04c971764dbfd7`; unchanged.

The 23 restored `tools/astrid-rename` file/line pairs were verified against
the real 924 Git blobs. Canonical source resolution is 12,515 exact bases,
two explicitly ambiguous bases (9439 and 9440, both candidate lines retained),
and zero unresolved. The original summary's zero ambiguous-source count is
stale and preserved as historical evidence; zero ambiguous current joins
remains correct. Publication preimages and final readback are referenced by
`design/handoff-agt-D108-baseline-custody-sol-0820.json`.
