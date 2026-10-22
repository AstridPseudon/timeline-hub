<!-- viewing | 2026-10-22T22:17:05Z | dispatcher heartbeat 0s | live 1 (sol 0, luna 1, other 0) | busy30 1 | status age 1m -->
# viewing board, 2026-10-22T22:16Z
| ID | task (short) | model | needs | status | worker | proof (test id / result on the integrated head) | commit |
| --- | --- | --- | --- | --- | --- | --- | --- |
| V1-prep | schema source and drift inventory (read-only) | Luna high | H0 | doing | vw-V1-schema-inventory | pending inventory | — |
| V1 | open meta namespaces and ignore behavior | Luna high | C0 APPROVED, U1 | blocked:runtime | — | not run | — |
| V3 | one commit-named Composition artifact and consumer pins | Luna high | U2, U3 | blocked:agent+app | — | not run | — |
| V4 | optional stale dirs/copy/block deletions | Luna high | U2, U3 (lane brief) | blocked:agent+app | — | not run | — |

Blockers: Runtime: C0 header is NOT YET APPROVED; U1 completion not recorded here. V1 implementation waits for both.
Blockers: Agent/App: U2/U3 completion not recorded here; V3/V4 wait for merged baselines.
Next ready: V1-prep dispatched; V1 after C0 approval + U1; V3/V4 after U2 + U3.
V2.1 restart: no previous STATUS existed. INBOX read through 2026-10-21T12:43:40Z; all entries predate the restart and are archival context, not new task authorization. Unified rendering/gate 6 is deferred by PLAN v2.1.
