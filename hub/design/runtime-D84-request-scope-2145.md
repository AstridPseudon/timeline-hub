Implemented D84a request-scoped replay reuse. Preserved 2142 contained no source changes. Fresh authority checks, acceptance locking, head CAS and receipt behavior remain intact.

At N=2 with three commands, paired genuine-daemon measurements showed:

| Check | Parent | Candidate |
|---|---:|---:|
| Full recorder replay | 21 | 3 |
| Historical traversals | 16 | 2 |
| Capture-document checks | 144 | 32 |
| Median wall time | 0.645 s | 0.242 s |

Raw `_verify_accepted` calls remain **21** because fresh database checks still run. Retries and reopened-daemon requests verified afresh. No flat-scaling or original-budget claim.

Validation passed:

- Targeted 16-file union: **1,038 passed**, exit 0. [Exact command](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-D84-request-scope-sol-2145/evidence/final-union.command>).
- Final scope tests: **13 passed**; existing ABA controls: **3 passed**.
- Independent security review: **PASS**.
- Ruff/Pyright: **zero new diagnostics**; compile and diff checks passed.

[Evidence, logs, XML, commands and blob hashes](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-D84-request-scope-sol-2145/evidence/measurement-notes.md>).

No blockers. Commit message and `DONE` written; no merge or release performed. Step 2 remains unimplemented. Next: normal release queue, then existing owners’ P4 ten-note and isolated App element runs.