## FAIL — D108 source audit

- Applied manifest verified: all four applied trees/source blobs match; manifest SHA-256 recorded.
- Agent: 104 missing predicates; 96 exactly cited/cleared, 8 restore-needed.
- Runtime: 10 missing predicates, all unmapped under the exact-source-hash rule.
- App WelcomeConnection tests and Agent installer coverage retained.
- No skip/xfail additions, parameter drops, or direct `==`→membership weakening found.
- Build/render/ZIP remain pending; App/Composition TypeScript predicate census is unverified.

Tests were not run per instruction. Source-only `git apply --check` and AST parsing passed.

Evidence: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-F-D108-reverse-audit-0645/evidence`

`DONE` created. `commitF-D108-audit` message written; no product changes.