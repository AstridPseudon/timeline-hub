## Rerun report: agt-public10-rerun

**Result: `remotion-0010-nodes` passed, 12 of 12.** The earlier TextCard SSR failure was environment drift, not code.

### What I did
- **Precondition check:** `/home/user/work/runtimes/agent-remotion-0010/package-lock.json` is byte-equal to the committed `remotion/package-lock.json` at HEAD (`cmp` against `git show HEAD:...`). The worktree is clean at `ba633b20`.
- **Runtime exact-pair suite (`bundle1-runtime6be9706-integration`):** not rerun. The tree did not change, so the brief's condition ("only if the tree changed") was not met.
- **Node suite:** requested via `request-test agt-public10-rerun remotion-0010-nodes --no-cache --files "..."` with the five targets, then `wait-test`. Service ID `agt-public10-rerun-remotion-0010-nodes-1020050742-21158`.
  - Command: `/tmp/claude-0/.../orch/bin/request-test agt-public10-rerun remotion-0010-nodes --no-cache --files "tests/reshape/test_remotion_gate.py tests/core/test_editor_element_catalog.py tests/core/timeline/test_clip_fields.py::test_render_status_defaults_to_pinned_union_composition tests/journeys/test_journey_plumbing.py::test_renderer_install_problem_names_the_missing_install_and_the_fix tests/packs/rendering/test_remotion_render_contract.py::TextCardVisibleMarkupTest::test_text_card_renders_visible_markup"`
  - Result: `pass exit=0 in 8s`, `12 passed in 6.77s`. No failures or skips.
  - Per-node: the pytest output gives only the total. I recorded each target as pass, which is supported by the exit code and total. Individual node lines were not printed.
- **No full suite** was requested.

### Changes in the worktree
- `design/m2-public10-adoption.md`:
  - Status changed to "verified".
  - New section 9 records the precondition, tested tree, exact command, service ID, and per-target results.
  - Open-items bullet for the lockfile marked done.
  - Section 1's `a158800a` is explained as the pre-commit snapshot tree. The tested tree is the committed `16d6528c`.
- The doc changed on disk after my first edit. I checked the diff, and it matches my edits.
- No test files were touched. Nothing was skipped or xfailed.

### Files written
- Commit message: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-public10-rerun/commit-msg`
- DONE marker: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-public10-rerun/DONE`

### Still open (unchanged from the adoption doc)
- Section 5: the vendor-lock script was not run in an unrestricted shell.
- Section 6: the source of `4e52f7df` is unknown.
- Section 7: the Remotion gate `install` was not run.

### Recommended next steps
- Orchestrator to decide whether the vendor-lock script run (section 5) is needed before the adoption is accepted.
