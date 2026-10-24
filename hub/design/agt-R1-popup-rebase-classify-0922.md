## Result

Source classification: **FAIL — current Agent provider defect confirmed.**

The exact donor `d99fd1a0bc` and current provider inputs are legitimate. Offline execution produced:

- `accepted`: PASS
- `merged` after disjoint parent `meta` edit: FAIL with `binding_changed`
- failing ref: `internal-revision:authoring-timeline-revision-79bb…`

The smallest source seam is [`_commit_patch.py`](/home/user/work/wt/agt-R1-popup-rebase-classify-0922/astrid/sdk/timeline/_commit_patch.py:804): same-step materialization roots from `occurrence.fork` are not retained as staged continuation bindings. [`rebase_patch()`](/home/user/work/wt/agt-R1-popup-rebase-classify-0922/astrid/sdk/timeline/_commit_patch.py:828) then reaches line 843 and rejects the intermediate internal revision. The production caller invokes this path at [`commit.py`](/home/user/work/wt/agt-R1-popup-rebase-classify-0922/astrid/sdk/timeline/commit.py:1143).

The mounted App merged expectation remains the old RED control; no assertions or fixtures were changed.

## Source custody

- Base: Agent `ba55ac1e9e`
- Actual witness: `67d5f19716`; provider `commit.py` and `_commit_patch.py` are byte-identical to base.
- Selected 079: `079580ca46`; source differs materially.
- Faithful 079 reproduction was blocked because its older `CommitPatch.after()` is incompatible with the current helper’s `inverse_records` call. No pin recommendation is made.

## Checks

- Ruff: PASS
- Mypy: PASS, 3 files
- `git diff --check`: PASS
- Focused offline pytest: **20 passed, 2 failed, 111 deselected**. The two failures are existing occurrence-fork reload/undo failures, unrelated to this popup path.
- No Runtime service, HTTP, database, browser, full suite, or original journey used.
- Worktree remains clean; commit message and `DONE` marker created.