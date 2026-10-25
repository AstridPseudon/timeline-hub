# F-D87 source acceptance

Date: 2026-10-25
Worker: `agt-F-D87-ledger-0007`
Base: current normal integration `0d142f7951` (b9f remains unmerged)

## Scope checks

- Read-only inputs: PLAN, current Agent guidance, normative Runtime
  `commit-v2.md` sections 1-5, D85/D87/D52/D72(1) reports, and the manager
  ledger. The manager ledger and Runtime ZIP README were not edited.
- Retained source manifest contains exactly 24 native-batch selectors. The
  appendix contains 25 numbered rows: 24 retained selectors plus the one
  separately mapped checkout parameter selector.
- Every numbered row contains `D87/G5/D52/D72(1)`.
- No product code, existing test, helper, fixture, schema, pin, or generated
  ledger was changed. No test was added because current promised capability
  coverage is complete.

## Static acceptance commands and results

All commands were source-only; no pytest, test body, service, build, render,
or function execution was run.

1. In-memory AST parse of the retained native-batch file: 8/8 expected
   function definitions found.
2. In-memory AST parse of named current replacement tests: all named
   replacement functions found; assertion-node counts were nonzero for every
   mapping. Result: `replacement assertion AST: PASS`.
3. In-memory `compile()` of the five replacement test files: `PASS`.
4. Appendix structural check: `25` numbered rows, `all rows cite required
   refs: True`, separate row present: `True`.
5. Scoped Ruff command:

   ```text
   PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m ruff check --no-cache tests/editing_conformance/test_native_batch_ingress.py tests/packs/timeline/test_cli_document_commit.py tests/packs/timeline/test_cli_commit_move.py tests/packs/timeline/test_cli_commit_trim.py tests/packs/timeline/test_cli_native_sheet.py tests/editing_conformance/test_commit_runtime_native_checkout.py tests/editing_conformance/test_commit_runtime_native_frontends.py
   ```

   Result: exit `1`, 11 existing `F811` diagnostics in
   `test_cli_document_commit.py`. All seven scoped source files hash exactly
   equal to their `HEAD:` blobs, so this is the true baseline/candidate result
   and not a D87 regression.
6. Scoped mypy command:

   ```text
   PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m mypy --cache-dir /tmp/w-2129611481/d87-mypy --follow-imports=skip --ignore-missing-imports tests/editing_conformance/test_native_batch_ingress.py tests/packs/timeline/test_cli_document_commit.py tests/packs/timeline/test_cli_commit_move.py tests/packs/timeline/test_cli_commit_trim.py tests/packs/timeline/test_cli_native_sheet.py tests/editing_conformance/test_commit_runtime_native_checkout.py tests/editing_conformance/test_commit_runtime_native_frontends.py
   ```

   Result: `Success: no issues found in 7 source files`, exit `0`.
7. `git diff --check`: exit `0`.
8. `git status --short`: clean.

## Coverage result

- Exact retained native-batch rows mapped: `24/24`.
- Additional checkout case mapped separately: `1`.
- Current promised capability gaps: `0`.
- Checkout cases left live: `6`.
- New targeted test: none.

