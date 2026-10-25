## Result

Resumed with the corrected tuple and preserved request identity. No old-tuple body had been submitted, so no body was duplicated or retargeted.

- Parent request: `...parent-1025022203-12208` — terminal NO-GO. Readiness passed; original timed out waiting 90s for the commit POST response. No retry.
- Transition-none single: `...single-1025022644-5678` — GO. Readiness and original test passed.
- D90 was not repeated; old IDs `24629` and `11446` remain terminal.

## Verification

- Profile syntax: passed.
- `d66-plain-stack.test.mjs`: 22/22 passed.
- `git diff --check`: passed.
- Worktree contains only the two allowed private profile files; no product/test changes.
- Exact tuple, source hashes, origins, and first-failure evidence recorded under the worker evidence directory.
- Empty `DONE` marker created.
- Commit message written to the requested handoff path.

The parent-move route remains unresolved and should be investigated separately; no diagnosis was attempted per plan.