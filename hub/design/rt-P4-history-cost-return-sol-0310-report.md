**No source change. P4 remains blocked.** Completed the finite ten-note SDK/provider control and demonstrated multiplication inside each commit POST:

| Undo | SQL executions | Graphs rebuilt | Record validations | Replay keys |
|---|---:|---:|---:|---:|
| 1st | 5,972 | 60 | 61 | 41 |
| 2nd | 26,442 | 146 | 275 | 253 |
| 3rd | 60,375 | 278 | 598 | 574 |

Each POST performed only **one pure replay validation**. Within one authoritative read, the third undo rebuilt 28 graphs and validated six distinct publications 64 times.

The precise seam is `_verify_accepted` rebuilding completed graphs within the same `history_read_scope`. Safe reuse remains unproved under the required fresh SQL/CAS and end-check guards, so **no candidate was authored**. [Counts, source trace and unresolved boundary](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-P4-history-cost-return-sol-0310/evidence/source-trace.txt).

Validation:

- Finite control: **1 passed**; refined request-segmented control: **1 passed**, both with `--timeout=45`.
- Initial collection failed on a test-package namespace collision; corrected diagnostic imports resolved it.
- Scoped Ruff: **11 existing diagnostics**; Pyright: **74 existing errors**, exact prior-baseline identities.
- `git diff --check`: passed; worktree clean.
- [Exact commands, results and limitations](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-P4-history-cost-return-sol-0310/evidence/commands.json).

Runtime remains `6634a17f`; store blob remains `60628ab8`. Prior 0301 evidence is untouched. No original P4, full suite or four-file candidate acceptance ran.

Recommend reviewing the demonstrated reuse boundary before another source proposal. Commit message and `DONE` written.