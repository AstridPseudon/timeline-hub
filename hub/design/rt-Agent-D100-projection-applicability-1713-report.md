# D100 source applicability report

- Compared held source `d3b5cf...` against Agent `d4ba991...`.
- Result: `APPLICABLE_MISSING_SOURCE_SEAM_PRODUCT_UNQUALIFIED`.
- The held `_command_state.py` change addresses the exact projection item-birth seam at `_command_state.py:369`; current production lacks it.
- Owner is the Agent provider identity seam. Runtime is not implicated.
- Retained App `own9` evidence remains 9 setup errors; no product PASS claimed.
- `fb9a47...` and the frozen candidate fixture path are `EXACTMISSING`; no fetch or alternate route used.
- No source, product, test, schema, generated, Git, or Runtime changes made.

Checks:

- AST parsing of current/held production sources: PASS.
- Source diff checks against base and current worktree: PASS.
- Retained evidence JSON parsing: PASS.
- Worktree `git diff --check`: PASS.
- Product tests/typecheck/lint/full suites: not run; N/A for read-only evidence scope.

Evidence:

- `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-Agent-D100-projection-applicability-1713/evidence/applicability.json`
- `.../source-manifest.json`
- `.../validation.md`

Next genuine acceptance step: adopt the Agent seam, independently review it, then rerun the exact retained own9 path. Completion marker and commit message were created.