No product lock change retained. The requested **head-pair-only CAS is insufficient** under the current mutable-data model.

Added [one test file](/home/user/work/wt/rt-D84-lock-placement-sol-2147/tests/test_timeline_lock_placement_limits.py). Using genuine native commits, nine concurrent mutations leave both head IDs unchanged while altering metadata, ABI, events, receipts, source digest, ownership, physical pins, ranges, or performing ABA with tamper. Current acceptance rejects every case without further writes. The unchanged control accepts and replays exactly.

Only that test file changed; no source-function conflicts with 2145. Verification functions, locks, request-scope helpers, memos and caches remain untouched.

Validation:

- Final targeted union: **527 passed in 210.75s**, zero failures/skips.
- Focused counterexamples/control: **10 passed**.
- Ruff, scoped Pyright, compile and whitespace checks passed.
- Initial probe setup errors were corrected; earlier failing logs remain preserved.

[Exact commands and environment](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-D84-lock-placement-sol-2147/evidence/commands.json), [results](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-D84-lock-placement-sol-2147/evidence/test-results.json), and [source-backed design limit](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-D84-lock-placement-sol-2147/evidence/source-limit.json) are retained.

Reused 2143 measurements show the 32.5 ms commit wait overlapping the history handler’s 40.3 ms lock hold. They establish bounded contention, not dominant cost or original-timeout causation. No gain or flat scaling is claimed.

Recommendation: continue 2145’s priority work. Lock movement needs an authorized freshness mechanism covering the other mutable authority facts; the head pair cannot replace those checks. No product security review was performed because no product change is retained.

Commit message and `DONE` created. No full/original/browser runs.