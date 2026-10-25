## F-D85 source review — FAIL_SOURCE (bounded)

Reviewed `c2f36dc126` against author base `efa0504f35`.

- Only the assigned test file changed.
- Exact 17 requested selectors remain.
- All test ASTs, assertions, inputs, raises, decorators, parameters, and branches are conserved.
- Runtime v2 caller chain is genuine: semantic commits and authoring publication use `commitTimeline`.
- No fabricated history, SQL, retired writer, or authority bypass found.
- Source checks passed:
  - in-memory compile
  - Ruff baseline/candidate
  - mypy baseline/candidate
  - `git diff --check`

Finding: `seed_shared_occurrence_parent` performs genuine semantic shared-source commits, then `_publish_current_candidate` authoring compilation materializes two independent `shot-placement-*` identities. The retained test still requires `source_pin['shot_id'] == 'shot-shared'` at [line 1018](</home/user/work/wt/agt-F-current-sheet-review-2353/tests/editing_conformance/test_native_sheet_current_runtime.py:1018>). This setup/test contract is inconsistent. No semantic fix was made.

Proposed existing behavior log entry:

`F-D85 | FAIL_SOURCE | shared-occurrence authoring seed materializes independent identities before source-preservation assertions`

No pytest, test-body, service, build, or functional qualification run. Evidence: `/tmp/.../evidence/source-review.txt`. DONE marker and commit message were created.