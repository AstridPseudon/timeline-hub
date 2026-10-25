## Report

Completed F-D87 as source-only evidence. No product/test/helper files changed; no new test was needed.

- 24/24 native-batch selectors mapped, plus the separate checkout parameter case.
- Current capability gaps: 0; six other checkout cases remain live.
- Exact ZIP migration handback text authored.
- Manager ledger and Runtime README unchanged.
- Evidence: [appendix](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D87-ledger-0007/evidence/d87-native-batch-retirement-appendix.md>) and [acceptance record](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D87-ledger-0007/evidence/source-acceptance.md>).

Checks:

- AST mapping/compile: PASS.
- Mypy: exit 0.
- Ruff: exit 1 with 11 pre-existing F811 diagnostics; source hashes equal HEAD.
- `git diff --check`: exit 0; worktree clean.
- Pytest, services, builds, and full suites were not run per scope.

Commit message written to the required path. `DONE` created. Protected review remains required before manager ledger publication.