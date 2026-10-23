# ap2-A2-undo-failover-0725: mounted guarded Undo/Redo

Completed the bounded continuation of WIP 8ff4ab537. The mounted production history hook now submits timeline.inverse through the existing durable outbox and Runtime client, adopts Runtime canonical results, and reconstructs targets from authoritative matching-pair history after saves and reloads. Durable loading/retry/conflict states cannot fall back to local snapshots; failures remain visible.

Final scoped evidence: 8 Vitest files / 112 tests PASS; root, App and Node TypeScript checks PASS; scoped ESLint PASS; diff check PASS; normal Runtime 34eac004 producer lock PASS; exact819acf Composition graph 80/80 archive bytes and public generated subpaths PASS. Shared installs remained read-only.

Broader targeted run: 244/245 tests passed. Unchanged dataProvider.test.ts:1224 managed placement test expects an absolute runtime.test object URL and receives /v1/objects/..., reproduced alone on final source. No placement fix, baseline/allowance change, or test weakening. Full exact commands, logs, decisions, and limits: [WORKERreport.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-A2-undo-failover-0725/WORKERreport.md).

The new mounted tests use real RuntimeDataProvider and generated client/history calls over an in-memory transport. They prove App payload, receipt adoption, exact lost-ACK replay, reload, and structured refusal handling; they do not execute the Python guard scan or live Runtime authentication. No browser/journey/service/build/full/remote request was made.

Next: independent Luna review. App home owns the final port to a fresh current branch with own commits only, including the inherited useTimelineState wiring. Do not merge this stopped-WIP ancestry as a substitute. Worker made no git mutation.
