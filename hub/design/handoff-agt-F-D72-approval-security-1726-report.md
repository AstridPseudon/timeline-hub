## F/D72 Review — PASS

Reviewed candidate `c3cbc3859621d15e03435cdd36d54b35229927f6` against base `867296c1e57583162970d5ec14d030f1b042002a`.

Findings:

- Approval validation matches frozen 924 behavior: candidate/publication digests, project/timeline scope, base binding, kind/schema/decision.
- Validation occurs before `commit_timeline`; five tampering controls confirm zero writer calls.
- Approval is absent from the Runtime wire request.
- Original render/restart, replay, count, approval, and single-generation assertions remain behaviorally preserved.
- No old writer, alias, or new wire field.
- Detached opaque `approval_id` remains an inherited limitation, not a D72 blocker per the settled brief.

Tests:

- Exact targeted selectors: `10 passed in 5.46s`
- No-approval compatibility selector: `1 passed in 0.56s`
- Ruff: passed
- mypy: passed
- `git diff --check`: passed
- Full/browser suites not run.

Evidence: [durableORCHevidence](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D72-approval-security-1726/durableORCHevidence>)

No review edits were made; unrelated pre-existing staged changes were preserved. `DONE` and commit message are recorded. Proposed log entry: `F/D72 approval security review PASS; authenticated candidate/publication/scope/base binding and five pre-write tamper controls verified; original 924 behavior preserved; inherited opaque approval_id limitation recorded.`