# D116/G3 protected review: FAIL

- Static source checks passed: Python 3.11 AST/compile, Ruff, mypy, and `git diff --check`.
- Candidate/source custody verified at `65d1dead…`; Runtime pin/tree verified as `5e9ad1c6…` / `de2954a…`.
- One authorized Gate3 node ran once and failed during fixture setup:

  `tests/editing_conformance/native_checkout_current_fixture.py:91`

  `capture_occurrence_delete()` → `commands.execute()` → `compile_recorded()` raises:

  `CommandError: bound source occurrence/clip is missing or ambiguous`

  The remaining word-anchored card still references the deleted occurrence. No retry or alternate route was attempted.

- No source fixes made; no behavior credit awarded. Worktree remains clean.
- Raw results: `evidence/own1.log` and `evidence/own1.xml`.
- JSON/XML evidence validated. `DONE` and commit message recorded.

Recommended next step: repair the semantic capture seam so occurrence deletion can safely handle the authored word-anchor dependency, then request a new protected review.