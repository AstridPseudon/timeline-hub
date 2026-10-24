## Report

**PASS — exact single-change review.**

- Diff is exactly one argument change at line 491:
  `current_head(service, editing)` → `current_head(service, editing.project)`.
- AST normalization produced identical trees after reverting only that argument.
- `current_head(service, project: str)` definition, all other function bodies, assertions, and witness predicates are unchanged.
- Worktree remains clean; `git diff --check` passes.
- Retained support control: **1 passed** (one existing pytest-mark warning).
- Ruff: **PASS**.
- Direct mypy: **Success: no issues found in 2 source files**.
- Private-TMPDIR `py_compile`: **PASS**.
- Reused retained static evidence: mypy **1904 current vs 1909 baseline**, five fewer inherited diagnostics; no full static rerun.

No code edits, live witness, App producer, new realm, full suite, browser, or network run. The scoped source correction supports merge; the actual witness remains unqualified.

Commit message and `DONE` marker written.