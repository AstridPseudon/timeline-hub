Completed the scoped **R1-reorder-history** fix. Only `_commit_patch.py` and a new focused test file changed.

History now replays occurrence `list.move` through the existing guarded evaluator at each sequential boundary. Exact physical rows, pins, order, membership, and final closure checks remain enforced.

Verification:

- Original three history cases: **old source 3 failed → new source 3 passed**, with expectations unchanged.
- Original focused cohort: **145 passed**.
- New guard tests: **12 passed**, covering sequential move/timing replay, membership versus order reads, native row-write ABA, forged rows/pins, and output mismatch.
- Scratch-only publisher witness `test_reorder_emits_source_bound_list_move_and_keyed_timing_changes`: **1 passed**.
- Scoped Ruff, artifact manifest, and `git diff --check`: **passed**.
- Whole-tree Ruff: **2,145 parent/current diagnostics**, identical identities and multiplicities.
- Mypy: **1,909 parent/current errors**, with identical error and note identities and multiplicities.

[Exact commands, results, and durable captures]( /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R1-reorder-history-sol-0239/evidence/commands.txt) accompany old/new source, actual provider replies, no-write conflict captures, and publisher request/reply/history. Evidence totals **3.3 MB**.

Retained unchanged: root assignment `7784e9e1cc`, forward reorder `4b49e6cce4`, and helper `184dc20a70` via merge `8a8dbf2d4e`. Publisher `5b5eab591` was overlaid only in scratch; reserved inverse `dfe105e13e` and historical carrier `975dd47157` were not imported.

The seven known external inverse failures were **not rerun**: six configless-root redo failures in `_step_undo.py` and one absence-restoration rejection in `validation.py`. Vendor checker execution remained unrun per the explicit restriction; pin `34eac004` is unchanged.

No full suite ran. Commit message and `DONE` are written. Next: cumulative independent review, then the current-only integration join.