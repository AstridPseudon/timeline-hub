# D118c occurrence2 report

- Preserved the original test exactly: SHA-256 `26ecb3e8…afe6f`, 29 assertions, AST unchanged.
- Ran both retained nodes against authenticated provider `astrid` and Runtime `42aad0e…`:

  - `[False]`: failed at `_prove_birth:173`; child exit `1`; observed `RuntimeErrorBase`, status `422`, reason `unsupported_timing`.
  - `[True]`: same result.

- Qualified Runtime/generated-runtime hashes and all four generator/manifest checks passed.
- Static checks passed: Ruff, mypy, py_compile, `git diff --check`.
- No product, test, input, assertion, or shared-runtime changes.

Disposition: observed Agent/Runtime contract mismatch—current source maps unchanged-base `unsupported_timing` to HTTP 422, while the retained test expects 409. Later history/inverse/redo/retry assertions remain unverified. Owner reconciliation is required; no speculative fix applied.

Evidence: `evidence/facts.json`, `facts.md`, and qualified node logs/XML/traces. `DONE` and commit message are present.