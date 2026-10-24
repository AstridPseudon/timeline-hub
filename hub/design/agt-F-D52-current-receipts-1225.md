## D52 reconciliation report

Created [evidence/d52-current-receipts-1225.json](/home/user/work/wt/agt-F-D52-current-receipts-1225/evidence/d52-current-receipts-1225.json).

- Full9758 membership preserved: 276 nodes; terminal result remains 231 failed / 45 errors.
- Exact current integrated-source receipt union: 106.
- Independently qualified selectors: 103.
- Still open: 173.
- Historical267 reconciliation preserved: 61 + 3 + 3 + 209.
- Explicitly held: alias three, M1 25, native five, capability 7, and owner-held child-import subset 33.
- Source-only receipts remain non-closing; no current-full, gate, HTTP, installed-runtime, ABA, or behavior credit inferred.
- JSON includes full node membership, selectors, source/test identities, source tuples, verdicts, missing facts, proof boundaries, and v2 request-field preservation.

Checks:

- `python3 -m json.tool ...` — pass.
- Structural count/disjointness validation — pass.
- `git diff --check` — pass.
- Tests — not run, per task instruction.

Commit message written and `DONE` marker created.