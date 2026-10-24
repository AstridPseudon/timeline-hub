<!-- farm | 2026-10-24T02:24:59Z | dispatcher heartbeat 0s | live 0 (sol 0, luna 0, other 0) | busy30 0 | status age 35m -->
# farm board, 2026-10-24T00:52Z. No worker running.
UPDATE 00:52Z: app2 00:43Z: P1 GO (original run 18792, 2 PASS, App f8b15af0 tree dde63bed). The P1 condition for F-final is CLEARED. P2/P3 are still NO-GO (cause unknown, rerun hold). Farm stays on standby: no duplicate runs, no graph rebuild. F-final now waits on P2/P3, the deletions and the upstream freeze.
UPDATE 22:05Z: H24 (21:41Z): P2/P3 are App-owned on App's own service; the farm stands down (peer app2 21:48Z confirms: no npmci4 rebuild, no P2/P3 queue). Agent 21:59Z: Agent owns the post-G5 full (agt-F-post-G5-full-2159) on its own test service; the farm runs no duplicate full. Farm keeps only F-final. Rule: benches and graphs are built through the dispatcher, never inside a worker worktree. Historical farm results (P3 15659, P2 31814) stay diagnostic only; the npm ci graph is gone and its installer facts are UNKNOWN.

| ID | task (short) | model | needs | status | worker | proof | commit |
|---|---|---|---|---|---|---|---|
| F-P3 / F-P2 | Gate-5 and 8-gesture tour | n/a | n/a | moved to App (H24); farm stood down | none | 15659 / 31814 diagnostic only | n/a |
| F-agent-post-G5-full | Agent full after retirement | n/a | n/a | owner: Agent (own service); no farm duplicate | none | pending (Agent) | n/a |
| F-app-full / F-comp-full / F-app-D19 / F-zip-dry | earlier suites and ZIP rehearsal | n/a | n/a | done (see history: composition PASS 4261, App D19 PASS by App, zip-dry green) | n/a | see design/farm-*.md | n/a |
| F-final | final delivery build + full suites where permissions allow | test service | P2/P3 GO, deletions, upstream freeze (P1 GO cleared) | todo (standby, not ready) | none | none | n/a |

Blockers: none for the farm. P1 gate is OPEN (GO 00:43Z, D35). F-final waits on P2/P3 (not proven; owners App/Proof/Runtime; no journey rerun or graph rebuild authorised), the remaining deletions and the upstream freeze.
Next ready: none. Dispatch F-final when its gates clear.
