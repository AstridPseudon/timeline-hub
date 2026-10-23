# P1/A2 poll-owner capture boundary: bounded causal result

Added three controlled schedules to the existing mounted `useTimelineSave.test.tsx`; production source is unchanged. **13 focused tests PASS. P1/H3 remains FAIL/NO-GO**: this is unit causal evidence, not a live Runtime refusal or a recovered explanation of service28486.

Base: `0cdc76782833d594776452e07706acb406c51553`, tree `654a66946da8a4da65248576a9eb5e32a9e8d382`. Only `src/tools/video-editor/hooks/useTimelineSave.test.tsx` changed (+176/-2). Existing setup gains a typed query and poll/rerender entry point. Every pre-existing test body/assertion from the first original test through EOF is byte-for-byte identical to HEAD (verified by script). Original browser spec SHA256 remains `06104227304e7bab77e8f3f2de131ef26a949db437d02c2b2d7e20a25c057518`.

Read PLAN §3 A2/P1, C0 request/addressing/conflict/reply/undo/history contract, CLAUDE.md, full Sol1025 report/handoff and recovery1035 handoff. The single-source decisions were followed. No product repair, browser/spec/body edit, shared dependency/cache mutation, generated/pin changes, commitSession metadata/popup overlap, Git writes, service request, full suite, HTTP, build, daemon, hub, dispatcher or upstream operation.

## What the regression establishes

The new test starts with the original explicit hold=8 source, actually splits through `useClipEditing` at 2, holds and acknowledges the real local-save-session transport, waits for canonical r1/p1 adoption, then supplies the previously observed native Agent-move head shape (right ID unchanged, at=3, from=0, to=8, hold=6, speed=1, app.astrid fixed_start/for). It uses real `usePollSync`, `useTimelineSave`, `useTimelinePersistence`, localSaveSession, handoff, IndexedDB outbox and UI handler `handleSelectedClipChange({from:3})`. It adds no executor or manually constructed App request, and never fills in omitted reads.

The Agent result is an explicit unit fixture matching the real Agent output established by service28486/spec:510–517, **not a newly executed Agent move**. Transport accepted envelopes use the existing acceptedCommit fixture; these are not full Runtime contract qualification or real HTTP responses.

| Controlled schedule | Actual capture and owner | Durable/transport result |
| --- | --- | --- |
| Edit before deferred poll adoption | Display stays split r1/p1, original owner remains; trim reads at=2/from=0 | Valid intent persisted after accepted split intent ID; exact request goes out at r1/p1. Only after the transport is called does the test return a mocked ApiError(409). Rejected intent remains; visible document adopts Agent head with from=0. |
| Poll adopts Agent head, then edit during held original-basis read | Display is ra/pa, owner retirement/reassembly has begun, original basis is loading; UI edits from=0 to 3; verified read then resolves | `useTimelineSave.ts:177–179` rejects capture with **Local edits preceded the original verified read; draft retained**. Basis becomes unavailable with **Local edits preceded completion of the original verified read**. No trim intent or pending request, send count stays 1. Recovery draft retains from=3. This is a pre-dispatch capture refusal, not a Runtime 409/rollback. |
| Poll adopts Agent head and replacement owner is fully ready before edit | New owner and verified ra/pa source; trim reads at=3/from=0 | Durable intent basis is ra/pa; request sends at ra/pa, preserving hold=6/to=8/speed=1/opaque metadata. Mock accepted result adopts from=3. |

Both transmitting branches assert the persisted original intent, actual head/predecessor basis, exact single normalized from-only patch (raw before=0), mirrored raw after document, original gesture config/registry, declared at/from reads, step ID, ordinals/patch, source, merge=fields, dry_run=false, scope/base pair, pending key and exact JSON body, and unchanged intent at dispatch. Full clip equality protects explicit hold=6, Source Out, speed, at, new split ID and app metadata. No transport assertion is inferred from a local refusal.

**Causal RED/GREEN interpretation:** the held-read schedule deterministically reproduces the one-dispatch signature and names its concrete source refusal. The schedules on either side prove that the same genuine from-only transform can persist and dispatch. All three diagnostic expectations are GREEN on unchanged production source. No causal RED proving loss of an already valid durable stale capture was found, and no production repair/expected-failure waiver was added. The refusal enforces the existing verified-before-edit precondition; whether that UX policy should change is a separate reviewed A2 decision.

## Statechart and remaining limits

```
split UI -> durable split -> ACK -> canonical r1/p1 + clean old owner
  Agent head observed -> deferred poll timer
    edit first -> old owner appends authentic stale trim -> POST
      mocked Runtime rejection -> retained rejected intent -> canonical Agent adoption
    poll first -> canonical ra/pa -> retire clean old owner -> verify original source
      edit before verification completes -> seq changed -> capture rejects -> recovery draft only
      verification/claim complete first -> new owner -> append trim at ra/pa -> POST
```

