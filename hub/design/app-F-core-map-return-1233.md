## App F core-map factual return

- Read-only review completed on `cca3deb361e8fbbc62ddf491d5fd09c7e542b99f` (tree `911956d49c...`); worktree remains clean.
- No product, test, config, ledger, source, fetch, browser, or full-suite changes.
- Commit message and `DONE` marker created.

### Core map

Production save reachability is:

`useTimelineState` → `useTimelineSave` → `createLocalSaveSession` / outbox → `RuntimeDataProvider.commitTimeline` → Runtime client.

Existing controls cover:

- Save/outbox/recovery: `commitOutbox.test.ts`, `localSaveSession*.test.ts`, `timelineCommit.test.ts`, `command-outbox.spec.ts`, P1 chain.
- Undo/redo/history: `useTimelineHistory*.test.ts`, `timelineLocalSaveHandoff.test.ts`, Gate-5 support tests.
- Split/trim: local-save split→trim, ordinary/clip trim, parent split/trim, mounted public trim.
- Move: ordinary move, clip move capture/primitives, semantic gestures.
- Placement: placement service/requester, native placement, auto-capture.
- Occurrence/media: occurrence duplicate/media capture and gesture tests, P2 element/asset and popup journeys.

`commitSession*.test.ts` and `createTimelineCommandSession` are supporting controls only: no non-test production import reaches that session in the current tree. No removal is proposed. The mounted production caller uses `localSaveSession` and the durable outbox.

### Historical 19570 classification

All nine failed files are now either fixed or dead-scope:

| Group | Current receipt/proof | D54a classification |
|---|---|---|
| Six retired `complete_task` edge files | `664a8a08...` retirement, included and independently verified by 1157 at `5a9ff97cf...` / tree `3311baa...`; 20/20 task-route tests and 1/1 edge neighbor passed | D52 dead-scope |
| Retired TS runner bridge | `3403a1d0...`, exact five-path retirement verified by 1146/1157; remaining Vitest union 608/608 | D52 dead-scope |
| `threeProductsAuthoring.test.ts` two fresh-worker failures | `7886f11a...`; targeted authoring result 3/3; included in 1157 exact packet review | Fixed environment/fixture setup |
| Home stale CTA | `e0a293703...`; Home lifecycle result 13/13, current 1157 packet verified | Fixed test-oracle/harness mismatch; upstream classification **UNKNOWN** |

The Home source blob matched frozen upstream, but the prior report incorrectly called the failure pre-existing without an actual same-node upstream execution. Only source identity is established; no upstream PASS/FAIL is claimed. If a matching upstream run later passes while ours fails, D54a requires fixing or reverting it regardless of non-core status.

Count correction: 1146 and 1157 each report 20/20 task-route tests plus 1/1 edge neighbor = 21 controls, not 33. The separate 33/33 edge result belongs to the historical targeted edge configuration and is not an 1146/1157 count.

### Full-suite status

The existing producer `app-U3b-F-reviewed-join-1146-full-1024120556-16138` remains the sole full producer. It is still `running`, snapshot tree `3311baa...`, with no terminal summary or exit. No partial output was classified and no new full run was requested.

### Evidence

No tests were run by this worker, per the readonly/no-new-suite brief. Existing evidence reused:

- 1146: 23/23 Node controls, 608/608 Vitest tests, 20/20 task routes, 1/1 edge neighbor, TypeScript and ESLint passed.
- 1157: additional 72/72 tests, exact source/provenance checks, and full v2 request/reply preservation review.

The v2 request and `{data, receipt}` accepted/merged/conflict/invalid/dry-run contract remains unchanged.