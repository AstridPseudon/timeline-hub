<!-- farm | 2026-10-24T10:41:45Z | dispatcher heartbeat 7s | live 0 (sol 0, luna 0, other 0) | busy30 0 | status age 51m -->
# farm board, 2026-10-24T09:50Z. No worker running.

| ID | task (short) | model | needs | status | worker | proof (test id / result) | commit |
|---|---|---|---|---|---|---|---|
| F-D49 checkpoint | One corrected Agent full run (agent full-farm) on Agent 9cd3dbe8 with Runtime 1d9ddba5 | test service | a v3 preflight that passes | blocked:Runtime (preflight failed) | none now | Run 1 (26511, old row): FAIL, 17335 passed, 288 failed, 187 setup errors. v3 preflight (tf-v3-preflight-0900, 09:05Z): FAIL at the row's import line, no module banodoco_timeline_schema; xdist also absent in the child | n/a |
| F-D49 setup | Store, runtime registration, managed child, v3 row | Claude and Codex | none | done except the preflight fix: Store init 04:38Z, checkouts 9cd3dbe8 and 1d9ddba5 clean, Remotion registration reused (key 5ca5c561), child venv-agent-child-farm-v3-9cd created 08:31Z (lead), v3 row installed 08:48Z (registry SHA e4edb022) | tf-farm-store-init-0436, tf-farm-row-append-0457, tf-v2-row-install-0738, tf-v3-row-install-0852 | python -I import of runtime_protocol in the child works | n/a |
| F-trace-export | Failure excerpts for Agent (88 + 8 failures, 187 setup errors) | claude-sonnet-5-5 | none | done 07:15Z | tf-trace-export-0705 | design/farm-trace-export-0705-* | n/a |
| F-P3 / F-P2 | Gate-5 and 8-gesture tour | n/a | n/a | moved to App; farm stood down | none | 15659 and 31814 are diagnostic only | n/a |
| F-final | Final delivery build and full suites where permissions allow | test service | P2/P3 GO, the remaining deletions, the upstream freeze (P1 GO is cleared) | todo, on standby, not ready | none | none | n/a |

Blockers: (1) Runtime owes a maker or distribution correction (or a corrected row import list) so the v3 preflight can pass; Runtime says Sol0853 finishes first, then a Luna with independent review, then the lead makes ONE changed child request. I can't unblock this. (2) The installer's backup of the registry (/tmp/w-6a625438a2/suites-20261024T084820.062320Z.conf) can't be hashed from my session; expected SHA e01da004. (3) F-final waits on P2/P3, deletions and the freeze.
Next ready: none. After Runtime's corrected child: lead's request-child-venv, then preflight, then the ONE checkpoint (only on PASS).
