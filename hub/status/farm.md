<!-- farm | 2026-10-24T14:05:31Z | dispatcher heartbeat 4s | live 0 (sol 0, luna 0, other 0) | busy30 0 | status age 104m -->
# farm board, 2026-10-24T12:25Z. STOOD DOWN (D56.3). No worker running; no new dispatches.

Orchestrator 12:27Z, owner-approved (D56.3): F-final and the ZIP move to main, so the farm stands down. Machinery idle, daemons stay up, until the orchestrator releases the farm.

| ID | task (short) | status | last result |
|---|---|---|---|
| F-D49 checkpoint | One corrected Agent full run (agent full-farm) | stood down (D56.3), not run | Run 1 (26511, old row): FAIL, 17335 passed, 288 failed, 187 setup errors. v3 preflight (tf-v3-preflight-0900, 09:05Z): FAIL, no module banodoco_timeline_schema in the child; xdist absent |
| F-D49 setup | Store, runtime registration, managed child, v3 row | stood down (D56.3) | Done through the v3 row install at 08:48Z (registry SHA e4edb022); left as is, no preflight fix, no row change |
| F-trace-export | Failure excerpts for Agent | done 07:15Z | design/farm-trace-export-0705-* |
| F-P3 / F-P2 | Gate-5 and 8-gesture tour | stood down (moved to App) | 15659 and 31814 are diagnostic only |
| F-final | Final delivery build and full suites | stood down (D56.3): moves to main | none |
| F-zip-dry | ZIP rehearsal rerun | stood down (D56.3): the ZIP moves to main | earlier steps green, see design/farm-zip-dry-report.md |

Blockers: none for the farm; it is idle by order. Left as found: the farm registry and Store (bench-store), the installed v3 `agent full-farm` row, the child venv, and both pins; nothing was reverted. The installer's registry backup (/tmp/w-6a625438a2/suites-20261024T084820.062320Z.conf, expected SHA e01da004) could not be hashed from my session. Worker tf-v2-preflight-0747 and others left small scratch folders under workers/.
Next ready: none.
