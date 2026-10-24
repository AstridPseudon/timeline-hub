## R5 Occupancy Review — FAIL

No tracked edits or product changes. Cumulative diff from `458595850` changes only `tests/test_timeline_legacy_occupancy.py`.

Coverage:

- Unrelated destination ×4: PASS; authenticated provider, repeat refusal, no-write and owner invariants retained.
- HTTP F1: PARTIAL; real HTTP path passes, but exact original code/message/details tuple is no longer asserted.
- Missing shot head ×2: FAIL; both cases use the same patch shape and differ only by name, not the original new/existing revision scenarios.
- Exact retry/newer head: PASS under v2 fields/conflict semantics.
- Receipt, occurrence, digest, projection and removed-member tamper: PASS; mutations target the evaluated `main` closure and no-write guards remain.
- Historical reuse ×2: FAIL. Both cases perform `timeline.inverse` on the same timeline. They do not create the original second timeline, reuse the same physical `shot-1` historical closure while a newer global head exists, or distinguish inline versus referenced modes; `inline=True` only adds undo-step metadata.
- Dedicated old-route `410`/no-write proof: PASS.

Tests/checks:

- Required exact pytest with `ASTRID_CHECKOUT=/home/user/work/agent`: **16 passed in 46.65s**, including real HTTP F1.
- Central targeted service run: **1 passed, 15 errors** because `ASTRID_CHECKOUT` was not supplied; failures occurred during fixture setup.
- Ruff: passed.
- In-memory compile: passed.
- `git diff --check`: passed.
- Pyright: parent 20 diagnostics, candidate 0; **0 new normalized identities or multiplicities**.
- No full suite run or full-suite PASS claimed.

Provenance:

- Original Runtime: `458595850c...`, tree `703b1aac...`
- Reviewed Runtime: `51c2d6aacc...`, tree `27c6c140...`
- Agent provider: `13d42ca1b4...`, tree `6c32a525...`
- Imports resolved from the reviewed Runtime worktree, its `packages/python`, and `/home/user/work/agent/astrid/sdk/timeline`; provider loaded through `load_timeline_commit_provider("astrid")`.

Recommended next step: restore authentic cross-timeline historical-reuse fixtures with genuinely distinct inline/reference inputs, then restore the exact HTTP and missing-head predicates.