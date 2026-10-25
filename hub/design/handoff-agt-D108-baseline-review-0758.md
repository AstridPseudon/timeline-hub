# F-D108 baseline-preparation review

Decision: **FAIL**.

The prep content is substantially source-authenticated, but it does not satisfy
the full-scope handoff requirement. The retained authentic terminal XML was
read: the 75 exact rows map to it with matching ordinals, outcomes, canonical
testcase blob hashes, and failure-text hashes. However, the retained index is
only the historical D54a 276-row table. It is not a full upstream924 XML node
index for later attribution of every full-core failure.

## Authentic terminal input

The exact retained XML is:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D60-snapshot-return-1342/evidence/upstream-full-9244377.xml`

SHA-256: `2941565205663912985f766210bfead7db42264976fabee7dc899d03d4f4657f`.
The XML parses as `testsuites`; its suite reports 13,083 total, 12,396
passed, 91 failed, 14 errors, 16 skipped, and 566 subtests. It contains 12,517
`testcase` nodes and no separate `<subtest>` elements. The terminal is FAIL,
not PASS. Runtime full-run isolation remains UNCERTAIN per D54 custody
correction.

## Checks that pass

- The actual prep files exist under the F-prefixed names and their JSON parses.
- `d108-upstream924-node-index.tsv` has 276 unique rows in order 1..276 and
  276 unique current selectors.
- The table has 75 exact XML rows (66 FAILED, 9 PASSED) and 201 UNKNOWN rows.
  No missing row is treated as PASS.
- All 75 exact XML ordinals and canonical testcase blob hashes match the
  retained XML; all 66 exact failure-text hashes match.
- Rename checks are 201 attempted, 2 exact counterparts, 199 no-match, and 0
  ambiguous. The two authenticated counterparts are retained as observations,
  not current PASS or regression closure.
- D13 is pre-indexed at order 162 with its exact node ID. D23 is pre-indexed at
  orders 170 and 213 with exact node IDs; order 170 remains UNKNOWN and order
  213 is the exact upstream PASS.
- The 9,268-node/409-file current inventory boundary and aggregate hash are
  preserved. No current numeric core result or current failure classification
  is claimed. Approved dead-scope assignments remain zero.
- Order 129 is same-function-name only; its normalized body is not equal.
  Order 181 is same-function-name-and-body-text; its normalized AST body is
  equal. Order 181 has an empty per-row `source_evidence_refs` field, though
  the separately hashed D63 correction artifact authenticates the decision.

## Precise omissions and smallest repair

1. **Blocking — full index missing.** Retain an evidence-only index derived
   from the authentic XML for all 12,517 testcase nodes, carrying suite total
   13,083 and subtest count 566, raw node ID, outcome, failure identity/location,
   XML ordinal, and canonical testcase blob hash. This needs no rerun.
2. **Blocking — exact prep filenames missing.** The searched original paths
   are EXACTMISSING:

   - `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-agt-D108-baseline-prep-0756.md`
   - `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-agt-D108-baseline-prep-0756.json`

   Republish the already validated F-prefixed content under those exact names.
3. **Non-blocking traceability gap.** Add the D63 evidence reference to the
   order-181 row, preserving its pending-current-proof decision and UNKNOWN
   exact-selector status.

Evidence: `workers/agt-F-D108-baseline-review-0758/evidence/review-validation.json`.
No product, test, generated, registry, service, or suite mutation was made.
