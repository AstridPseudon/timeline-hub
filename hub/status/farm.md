<!-- farm | 2026-10-25T12:48:26Z | dispatcher heartbeat 3s | live 0 (sol 0, luna 0, other 0) | busy30 0 | status age 5m -->
# farm board, 2026-10-25T12:45Z. Active (D124) for ONE purpose: host Agent's heavy runs. No worker running.

D124 (lead, 12:41Z) un-stands-down the farm for Agent's `agent-core-full` runs only. Everything else stays stood down (D56.3). Disk 15 GB free (floor 14).

| ID | task (short) | status | notes |
|---|---|---|---|
| F-agent-core-full | Run `agent-core-full` (unfiltered Agent core suite, design/agent-core-full-command.md) on Agent's current head plus merged batches; publish `core open: N` with the outcomes file to design/ and the Agent INBOX; repeat per batch | active (D124), waiting for the Agent lead to name the head/batch | Needs: Agent lead names head/batch; the farm's own correctly keyed profile built through the normal installer (the lead issues request-runtime / request-child-venv; workers never call dispatcher tools); path bindings adapted from MAIN's immutable checkouts to the farm's request-checkout receipts. Tell the lead before each run so disk can be freed |
| F-D49 checkpoint | One corrected Agent full run (agent full-farm) | stood down (D56.3); superseded for now by F-agent-core-full | Last results: run 26511 FAIL (17335 passed, 288 failed, 187 setup errors); v3 preflight FAIL (no banodoco_timeline_schema, no xdist in child) |
| F-D49 setup | Store, registration, managed child, v3 row | stood down (D56.3), left as is | Store at bench-store, v3 `agent full-farm` row installed (registry SHA e4edb022), child venv-agent-child-farm-v3-9cd |
| F-trace-export | Failure excerpts for Agent | done 07:15Z | design/farm-trace-export-0705-* |
| F-P3 / F-P2 | Gate-5 and 8-gesture tour | stood down (moved to App) | diagnostic only |
| F-final / F-zip-dry | Final delivery build, full suites, ZIP rehearsal | stood down (D56.3): moved to main | none |

Blockers: (1) Waiting for the Agent lead to name the head/batch for `agent-core-full`; I start nothing before that. (2) The existing child and Store were built for Agent 9cd3dbe8 / Runtime 1d9ddba5 and the old tuple; D124 requires a profile correctly keyed for the NAMED head, built through the lead's normal requests. (3) The installer's registry backup (/tmp/w-6a625438a2/...) can't be hashed from my session.
Next ready: none until the Agent lead names the head/batch.
