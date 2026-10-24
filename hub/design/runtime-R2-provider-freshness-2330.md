Implemented the R2r/P4 provider freshness repair in three allowed files. The existing SQL/CAS collector now remains active through complete port reads, including pins, ancestry, history, closures, head checks and result copying. Bounded graph assembly remains intact.

Validation:

- Required five files: **260 passed**—original 235 plus 25 added cases; all original 42 provider attacks retained.
- Neighbors: **192 passed**.
- Port/coordinator controls: **123 passed**.
- Exact independent witnesses: **2 passed**. Preserved RED controls: bad9 fails both; 7627 fails the late pin-read witness.
- Actual Agent N2/N4/N8 previews: **3 passed**, with deep reply equality against released732. N8 record checks remain **128→8**, closure reads **256→16**; CPU **0.573→0.073s**, wall **0.640→0.073s**.
- Ruff/Pyright: **zero new diagnostics** versus732. Compile and diff checks passed.

[Exact commands and environments](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-R2-provider-freshness-sol-2330/evidence/commands.json>) accompany preserved scripts, XML, logs, exits and source hashes. Commit message and author `DONE` marker are written. No git writes or merges performed.

Independent final-review dispatch failed because the agent tool could not load its thread context. **Final security PASS and normal-home validation remain required before merge.** Full/core/browser/original-P4 runs were not performed.