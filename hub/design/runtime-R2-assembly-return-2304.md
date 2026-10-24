Implemented freshness checks in `timeline_commit_store.py` and 42 provider-path attack cases. Each graph lookup rechecks exact consumed SQL results and physical CAS bytes before deferred replay and before return. Lock placement and graph traversal remain unchanged.

Validation:

- Required five-file command: **235 passed**, zero failures/errors/skips.
- Authentication/ABI/history neighbors: **192 passed**.
- Actual Agent N2/4/8 previews: **3 passed**, with deep result equality against base732.
- N4 callback regression against bad9: **failed as expected** because stale history escaped.
- Compile and `git diff --check`: passed.
- Ruff/Pyright: zero new source/rule findings; 11/74 existing diagnostics remain.

| N | Node checks | Closure reads | Replay checks | Wall / CPU |
|---|---:|---:|---:|---:|
| 2 | 2 | 4 | 2 | 0.021s / 0.020s |
| 4 | 4 | 8 | 4 | 0.042s / 0.041s |
| 8 | 8 | 16 | 8 | 0.122s / 0.109s |

Base732 at N8 used 128 node checks and 256 closure reads.

[Exact commands and environments](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-R2-assembly-return-sol-2304/evidence/commands.json>) and neighboring evidence retain XML, logs, exits, scripts, hashes and resolved test-setup failures. The original failure report and raw witness remain preserved. The missing temporary attack script was recovered from reviewer transcript text; its blob hash matches that transcript.

Commit message and `DONE` are written. No full/core/browser/gate/original P4 run occurred. No implementation blocker remains; **adoption stays held pending the required independent Luna review**.