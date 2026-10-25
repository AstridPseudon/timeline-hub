## PASS_SOURCE

Reviewed author `d1b1d10191` against parent `ac9a00f18e1d90a9fdd61938e3bfc3862552e89a`.

- ID6: `clip.anchor` is genuinely registered and used by production execution; fresh JSON-only compile, identity, timing, restart, and no-history guards remain unchanged.
- ID8: `invalid_anchor` maps to C0 `status: "invalid"` / HTTP 422; half-open predicate, reason, head/no-write, and undo assertions remain unchanged.
- ID9 remains exactly `status == "refused"`.

Checks passed:

- AST/in-memory compile and normalized AST conservation
- Ruff parent/candidate
- Mypy parent/candidate shadow comparison
- `git diff --check`

No tests, collection, fixtures, helpers, services, or functions were executed. Worktree is clean; no blockers. Evidence: [source-review.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-word-oracle-review-0320/evidence/source-review.md).

Only the original author should merge. Functional qualification remains separate; this is not behavioral credit.