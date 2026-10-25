# D115 independent review

Verdict: `PASS_SOURCE / HOLD`. The producer preserves the sealed input manifest and rejects wrong-pin/no-write tampering. Adoption remains held by the known Runtime projection failure at `timeline_commit_auth.py:2864`; no merge requested.

Per-commit results:

- `3352791b97` — `FAIL (superseded)`: accepted-path test still mutated staged records instead of authentic accepted history.
- `d00f5dda66` — `PASS_SOURCE`: corrected accepted custody to use durable history.
- `ff8d14f021` — `PASS_SOURCE / behavior OPEN`: added the real-provider regression.
- `82b6d00d7f` — `PASS_SOURCE / behavior OPEN`: producer fix is narrowly scoped to `commit.py`; no guard or observer changes.

Final candidate tree: `019ae9944d5f445776bd19c7d0c441190955c1a3`.

Evidence:

- Targeted review: `51 passed, 1 failed, 61 deselected`.
- Failure: `test_mounted_accepted_selection_uses_predecessor_input`, Runtime error: `provider sequential command output differs from its next input projection`.
- All 32 original accepted/staged PARAM variants passed.
- Ruff, mypy, compilation, and `git diff --check` passed.
- AST preservation passed: original 32 variants retained; regression AST hashes unchanged.
- XML: [review.xml](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D115-producer-review-1020/evidence/review.xml), SHA-256 `1c04923b4b2497d89b62c8a985c34d88c8c1bd0f7ee78cb30471776666739077`.

Exact commit tree hashes:

- `3352791b97` → `7c936e9c591816808ae03ab64f6268670c577fb2`
- `d00f5dda66` → `21b3d25ce7e24d69f7e6276dd7c9c249edd58b21`
- `ff8d14f021` → `80bd5e36d18a386c41c72eccc3680580e7d10084`
- `82b6d00d7f` → `019ae9944d5f445776bd19c7d0c441190955c1a3`

`DONE` and the required commit message were created.