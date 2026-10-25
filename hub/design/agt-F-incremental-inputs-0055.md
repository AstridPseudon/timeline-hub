Completed the private incremental MAIN packet; no repository files changed.

- Eligible union: 298 unique selectors.
  - Retained 227 from prior 251.
  - Excluded only 24 exact D87-retired native-batch records.
  - Added 71 newly merged families.
- Preserved all 550 rollup identities/dispositions.
- Recorded Agent head `0ae146e1b0acc6e4a82ba6b4f905d88bad48320c`, tree, parents, Runtime `a3cd1a3`, source/review receipts, and 1,932 dependency hashes.

Evidence: [packet directory](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-incremental-inputs-0055/evidence)

Checks passed:

- JSON/TSV parse, 298-selector uniqueness, lossless 550 accounting.
- AST selector-function existence without collection.
- Protected hash checks.
- `bash -n main-affected-batch-recipe.sh`
- `python3 -m json.tool validation.json`

No pytest, collection, service, browser, build, or functional qualification was run. MAIN D73 checkouts, receipts, profile, poison preflight, and JUnit remain pending.

Noted the M2-placement author-report hash discrepancy; packet uses hashes from the reviewed merged `4a7f321704` tree and records the discrepancy in `hash-notes.md`.

`DONE` and commit message were written.