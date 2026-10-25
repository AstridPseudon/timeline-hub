# D136c independent review: PASS

Original-nine remains `FAIL_ACTUAL_ORIGINAL9 / NO_GO`.

- Exact retained run reconciled: 9 collected, 9 setup errors, 0 failures/passes/skips, exit 1.
- Common seam: `provider intermediate command lacks an authenticated physical observation`.
- All nine cases are bounded `UNKNOWN`; the structured refusal map and per-boundary safe values were not exposed, so neither PRODUCT GAP nor SETUP is proven.
- Source custody, loader provenance, protected projection, privacy schema, and raw-artifact custody all PASS.
- No B023–B036 cases were reached. No retry, product execution, or duplicate tests were run.

Per-case verdicts: all nine exact selectors are `ERROR / setup boundary / UNKNOWN`, with missing structured refusal map, capture-site flags, digest state, exemption outcome, and ownership/binding/continuation state.

Validation performed:

- Exact three-file carrier/donor hash and immutable-preimage checks: PASS.
- XML aggregate and selector reconciliation: PASS.
- AST/schema allowlist, bounds, hash-shape, and privacy checks: PASS.
- Protected projection SHA-256 and counts: PASS.
- `git diff --check`: PASS.
- Admission remained above the 5 GB floor; no active test runner detected.

Safe evidence files and the D136c commit message were written to the required worker outputs. Raw XML/stdout/stderr remain private and untouched.