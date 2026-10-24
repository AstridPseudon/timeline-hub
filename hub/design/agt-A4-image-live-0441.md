## Report

- Updated only worker/realm/evidence/output path constants in the reviewed witness pair; preserved all bodies/assertions and the `007164c16` correction.
- Fresh live fixture created from Agent `985f012…`, Runtime `8ea0766f…`; input SHA-256: `15fa6ca8…829a354`.
- App output arrived and was accepted. Receipt: `txn-52c00df775974c21903e25873a36dda8`.
- Exact retry, foreign-selection refusal, and changed-body refusal passed with no writes.
- Witness failed at retained undo-preview: `validation_error`, `invalid_records`, “landing execution output differs from the prepared document.” Complete failure packet and no-write state are preserved in the worker evidence directory.
- Not reached after failure: inverse acceptance, undo retry, post-undo history, reopen/readback, canonical restoration.

Tests/checks:

- Targeted witness test: `1 passed` (existing unknown-mark warning).
- Ruff, private mypy, vendor lock, artifact manifest, and `git diff --check`: all passed.
- No full suite, browser, product/App/Runtime edits, or retries.

Commit message written and `DONE` marker created. Recommended next step: diagnose the Runtime inverse-preview prepared-document mismatch before another live witness.