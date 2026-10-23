**Verdict: INSUFFICIENTEVIDENCE.** Case 2 demonstrably rejected the trim locally, before transport, with authentic reason `source-parent-mismatch`. The retained evidence does not identify which compared operand differed, so it cannot establish PRODUCTDEFECT versus VALIDREFUSAL/HARNESS.

Read-only triage completed in approximately three minutes. No repository, test, pin, environment, or artifact changes; no replay or test-service requests.

**Safe-artifact publication manifest**

Both existing files passed complete JSON parsing, nested schema checks, strict mounted-record projection, formatter idempotence, and credential/private-data pattern checks. No unexpected keys were found.

| Existing file | Bytes | Security |
|---|---:|---|
| [p1-diagnostic.json](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/app-P1-preflight-inner-return-2147-ap2-P1-chain-h6-1023215343-24510/playwright-output/three-products.p1-chain-P1-c924b-p-rolls-back-with-a-message/p1-diagnostic.json) | 144118 | PASS |
| [Existing attachment copy](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/app-P1-preflight-inner-return-2147-ap2-P1-chain-h6-1023215343-24510/playwright-output/three-products.p1-chain-P1-c924b-p-rolls-back-with-a-message/attachments/p1-diagnostic-cc992896ab7189cf38730c3b63c929a2ce70001c.json) | 144118 | PASS; identical bytes |

SHA256 for both:

`faa0df373a0ae84dfd3ba56aab81988a65435c31b339ec91864be1bb299e4b0f`

The manager can publish these **existing bytes** under D30. Nothing was copied or reconstructed. Private trace/error-context artifacts were not opened. The request projection contains body length, **not a request-body hash**; that missing hash was not reconstructed.

**Run and failure**

Inspected only the named run, `app-P1-preflight-inner-return-2147-ap2-P1-chain-h6-1023215343-24510`.

- App HEAD verified: `e6d72d3d07d2df485e4f3e86c56d1eb2dd5cd91a`.
- Tree verified: `6513960eb0b2704d02c3b3298ba594b546af7565`.
- Summary identifies Agent `78738040d72ce74c42ddf7731221aecb06f9246d` and Runtime `2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d`.
- Existing result: **1 passed, 1 failed**. Case 1 passed in **29.7s**. Case 2 timed out at **300001ms**.
- Primary failure retained: second-POST expectation at [three-products.p1-chain.spec.ts:1593](/home/user/work/wt/app-P1-H24-triage-sol-2201/tests/e2e/local/three-products.p1-chain.spec.ts:1593), expected `2`, observed `1`; log also records the 90000ms predicate timeout.
- Final safe artifact captured at `2026-10-23T22:01:02.806Z`.

Preflight passed. Its success and case 1’s pass do not establish case 2’s cause.

**Actual case 2 gesture and basis**

Project: `e1c63027229f49adb37ef2e80552d3f9`  
Timeline: `7329bb69-4aee-4eb8-bf2d-605485b890a1`  
Selected right clip: `p1-chain-source-1792792571203`

The retained DOM observations show Source In changing **0 → 3** on that selected clip. Mounted diagnostics independently show `gestureKind: trim`, patch **`{from: 3}`**, with `to/at/hold/speed` absent from the patch.

At schedule/capture:

| Numeric projection | from | to | at | hold | speed |
|---|---:|---:|---:|---:|---:|
| Gesture’s original selected clip | 0 | 8 | 2 | 6 | 1 |
| Scheduled/captured next source clip | 3 | 8 | 2 | 6 | 1 |

The callback maps to [useClipEditing.ts:235](/home/user/work/wt/app-P1-H24-triage-sol-2201/src/tools/video-editor/hooks/useClipEditing.ts:235), which snapshots the trim gesture basis before applying rows. [useTimelinePersistence.ts:1012](/home/user/work/wt/app-P1-H24-triage-sol-2201/src/tools/video-editor/hooks/useTimelinePersistence.ts:1012) invokes local capture.

