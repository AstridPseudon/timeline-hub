Finite WIP: authenticated fixture prepared; R1 capture fixes still required.

Changed only `test_recipe_m1_commands.py` setup/helpers. Registered removals, survivor edits and inverse requests now use real `RuntimeCommitService` with existing `MediaRealm` accepted history. All **46 original test ASTs**, parameters and assertions remain identical.

Validation:

- Exact ten: **10 failed, 116 deselected**. Eight reach the production inverse guard and fail with `intervening_write`; two accept undo but lack the required collection-order selection.
- Scoped Ruff, qualified mypy, AST parity and `git diff --check`: **PASS**.

[Exact commands and results](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-M1-auth-fixture-sol-1152/evidence/commands.txt) · [Final XML](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-M1-auth-fixture-sol-1152/evidence/exact-ten-canonical.xml)

Next: merge forward the reviewed R1 member-removal correction, rerun ten, then run 126 only if green. Redo and Runtime persistence remain unqualified. No 126/full/gate/original-ABA run occurred.

Commit message and `BLOCKED` marker written. No product changes or Git writes.