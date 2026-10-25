Completed the finite scope handback. **No source changes applied; no faithful fixture-only fix established.**

- **Original-third, all five failures:** the first 3.5-second move stores local `at=0.20000000000000018`; with `hold=1.8`, exact validation exceeds the approved 2-second bound. Later unchanged moves exceed it materially: the ABA move ends at 2.5 seconds; the repeated sibling move ends at 9.8 seconds.
- **Authored-first, all five errors:** `shot_item_map` looks for newly created `repeated-third` in the authenticated batch baseline. Publishing its birth separately would still leave the `[] → [shared-source-item]` membership change without an authenticated item correspondence.

The exact 2000 ms/13-second inputs, shared topology, five original test bodies, and 29 assertions remain intact. Owner decisions are needed on interval compatibility and provider provenance scope. No guard relaxation or fabricated identity is proposed.

Validation:

- `python3 /tmp/w-bb45420810/d91_source_audit.py` — passed source AST/compile conservation, captured payload/CAS hashes, and inspection of all ten retained XML traces.
- Scoped baseline/candidate Ruff and mypy — all exited **0**; [exact commands and results]( /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-D91-interval-identity-sol-0433/evidence/baseline-mypy.json).
- `git diff --check`, `git diff --exit-code` — passed; worktree clean.
- No behavioral execution. Retained central **2966 remains 5 failed, 5 errors in 6.99s**.

HEAD remains `12c4efdd8603480f0d72024e29a55c6ef73c9dd7`; tree `7a37b062da5ecfe732da6618f81028f222573a93`; test blob `621110f87f0af576097aeeaa92574f18f29e999b`.

[Detailed unapplied handback](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-D91-interval-identity-sol-0433/evidence/unapplied-handback.txt) contains precise fields, source locations, C0 constraints, and recommended owner actions. Evidence is under 0.5 MB. Task-named commit message and `DONE` written.