## Completed

Added `tools/main_affected_batch_d86/` containing:

- Exact 251-selector membership and argv files.
- One existing pinned-launcher recipe with strict 45s timeout and `-n 3`.
- Counts/family/owner manifest, 299 deferred records, and D23/D67/D77 visibility.
- Source hash manifest and pending MAIN submit-input template.
- C0 request/reply shape and fresh-receipt requirements.

Counts: 251 selected; D86 108; ABI20 20; next cohort 11; deferred 299, including 126 non-core records.

## Verification

- JSON parsing: passed, 3 files.
- `bash -n tools/main_affected_batch_d86/main-affected-batch-recipe.sh`: passed.
- Exact parsed recipe argv: passed.
- Python AST/in-memory compilation: passed, 16 source files.
- Selector uniqueness/membership: passed, 251.
- Hash manifest: passed.
- Existing stub positive-once/poison-zero evidence: passed.
- No pytest, service, launcher, full suite, or original body executed.

## Pending

Final source-join commits/hashes, D73 four-repo receipts, MAIN profile, request ID, evidence directory, and parsed-command preflight remain receiving inputs.

Commit message written and `DONE` created.