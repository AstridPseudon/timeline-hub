# D118 current sheet15 report

- No source change made. The allocated test file is byte-identical to original070dfc and current base (`SHA-256 3d391f…b8b7`); 248 AST assertions are conserved.
- Retained evidence reports failures only by location and failure-text hash. The actual exception/stack, prepared record, and passing public-caller comparison are missing. A fixture edit would be speculative, so this is an unapplied missing-input finding owned by Agent core service.
- Checks passed:
  - `ruff check ...`: PASS
  - `mypy --follow-imports=skip ...`: PASS
  - `py_compile`: PASS
  - `git diff --check`: PASS
  - base/original file diff: clean
- Functional qualification remains unverified/RED. If rerun is authorized, Agent core service should use the exact `agent-core-full` selector after restoring the missing diagnostics.
- No protected review or merge claimed. DONE marker and commit message were created.