Initial basis-ready and handoff-ready observations had matching mounted/original heads:

- Revision `authoring-parent-revision-8a339cc6c19d8445c44a37325e6ac218cc328e8c88d96e13bc7e956fe08d0aa1`
- Publication `txn-c40c77d04df74d2a83426b35b686507a`

After the accepted split, adoption and trim schedule show:

- Revision `authoring-parent-revision-4714a2e5684a324112f750df7edf035f14a01ce3eb28db54d3e7cded11481609`
- Publication `txn-2304c204c32b4eb484ebb20a4718903e`

Sequence 19’s `originalHead` reports the hook’s original verified read. It does **not** prove the handoff retained an obsolete basis.

**Capture, owner, and outcome**

Times below are page-relative milliseconds.

| Sequence | Time | Observation |
|---:|---:|---|
| 6 | 3610.5 | Original basis ready |
| 7 | 3610.9 | Identity present; owner current |
| 9–10 | 3658–3661.6 | Session created; handoff ready |
| 14 | 5564.7 | Split capture resolved |
| 16–19 | 10678.8–10679.5 | Split adoption completed; session saved |
| 21 | 11620.0 | Trim scheduled |
| 22 | 11620.3 | Trim capture called |
| 23 | 11649.8 | Trim capture rejected |

The trim rejection is:

- Phase: `capture-rejected`
- Stage: `capture`
- Exact finite-38 enum: **`source-parent-mismatch`**
- Error class: **`TimelineVersionConflictError`**

Owner alias remained **1**, hook generation **0**, session present, closed false. Identity presence was observed; authenticated principal contents are intentionally unavailable. The durable outbox separately reports owner `eec76373-3e47-432c-8f7b-8dc8dc77e2b2`, generation **1**; these generation fields belong to different objects.

No trim `capture-resolved` event appears. The final outbox read succeeded: one owner, zero intents, no pending request, no outcome, no conflict. Only the split POST appears, with HTTP **200**. A separate local draft write is possible in the source path; its completion is unobserved.

**Second POST, intervening Agent move, Runtime 409, and refusal rollback were not reached.** The Agent move follows the unmet second-POST assertion in this test.

**Smallest proven local check—and missing seam**

The authentic rejection maps to [timelineLocalSaveHandoff.ts:78](/home/user/work/wt/app-P1-H24-triage-sol-2201/src/tools/video-editor/hooks/timelineLocalSaveHandoff.ts:78), called during capture at line 218:

```text
(source.config differs from loaded AND projected.config)
OR source.registry differs from projected.registry
```

Comparisons use `authoredJson` and canonical equality. The rejection occurs before `appendDocument` at line 308. The hook emits the tagged rejection at [useTimelineSave.ts:104](/home/user/work/wt/app-P1-H24-triage-sol-2201/src/tools/video-editor/hooks/useTimelineSave.ts:104).

**Missing seam:** the actual compared config/registry operands—or a safe, field-specific comparison result with their basis provenance. The artifact cannot distinguish the failing config arm from the registry arm or identify the differing field. Selected numeric clip values are insufficient.

Consequently, no guard clearing, basis replacement, Runtime/oracle fix, or product patch is justified. No fix/regression proposal is made without a proven product cause.

**Limits and next step**

The case 2 buffer contains **23/32 records**, accepted 23, rejected projections 0, overflow 0, listener errors 0. “Rejected projections 0” does not negate the captured save rejection. The duplicated snapshots agree. Console arrays are capped at 40; other loss/unknown markers remain explicit. No missing suffix or full history was reconstructed.

Historical run 17985 was not used as current proof. Safe projections remain distinct from private App custody.

Tests: **N/A—read-only causal triage.** No test commands were run. Read-only validation passed; `git status --short` was empty. Authorized `commit-msg` and `DONE` control files were written.

Next: manager dispatches **app-P1-H24-triage-review-2201 (Luna)**. Further classification requires the missing comparison seam; no implementation change is authorized by this verdict.