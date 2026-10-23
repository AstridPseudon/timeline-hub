<!-- farm | 2026-10-23T10:40:19Z | dispatcher heartbeat 10s | live 0 (sol 0, luna 0, other 0) | busy30 1 | status age 5m -->
# farm board, 2026-10-23T10:25Z (disk 21 GB free, above the 15 GB floor)
| ID | task (short) | model | needs | status | worker | proof (test id / result on the integrated head) | commit |
|---|---|---|---|---|---|---|---|
| F-H0 | upstream baselines | n/a | none | superseded by orchestrator priorities 10:02Z (Agent and Runtime ran their own full suites); App upstream 7c17cc9d9 baseline only if the classifier needs it | none | none | n/a |
| F-app-full | App full suite on integrated head | test service | none | merged-head run DONE: FAIL, 89 failed / 18706 passed, 20 files, exit 1, 908s | test service | app-full-1023100721-23537 (app tree 87c00cb43a07, `npm test -- --maxWorkers=3`) | n/a |
| F-app-classify | classify the 89 App failures (real / pre-existing / env / D14) | Luna high | F-app-full | DONE 10:34Z; peer message sent to App (design/peer-farm-to-app-20261023T1036-app-full-failures.md). 34 stale-fixture, 50 real (several probable), 3 env, 2 unresolved, 0 D14, 0 confirmed pre-existing | tf-app-classify | design/farm-app-full-classification.md | n/a |
| F-app-rerun | App full re-run after fixes | test service | App names a SHA with fixes | gated:app-fixes | none | none | n/a |
| F-comp-full | Composition full suite | test service | none | DONE: PASS | test service | composition-full-1023100726-4261 | n/a |
| F-EXACT8 | agent heavy-journey failures (2 sigterm, 6 quick_run) | n/a | n/a | Agent owns it (peer 09:19Z), id agent-targeted-1023091523-8962. No farm copy | none | Agent's id pending | n/a |
| F-H6/H9 | integrated suites + P2 tour + P3 journey | test service | P1 GO, A2-undo, A2-move-reads | gated:P1 | none | none | n/a |
| F-final | final run + delivery-build dry run | test service | all lanes | todo | none | none | n/a |

Blockers:
- P1 is NO-GO (App/Proof peers): no mounted A2 chain selector, so no honest P2/P3 or chain run can be requested. Owner: App/Proof.
- The v1 checkpoint12 and gate6 requests are VOID (orchestrator 22:55Z); I'm not serving them.
- Provisional triage from the log, to be confirmed by tf-app-classify: ~25 providerCompatibility.runtime failures all hit 'retired mutable timeline GET must not be used' (src/test/fakeWorkspaceRuntime.ts:496); runner.test.ts (12), semanticGestures.test.ts (~25), VideoEditorPage P2-L04 (3), vendoredTimelineCompositionAliases (3) and others. Real ones go to App as peer messages once classified.

Next ready: after classification, peer messages to App; the P2/P3 runs when the A2 gates merge.
