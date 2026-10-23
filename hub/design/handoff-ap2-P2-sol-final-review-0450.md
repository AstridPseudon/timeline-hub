# P2 Sol final review — 0450

## Verdict

**Source PASS; execution NOT READY/FAIL.** The 0440 correction is source-faithful and contains only the claimed `three-products.p2-tour.spec.ts` delta (67 additions, 8 removals). The required mounted Undo caller is genuinely missing, so no behavioral body was run and acceptance is pending App wiring of the existing inverse capability.

## Accepted source claims

The correction now separates the minimal submitted ABI-1 inverse/doc.patch requests from provider-normalized authoritative commands. It checks:

- exact submitted fields, count, and ordinal correspondence against the known Agent capture fields;
- complete `reply.data.commands === history.records.commands.map(record => record.command)`;
- ordered doc.patch binding operands against submitted changes and normalized physical step effects;
- exact step metadata plus authoritative patch/dependency retention;
- ABI-1 inverse default request/label/step metadata and its guarded publication target;
- empty native `record.dependencies` versus nonempty field/scope `step.dependencies`;
- canonical closure/digest and exact post-reload/repeated-history equality;
- prior-history retention after inverse;
- parent move, single transition None, and bulk transition None, including intended-field-only deltas, `config.clips` mirror behavior, raw absence, opaque/sibling/order preservation, guarded Undo, and no legacy mutation traffic.

The provider sources support the correspondence: Agent `commands.py:146-162, 200-274`, `_recording.py:240-274`, `_doc_patch.py:334-433`, and `_commit_patch.py:407-492`; Runtime projects the complete accepted command records at `runtime_protocol/timeline_commit_store.py:740-764`.

## Concrete production gap

Confirmed on latest readable App `8770aa162` and current integration `18354adfa` (resolver ancestor `616ee85b8`):

```text
useTimelineState.ts:641 -> useTimelineHistory({ ..., commitData: save.commitData, ... })
useTimelineHistory.ts:212 -> empty undoStackRef
useTimelineHistory.ts:424 -> local stack entry / restoreHistoryEntry
useTimelineHistory.ts:314 -> commitData(snapshot-derived nextData, { save: true, skipHistory: true })
```

`RuntimeDataProvider.undoTimeline` exists/exported at `dataProvider.ts:118-121, 767-796`, but there is no mounted caller beyond provider/unit-test references. A reload also recreates the empty local stack. D13/resolver does not change this wiring fact. The P2 test correctly keeps the required inverse-after-reload assertion and does not add a direct submission, skip, refusal, snapshot workaround, or expanded product scope.

## Checks and execution status

Passed:

- Playwright `--list`: exactly 3 tests in 1 file.
- `npm exec tsc -- --noEmit`.
- Scoped ESLint with `--max-warnings 0` on the changed spec.
- `git diff --check HEAD^ HEAD`.

No browser/socket/service/body/build/full/e2e run was performed. Final behavioral qualification is explicitly **pending the real mounted Undo caller**; once wired, run the original three cases through the central service from current integration.

