# D118c occurrence-create2 first return

- Removed only the unsupported request-metadata additions from the allowed test file.
- Restored exact original body wrapper; source SHA256: `26ecb3e8…afe6f`.
- Preserved all 29 assertions, authored `1e308`, expected `409`/`unsupported_timing`, and no-write/history/inverse/redo/retry behavior.
- No product or assertion changes; known RED remains.

Checks passed:

- Ruff
- Mypy with skipped imports
- `PYTHONPYCACHEPREFIX=/tmp/w-bb90933aa6/pycache-final python -m py_compile ...`
- `git diff --check`
- Source/hash and AssertAST conservation

Behavioral tests were not run per the source-only brief.

Owner handoff: current source maps `unsupported_timing` at the base to HTTP 422/`invalid`; this does not explain the retained subprocess status `1`. Agent/Runtime must reconcile that with the protected expected `409`. No GREEN or functional closure is claimed.

Evidence: `evidence/facts.json` and `evidence/facts.md`. Commit message and `DONE` marker are present.