Original-source invalidity is a separate branch: `readTimelineOriginalSaveBasis` checks exact head pair and raw/projected config/registry. The new valid fixtures prove initial readiness/raw-display agreement. Existing targeted guards still pass for stale gesture input, missing/refreshed/foreign head, source mismatch and non-finite values; none was weakened. No source mismatch or default laundering was needed to produce the held-read refusal.

The missing original trace cannot be reconstructed. This test does not establish which branch service28486 took, a real Runtime conflict reason/path, full ABI-v2 reply/history/undo semantics, lost ACK/restart qualification, or live provider behavior. The old 86-PASS evidence remains historical and unchanged; it was not rerun in full. Existing original browser 409/root-conflict assertions remain untouched and unverified. After-owner-ready dispatch also demonstrates why a poll that already adopted the Agent move cannot truthfully be required to yield a stale-read conflict.

Smallest next observable for a separately authorized retained-log browser diagnostic: record, at the actual capture boundary, selected ID/from/at/hold, displayed head pair, `originalLocalSaveBasis` status/reason, localSaveState owner/status/error, the capture promise's exact rejection, and read-only outbox intent/pending/accepted IDs plus actual POST count. These fields discriminate source-invalidity, verification-window refusal, successful stale dispatch, and replacement-owner dispatch. Do not change the original browser expectation or repair source based only on POST count.

Recommended next steps: independently review this test and its fixture/limits, then let the orchestrator choose a bounded A2 UX/capture repair or controlled stale-capture scheduling proof. Keep the original verified-source/read guards. No production patch is recommended before that review and no live retry was performed.

## Exact validation

Final command (working directory is this assigned worktree):

```bash
ASTRID_CHECKOUT=/home/user/work/wt/agt-pin-b8e50762 timeout 45s node node_modules/vitest/vitest.mjs run --config /tmp/w-f520e7cb56/vitest.config.ts --configLoader runner --no-cache src/tools/video-editor/hooks/useTimelineSave.test.tsx src/tools/video-editor/hooks/timelineLocalSaveHandoff.test.ts src/tools/video-editor/lib/serialize.test.ts -t 'traces split ACK|persists an inspector trim|stages the original verified closure|binds declared timing reads|retains source mismatches|refuses missing publication|refuses refreshed head|refuses foreign timeline|serializes a held media Source In' > /tmp/w-f520e7cb56/targeted-reviewed.log 2>&1
```

**Exit 0, 3 files PASS, 13 tests PASS, 76 filtered out, 7.81 seconds.** Three are new race schedules; ten are closest original mounted/handoff/serializer guards. No tests were disabled, skipped in source, deleted or rewritten.

```bash
node node_modules/typescript/bin/tsc -p tsconfig.json --noEmit > /tmp/w-f520e7cb56/type-root.log 2>&1
node node_modules/typescript/bin/tsc -p tsconfig.app.json --noEmit > /tmp/w-f520e7cb56/type-app.log 2>&1
node node_modules/typescript/bin/tsc -p tsconfig.node.json --noEmit > /tmp/w-f520e7cb56/type-node.log 2>&1
node node_modules/eslint/bin/eslint.js src/tools/video-editor/hooks/useTimelineSave.test.tsx --max-warnings 0 > /tmp/w-f520e7cb56/lint-reviewed.log 2>&1
git diff --check
```

All **exit 0**, empty type/lint logs. Root has no direct files; App config excludes test files, so these typechecks do not independently typecheck the new test. Scoped ESLint and Vitest exercise that test. Private runner config preserves normal setup/plugin/aliases, selects read-only private Composition exports as in previous bounded work, and points cacheDir into `/tmp/w-f520e7cb56`. Shared node_modules resolves to `/home/user/work/app/node_modules`; no writes were made there.

Development attempts, disclosed: initial scratch config write assumed the `tmpdir` marker was a directory; it is a text pointer to `/tmp/w-f520e7cb56`, corrected before config creation. First two three-race attempts failed at split ACK because the new mock reply contained UI-only undefined fields; changed only the new helper to serialize canonical JSON exactly like the original existing test, then 3/3 passed. A subsequent focused 13-test attempt failed 2 assertions newly expecting duplicate config+clips wire patches; inspection showed existing encoder intentionally normalizes this mirror to one clips patch. Corrected the new assertion to require the exact one-field patch and verify both raw stored mirrors separately. Final 13/13 passes. Earlier failed logs are `/tmp/w-f520e7cb56/race-first.log`, `race-second.log`, `targeted-final.log`; earlier green `race-third.log` was 3/3. No product failure was hidden by these test-fixture/assertion corrections.

Completion: bounded diagnostic task complete; historical exact-cause/live P1 proof remains evidence-limited. No external blocker prevented this authorized slice.
