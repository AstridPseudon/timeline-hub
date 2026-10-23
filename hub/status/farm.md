<!-- farm | 2026-10-23T10:09:31Z | dispatcher heartbeat 3s | live 0 (sol 0, luna 0, other 0) | busy30 0 | status age 2m -->
# farm board, 2026-10-23 (round start; disk 21 GB free, above the 15 GB floor)
| ID | task (short) | model | needs | status | worker | proof (test id / result on the integrated head) | commit |
|---|---|---|---|---|---|---|---|
| F-H0 | upstream baselines (runtime/agent/app) | claude | none | todo: no farm-*.md result exists and no tf- worker has ever run; not executed | none | none | n/a |
| F-H6 | integrated full suites + tour + journey | claude | P1 GO, A2/A3 | todo: not run. Header: farm was down and Proof ran P1/P3 on the test service | none | none | n/a |
| F-H9 | same, at H9 | claude | P1 GO | todo: not run | none | none | n/a |
| F-app-full | App full suite on integrated head (orchestrator priority 1) | test service | none | doing (queued 10:07Z) | test service | app-full-1023100721-23537 | pending |
| F-comp-full | Composition full suite (priority 3) | test service | none | doing (queued 10:07Z) | test service | composition-full-1023100726-4261 | n/a |
| F-EXACT8 | agent heavy-journey failures (2 sigterm, 6 quick_run) | claude | n/a | Agent owns it as farm-down fallback (peer 09:19Z): sole id agent-targeted-1023091523-8962. Farm must NOT dispatch a copy | none | Agent's id pending | n/a |
| F-final | final run + delivery-build dry run | claude | all lanes | todo | none | none | n/a |

Blockers:
- P1 is NO-GO (App/Proof peers, through 02:13Z): no mounted A2 chain selector exists, so no honest H3/H6 chain run can be requested. Owner: App/Proof.
- Peer asks to acknowledge: the v1 checkpoint12 and gate6 requests are VOID (orchestrator 22:55Z). I'm not serving them.
- Heavy-run capacity: 0 of 2 in use. Ready to take a run the moment one is named with an exact SHA and command.

Next ready: none until a lane names an exact SHA and command. I'll serve the Agent EXACT8 result only if the Agent's id fails for infrastructure reasons.
