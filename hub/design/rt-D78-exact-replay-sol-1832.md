D78 remains **blocked on original state**.

- Verified the 4,459-byte body hash, key consistency, all four clean pinned checkouts, and captured provider import.
- Missing: authentic original realm/CAS/base/history snapshot and normal door credential custody. The retained headers also lack `Origin`, required by captured `door.py:532`.
- No server, replay, or stack capture ran. No hang cause or fix is established. Product/tests/kit remain unchanged.

Verification: read-only audit exited **0**; `git diff --check` exited **0**; `git status --porcelain=v1` was empty. No test suites ran.

Exact audit command, source identities, missing-state details, and stack disposition are retained in [stack-summary.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-D78-exact-replay-sol-1832/evidence/stack-summary.md).

Wrote `commit-msg` and `BLOCKED`. Next: App supplies authentic original state and resolves retained Origin custody; then resume exact replay on the captured tuple.