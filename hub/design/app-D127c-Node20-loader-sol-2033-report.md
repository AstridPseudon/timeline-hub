**Cause proven; strict F002 acceptance remains blocked.**

- Node20’s assertion-message parser repeatedly reparses an unchanged window after a zero-byte read. TSX’s minified callsite coordinates trigger this on the original TypeScript file.
- The supported `tsx/cjs/api` route executed all **three exact controls** under Node20.19.4: **3 passed, 0 failed, 0 intended skips**, in 1.38s. Whole-file output includes **four nonmatching skips**, preserved explicitly.
- Outside service `13179` stopped at the **5 GB snapshot disk guard** before executing controls. No retry.
- Independent event verification passed. Repository source stayed unchanged; prior Node22 and Runtime61 evidence was reused.

[Exact commands and results](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-D127c-Node20-loader-sol-2033/evidence/commands-results.md) · [Validation and prerequisites](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-D127c-Node20-loader-sol-2033/evidence/validation.md)

Required evidence, commit message and `BLOCKED` marker are written. Closure needs snapshot disk headroom and an authorized route satisfying literal global zero skips. D130 holds remain unchanged.