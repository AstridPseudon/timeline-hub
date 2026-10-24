## Report

- Added isolated witness: [test-support/new_image_witness.py](/home/user/work/wt/agt-A4-image-created-current-0154/test-support/new_image_witness.py).
- Prepared input: 8,957 bytes, SHA-256 `c0a3b657…3c83eb1e`; manager copied it exactly.
- App output: SHA-256 `af1a9a845d4b6cc43315385e149072ef20f57af885c53c4fa5c546a68fc809ad`.
- Runtime accepted the request, receipt `txn-15e03e4e55bf485cae9b70831ce25663`.

Tests:

- `py_compile`: passed.
- `ruff check`: passed.
- `git diff --check`: passed.
- Witness execution stopped at the required boundary: Runtime enriched the returned command with `authorship`, `bindings`, `expect`, `reads`, `resolved`, and `selections`, so exact command equality failed.

Per plan, no retries, inverse, readback, refusal controls, or speculative fix were run. Evidence and commit message were retained; `DONE` marker created.