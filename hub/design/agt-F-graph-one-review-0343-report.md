# F-D86 Source Review — `FAIL_SOURCE`

The candidate does not reach genuine Runtime acceptance. `DetachedRealm.call()` invokes Agent’s `RuntimeCommitService` with test-local `DetachedPort`; acceptance is synthesized by `DetachedPort.accept()` into in-memory `realm.entries`, not Runtime’s coordinator, registered provider, authorization, SQLite store, or authoritative history.

Preserved: both root assertions, original graph inputs/opaque values, refusal, identity-collision, and no-write guards.

Checks:

- AST parse: PASS
- Ruff candidate: PASS
- Ruff parent baseline: PASS
- Mypy candidate: PASS
- `git diff --check`: PASS
- Tests/services/full suites: not run, per source-only instructions
- Worktree: unchanged

Evidence and D72 proposal: [source-review.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-graph-one-review-0343/evidence/source-review.md)

No blockers beyond required candidate rework: setup must use the registered Runtime provider and authenticated durable history before re-review.