# D66 reverse-diff report

Completed the bounded static reverse census against upstream `9244377` and current `d27b6601`.

- Upstream XML: 12,517 cases / 9,857 AST identities.
- Current source: 12,290 AST identities.
- Retained collection1443: 8,665 nodes across 386 files.
- Missing scope: 362 cases / 204 identities.
- Exact renames: 0.
- Ledger-deleted: 137:
  - D06: 89
  - D05: 38
  - VW dead inspector: 5
  - D07: 3
  - D10: 2
- `RESTORE_NEEDED`: 225 cases across 66 live files.

Same-name functions were not accepted as renames unless body, parameters, and decorators matched exactly. Every restore row preserves the exact upstream path, blob, selector, source span, parameters, body hash, and compatibility metadata.

Evidence:

- [Summary](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D66-reverse-diff-1527/evidence/d66-reverse-diff-summary.md>)
- [Detailed JSON](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D66-reverse-diff-1527/evidence/d66-reverse-diff.json>)
- [TSV inventory](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D66-reverse-diff-1527/evidence/d66-reverse-diff.tsv>)

Validation:

- JSON row/body/ledger validation: `PASS`
- `git diff --check`: `PASS`
- No tests, collection, full suites, HTTP/browser, installs, or source acquisition run per instruction.
- No source or test files changed; the three-file restore allowance remains unused.
- Production caller seam inventory was preserved from collection1443, but caller qualification remains for the next restore worker.

Commit message written and `DONE` created.