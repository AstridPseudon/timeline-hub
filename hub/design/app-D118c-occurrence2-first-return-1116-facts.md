# D118c occurrence-create2 first return

Verdict: unapplied owner handoff; known RED remains.

The prior candidate's unsupported request metadata was removed from the only allowed file. The body wrapper is byte-identical to authorbase `942855e56e774d83b3930bbfd87df22dbcd94ad1` and original `070dfc5ef4f3dc35062fcb36a50cb571cd77fbd2`, SHA-256 `26ecb3e8da202dc9a1113f942cf9c1a7384600d8662cb9c1e8d983caf17afe6f`. The prior candidate hash was `91b0d3e7f5815892e58cb0256640a08173fe3e7703cff0a4caa480d0e9bcf855`. The `08e6b905` evidence root does not contain this path.

All 29 assertions, the full target test-function AST, semantic inputs, authored `1e308`, expected status `409`, expected reason `unsupported_timing`, no-write/history guard, inverse/redo/retry purpose remain unchanged.

Source-only current mapping: `native_occurrence_create.py:33-38` raises `CommandError(kind='unsupported_timing')` for timing conversion failure; `commit.py:1456-1469` passes the kind to `_failure`; `_commit_errors.py:65-71` classifies `unsupported_*` at an unchanged base as invalid/HTTP 422; Runtime `timeline_commit_port.py:96-100` copies that status and details onto `RuntimeErrorBase`. The retained subprocess failure at line 70 reporting inner `_prove_birth` status 1 is not causally explained by these source facts. No caller/product fix, assertion change, prepared record, service run, or behavioral claim was made.

Static controls passed: Ruff, mypy with skipped imports, py_compile in the resolved task temp directory, `git diff --check`, source hashes, and AssertAST/function-AST conservation. Behavioral tests were not run per the source-only brief.
