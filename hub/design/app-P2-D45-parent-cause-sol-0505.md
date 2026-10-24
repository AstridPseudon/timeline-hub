**A2 result: precise UNKNOWN before commit transport. No product fix justified.**

Source identity matches the assigned App commit `c0fe88994405fd517b58473c14678a0d1b73056d`, tree `8e3ef15ee5f7c08381d8dc9efb38b5c98845466d`. Worktree remains clean.

Retained parent-case evidence from P2 `13583`:

- Original canonical parent has the selected clip at **0s**, reference at **15s**, and one occurrence.
- Pointer drag runs at trace time **164350–164821ms**, moving x=181→341.
- By **164959ms**, the selected clip’s rendered position has moved 160px, corresponding to **5s**. This demonstrates a local display mutation.
- The response wait starts at **164153ms** and times out at **254157ms**.
- Actual recorded browser traffic contains **zero `/commit` POSTs**. All 16 recorded `/inspect` requests returned **200**. ACP/chat 503s do not establish a timeline-commit failure.
- Final UI shows “Not saved” and the confirmation watchdog message.

The unresolved boundary is **local mutation → save scheduling/capture/owner/outbox → commit transport**. Durable intent append, pending-request reservation and transmission are not demonstrated. There is no Runtime/Agent mutation reply, error code/path, receipt or adoption to inspect.

The relevant source chain is:

| Boundary | Exact source |
|---|---|
| Capture move basis; conditionally forward it | `useClipDrag.helpers.ts:344,369–373,501–509` |
| Apply local edit with basis | `useTimelineTrackManagement.ts:332–337` |
| Emit/save subscription | `useTimelineCommit.ts:404`; `useTimelineSave.ts:405–407` |
| Capture waits for mounted owner | `useTimelineSave.ts:111–114`; original-read validation at `:223–275` |
| Capture before dispatch | `useTimelinePersistence.ts:1015–1018,682–693` |
| Validate parent/closure/before/basis | `timelineLocalSaveHandoff.ts:263–326` |
| Append durable intent | `localSaveSession.ts:269–311` |
| Reserve request, then transmit | `commitOutbox.ts:468–491`; `localSaveSession.ts:165–192` |

Reviewed merge `19c4839d81` adds the parent-move exception while preserving head, source, closure and selected-field validation. Those checks remain present at current HEAD. However, its persistence test **directly injects the move basis** into an already-created handoff (`useTimelinePersistence.test.ts:319–354`); it does not exercise mounted pointer capture or `useTimelineSave` owner initialization.

No safe diagnostic JSON or parent outbox snapshot was retained. Therefore an early valid refusal, missing gesture basis, pending owner/capture, empty emitted intent, or outbox wait cannot be distinguished. Neither D42 nor old run `12221` is established as the cause. The element and Gate5 final reports demonstrate different boundaries; no shared cause is proven.

Validation:

- Retained command: `npm run test:e2e:three-products -- tests/e2e/local/three-products.p2-tour.spec.ts tests/e2e/local/three-products.p2-elements-assets.spec.ts tests/e2e/local/three-products.p2-popup.spec.ts` — **exit 1; 405s; 3 failed, 5 NOTRUN**.
- Parent ZIP CRC check — passed; embedded tour/support source exactly matches this worktree.
- `git diff --check`, `git diff --exit-code`, `git diff --cached --exit-code` — passed; status empty.
- No tests, browser, backend or service launched.

**Smallest next bounded reproduction:** preserve the original parent test and waits; separately authorize retention of existing safe schedule/capture/owner diagnostics plus a read-only outbox snapshot at timeout. This should distinguish rejection, pending capture and dispatch state before selecting a repair.

Commit message and `DONE` created. No source or test changes.