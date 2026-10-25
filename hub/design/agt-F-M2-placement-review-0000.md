# FAIL_SOURCE — F-D85/D86

Reviewed `tl/agt-F-M2-placement-2350` and the three owned test files. No product changes made.

Findings:

1. `GenuineTimeline.accepted_boundaries()` submits local inverse records directly to a fresh Runtime timeline ([test_recipe_m2_auto_placement.py:161](/home/user/work/wt/agt-F-M2-placement-review-0000/tests/editing_conformance/test_recipe_m2_auto_placement.py:161)). Those records contain the fallback `timeline.inverse` publication `"accepted-publication"` from `test_recipe_m1_commands.py:101-103`, but Runtime history only contains bootstrap. The exact capture/redo selectors therefore lack a genuine accepted original receipt.

2. Shared placement builds local-only `overlay`/`clip-c` state and expands duration to 20 seconds ([test_recipe_m2_shared_auto_placement.py:50](/home/user/work/wt/agt-F-M2-placement-review-0000/tests/editing_conformance/test_recipe_m2_shared_auto_placement.py:50)), then submits commands against the unchanged Runtime document ([test_recipe_m2_shared_auto_placement.py:311](/home/user/work/wt/agt-F-M2-placement-review-0000/tests/editing_conformance/test_recipe_m2_shared_auto_placement.py:311)). Runtime therefore lacks consumed `clip-c`/`overlay` and retains the original 10-second duration.

Evidence:

- Source hashes match author report:
  - `53a426d4...42688e12`
  - `57df2ad1...84bbabd`
  - `339fc32c...b0ca8ad9`
- `py_compile`: passed.
- Candidate Ruff: passed.
- Baseline Ruff via `git show HEAD^`: passed.
- Candidate and scoped baseline mypy (`--follow-imports=skip`): passed.
- `git diff --check`: passed.
- AST review: original test assertions, `pytest.raises`, decorators/parameters, and control branches remain; all 20 requested selectors remain present.
- No pytest, service execution, build, or body execution performed per brief.
- Worktree remains clean; no commit message written. `DONE` marker created.

Recommended next step: repair the Runtime-backed setup and redo custody, then re-review before requesting functional qualification.