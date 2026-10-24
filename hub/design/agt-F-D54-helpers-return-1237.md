## Completed

- Produced [D54/D57 classification evidence](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D54-helpers-return-1237/evidence/agt-F-D54-helpers-return-1237.json).
- Classified all 23 nodes as core:
  - 21 provider/session/commit nodes
  - 1 D13 native-preflight node
  - 1 D23 helper node
- Preserved exact D52 membership, status, order, summary offsets, and traceback offsets.
- Categories: 22 `UNPROVEN`, 1 deferred D23; 0 proven regressions, environment, pre-existing, or dead-scope.
- Added per-file semantic properties, D54 clauses, test assertions, and production caller line evidence.
- No product or test edits.

Validation:

- `python3 -m json.tool ...`: PASS
- Inline parity validator: PASS; exact 23-node membership/status/order/offset parity
- Worktree status: clean

Blocked evidence: exact upstream `25359ed68` pass/fail comparisons are unavailable. Recommended next step is to obtain those comparisons before assigning regression or pre-existing status.

Commit message and empty `DONE` marker created.