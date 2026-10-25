**BLOCKED before editing:** frozen helper `231ddb` contradicts review 1647’s settled assumptions:

- Queue end occurs at handler entry, so ended-queue `pending_at_stop` is valid.
- Raised-after-handler retains an observed queue.
- Completed-after-error can have null completion durations.
- Missing dispatch boundaries conflict with the prohibition on relaxing phase counts.

Recorded the complete truth table with source citations: 16 flag combinations, 128 phase projections, and 16 retention combinations. Direct frozen-helper callback probes produced 12 cases; the unchanged App validator rejected four valid projections.

Baseline checks passed:

- Node20 D127/D105 selector: **2 passed, 2 selector exclusions**.
- Scoped ESLint.
- Serialized App TypeScript and node TypeScript.
- `git diff --check`.

Exact commands and results are in [commands-results.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-D127-lifecycle-complete-sol-1654/evidence/commands-results.md).

Normal/exact-4ee bootstrap controls: **NOTRUN**; source qualification was not reached. No repository source changed. Frozen helper/test bytes remain unchanged.

All five required evidence files, `commit-msg`, and `BLOCKED` exist and were verified. Recommended next step: orchestrator corrects the source-conflicting assumptions and resolves missing-boundary scope before implementation and independent review.