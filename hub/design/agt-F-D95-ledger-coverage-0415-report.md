## Report

Implemented D95 legacy-only retirement in the permitted test file:

- Removed exact IDs 99/101.
- Added one parametrized rebind/clear refusal test with no-write assertions.
- Preserved unbound positive tests unchanged.
- Added external evidence appendix with original bodies, hashes, citations, and replacement map.
- No guard/product/design changes.

Static checks passed:

- AST/source conservation and in-memory compile
- Ruff candidate and parent
- Mypy candidate
- `git diff --check`

Behavioral tests were not run per source-only instructions. Required protected review and main targeted run remain pending. `DONE` and commit message were created.