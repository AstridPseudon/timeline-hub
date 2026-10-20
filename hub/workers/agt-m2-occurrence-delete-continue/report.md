The branch is now reviewable as-is, and I didn't need to port the Bundle2 stack. The targeted tests pass: 358 passed, 23 deselected. The 23 deselected are `integration`-marked and need a Runtime checkout, so I didn't run them. I did not run the full suite or the Runtime `-m integration` lanes for delete.

**The branch already carries most of the M1 fixes.** `tl/integration` gained 8 M1 commits since the merge base (`fc324e83`). The branch's Bundle2 stack already has most of them in a more evolved form (opaque-item remap, inverse images, shared-redo). I couldn't run `git merge`, so I did the reconciliation by hand in the working tree instead of a real merge.

What I changed:
- **Exact-encoding fix (`astrid/sdk/timeline/commit.py`, `astrid/core/timeline/authoring_bundle.py`):** the branch was missing the fix where reuse of immutable shot, parent and manifest images compares exact encoded content. Before it, `2` vs `2.0` and `1` vs `True` could reuse an old image. I added it to `document_from_bundle` and the materialization compare.
- **Conflict resolution:** for the other `commit.py` conflicts I kept the branch side. It supersedes integration's equivalent code (`AcceptedRecords`, inverse sources, boundary checks). `_command_state.py` needed no change.
- **Tests and catalog digest:** I brought in the integration tests the branch lacked: the new numeric-move test and the added cases in six existing test files. I also took integration's `artifacts.json`, since the catalog source is identical.
- **Deliverables:** `design/m2-occurrence-delete-status.md` and the commit message are written, and the DONE marker is created.

The 358 passes came from `request-test targeted` (run `agt-m2-occurrence-delete-continue-targeted-1020042622-8951`, tree `72c7521e`). It covered:
- the occurrence-delete recipe and provider tests
- the commit provider, document and scalar tests
- `test_authoring_bundle.py`
- `test_recipe_m1_commands.py`
- the numeric-move, opaque-items and shared-inverse tests

**Dependencies.** None of this exists on `tl/integration`:
- `AcceptedRecords`, `root_identity` and `clip.delete` come from `84db8bde`, the native editing foundation.
- The placement and occurrence media ops come from `7b61efd5`, the popup editing candidate.
- The Bundle2 editing source and product successor are `d4743e29` and `a31d712d`.

**Compose order for the group bundle:**
1. `84db8bde`
2. `7b61efd5`
3. `d4743e29`
4. `a31d712d`
5. The M1 integration commits, which this branch already carries and which should drop out as already applied.
6. The `occurrence.delete` commits.
7. The group migration command and the App read-side legacy group view. Until that lands, delete refuses non-empty legacy groups with `migration_needed`.

Steps 1–4 are about 34k lines across 96 files. Composing them is a separate Bundle2 task.

The delete schema is still only a candidate pending Runtime generation and App native acceptance proof. I didn't touch the App.

The doc is at `design/m2-occurrence-delete-status.md` in the worktree. The commit message is at `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-occurrence-delete-continue/commit-msg`.
