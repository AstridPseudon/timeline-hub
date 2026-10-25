## Verdicts

- **A — PASS_SOURCE:** Only the fresh v2 disjoint-landing literal changed from `rebased` to `merged`. Historical retry assertions remain `rebased`; all other predicates are AST-identical.
- **B — PASS_SOURCE:** Runtime pin is captured once and strictly verified as `6634a17f…` / tree `47b37671…`. Frozen schema constants and behavior body remain identical.

Evidence: [protected-review.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-owned-oracles-review-0403/evidence/protected-review.md)

Checks passed:

- In-memory AST parse/compile, parent and candidate.
- Ruff, parent and candidate.
- Mypy shadow-file checks, parent and candidate.
- `git diff --check`.
- Runtime lock/object/tree identity verification.
- Worktree remains clean.

No pytest, collection, fixtures, services, or behavior execution was run per source-only scope. Commit message and `DONE` marker created. Recommended next step: merge candidate `9dc6128d5e` and run the required exact MAIN proofs.