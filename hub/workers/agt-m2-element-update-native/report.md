Migrated the helper to one native command batch; removed whole-candidate publication and legacy mirror writes. Deleted 58 helper lines.

- Local tests: **204 passed, 1 strict xfail**.
- Central integration: **29 passed**.
- Ruff and diff checks passed.

**Blocked:** element-only updates with empty params need native retained-declaration validation without a parameter write. The success expectation remains intact.

Wrote `BLOCKED`, `commit-msg`, and [report.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-element-update-native/report.md) with exact commands, results, decisions, and recommended follow-up.