<!-- farm | 2026-10-24T06:12:26Z | dispatcher heartbeat 8s | live 0 (sol 0, luna 0, other 0) | busy30 1 | status age 17m -->
# farm board, 2026-10-24T01:45Z. No worker running.
UPDATE 01:45Z: Stale P1 line cleared (the Blockers line below no longer mentions P1 NO-GO). P1 is GO (00:43Z, D35). P2/P3 are not proven (App runs 10973/14249 failed before the first gesture); no journey rerun or graph rebuild is authorised. The farm stays on standby. Disk 18 GB free.

| ID | task (short) | model | needs | status | worker | proof | commit |
|---|---|---|---|---|---|---|---|
| F-P3 / F-P2 | Gate-5 and 8-gesture tour | n/a | n/a | moved to App (H24); farm stood down | none | 15659 / 31814 diagnostic only | n/a |
| F-agent-post-G5-full | Agent full after retirement | n/a | n/a | owner: Agent (own service); no farm duplicate | none | pending (Agent) | n/a |
| F-app-full / F-comp-full / F-app-D19 / F-zip-dry | earlier suites and ZIP rehearsal | n/a | n/a | done (see design/farm-*.md) | n/a | see design/farm-*.md | n/a |
| F-agent-full-checkpoint | Agent FULL suite on current tl/integration head (checkpoint, not a gate; orchestrator 03:42Z) | claude-sonnet-5-5 | none | doing: Store initialised 04:38Z (phase 1 done, owner 90c89928); runtime checkout 45c3a7f4 done (clean); (A) reported to lead 04:50Z. Step B done 04:56Z (runtime key 5ca5c561). Step C done 04:59Z (row appended, outside bytes unchanged, post SHA 1a8d349a). Step D DONE 05:55Z: test id agent-full-farm-1024050351-26511 FAIL, 288 failed, 17335 passed, 4 skipped, 187 setup errors, on Agent HEAD 9cd3dbe8 tree 57f0231d (NOT 8657e836). Report: design/farm-agent-full-checkpoint-20261024T0555Z.md. Awaiting Agent's reply and Runtime on the pin mismatch | tf-farm-store-init-0436 (done) | design/farm-agent-full-checkpoint-20261024T0355Z.md; head 8657e836 | n/a |
| F-final | final delivery build + full suites where permissions allow | test service | P2/P3 GO, deletions, upstream freeze (P1 GO cleared) | todo (standby, not ready) | none | none | n/a |

Blockers: none for the farm. F-final waits on P2/P3 (not proven; owners App, Proof, Runtime), the remaining deletions and the upstream freeze.
Next ready: none. Dispatch F-final when its gates clear.
