## Report

Reviewed `agt-R2-fixture-m1-1105` read-only. No code or test changes made; worktree is clean.

The saved author result is confirmed: 116 passed, 10 failed. All ten are the shared `occurrence:occ-1` redo cases for `track.remove`/`clip.remove`, failing with `missing authenticated fork materialization` at `inverse.py:990–1019`. Evidence: [m1.xml](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-fixture-m1-1105/evidence/m1.xml).

Findings:

- The helper now correctly uses `bundle_from_document()` and the complete Runtime closure.
- `recorded_removal()` still records unsupported removals directly through `Recording`, bypassing the production `execute(..., commit_request=...)` path.
- Supported production capture emits the required authenticated shot/internal `commit.materialization` bindings.
- Fabricating those bindings or caller facts would violate the settled contract.
- All test function ASTs, decorators, assertions, ordering, full-row, and nested-opaque predicates are unchanged: 46 ASTs matched.

Checks:

- Focused recorder-only reproduction: PASS; exact `history_unavailable` refusal reproduced.
- Focused supported production capture: PASS; 2 authenticated materialization bindings emitted.
- Ruff: PASS.
- Qualified mypy: PASS.
- `git diff --check`: PASS.
- No full suite or 126-case rerun performed.

Handoff: Agent R1/provider owner must expose a faithful accepted-boundary builder using the production caller, or register production `track.remove`/`clip.remove` support. Then rerun only the exact ten cases. Current status remains code-only partial FAIL; fixture adequacy is not claimed.