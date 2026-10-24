## Report

Classification: **PASS**. The six retained failures are one Agent-provider undo defect, not stale-collaborator setup:

- Four `test_provider_occurrence_fork.py` nodes.
- Two `test_recipe_occurrence_fork.py::test_reload_undo_redo_exact_and_replay[1/2]` nodes.
- All fail at `State.shot_item_map()` with `identity_conflict: shot item source changed`.
- Before/after evidence is identical: **19 passed, 6 failed**.
- Production acceptance/merge, authenticated bindings, CAS retry, forged-history rejection, stale/ABA guards, and preview controls pass.

Cause: inverse scratch restoration returns the occurrence to its authenticated prior placement-local source, while `_runtime_document` remains the accepted fork publication. The provider compares those historical source maps as if they were unrelated. Minimal seam/owner: Agent R2 provider undo, around `inverse._validate_inputs` / `_physical_state` and `State.shot_item_map`; no Runtime defect identified. ABA20732 timeout remains separately **UNKNOWN**.

Evidence/test results:

- R1 exact command: **167 passed, 4 failed**; all 18 new R1 tests passed.
- Source review baseline: **19 passed, 6 failed**, identical failures before/after.
- Scoped Ruff, qualified mypy, and `git diff --check`: **PASS**.
- No full suite, HTTP, browser, service, or live-runtime run performed.
- Current worktree is clean; no product/test/config changes made.
- Census delta: none; these six names are absent from the current 267-node census, so failures remain unwaived.

Recommended next step: assign the historical-source boundary fix and regression coverage to Agent R2, preserving all original assertions.