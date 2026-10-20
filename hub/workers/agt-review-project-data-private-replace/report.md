# Review report

**Verdict: HOLD qualification and App cutover.**

- Candidate: `b5984ac0c7e2aa9de710175188cef9a602c48c3d`
- Tree: `d4a9474e20b7eca2b36ba80f5fa7204b5dc3f8fb`
- Private schema SHA-256: `b02cd3a30a63647cd4a31bb8426c049d02ac3ddd168af5f7847a735eb549db16`
- Counts: 56 schema definitions, 30 composed clauses, 28 registered handlers.

Confirmed exact storage path `parent.config.app[extension_id][key]`, closed `select:"parent"`/`mode:"replace"` arguments, no catalog/TargetKey/table/endpoint, opaque-key preservation, ordered source/source-map batches, strict inverse/ABA guards, and no whole-parent replacement.

Blocking findings:

1. Candidate key validation is not App-compatible: whitespace, reserved outer keys (`__proto__`, `constructor`, `prototype`), and oversized UTF-8 keys are accepted by schema validation; App requires trimmed keys, a 256-byte limit, reserved-name rejection, and additional size/count limits.
2. Concurrent writes to disjoint keys under a previously absent/empty/null target namespace refuse with `dependency_changed`; this avoids silent deletion but does not yet satisfy automatic disjoint-key rebase.
3. Runtime pairing and App native cutover are absent; App must retain the compiler-canary and legacy snapshot fallback.

Tests:

- Focused M2/M1/scalar suites: `209 passed`
- M2 + composed schema: `16 passed`
- M2 only: `11 passed`
- Ruff: passed
- `git diff --check`: passed
- Frozen inventory failures: original candidate evidence reports `4`, private-only and expected; frozen files remain unchanged.
- No Runtime, App/browser, schema-generation, or full suite run.

Precise proposals are recorded in [report.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-review-project-data-private-replace/report.md). Commit message was written to the requested path; `DONE` created. Worktree remains clean.