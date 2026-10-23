# A4 mounted track persistence review — FAIL

Reviewed `tl/app-A4-track-mounted-1921` (`6b42420978`) against base `6e04a9a9a7`.
Only the new persistence test differs. Focused tests: **3 files / 37 passed**.
TypeScript app/node/root, scoped ESLint, and `git diff --check` all passed.

## Result

**FAIL.** The new test uses the real mounted caller through
`handleMoveTrack` → `applyEdit` → `useTimelineSave` →
`createTimelineLocalSaveHandoff` → `createLocalSaveSession` → outbox. It proves
the accepted generic `doc.patch` `list.move`, paired base, durable intent,
atomic/no-reads choice, representative raw/null/opaque preservation, canonical
head adoption, and refusal rollback. It does not prove the complete required
Runtime-v2 refusal/revalidation or the generated-client transport binding.

## Old → kept → mounted caller map

| Obligation | Kept old evidence | Mounted witness / gap |
|---|---|---|
| Valid reorder, exact row/order preservation | `trackReorderCapture.test.ts` valid reorder case | Real hook emits the mounted save; representative rows/opaque values checked, not full all-row equivalence |
| Same-order explicit legacy write | `trackReorderCapture.test.ts` round-trip case | Current mounted UI is honestly a no-op; legacy explicit-record parity remains uncovered |
| Missing, duplicate, foreign, malformed identity refusal | `trackReorderCapture.test.ts` refusal cases | Kept unchanged; no mounted semantic replacement claimed |
| Invalid current collection and stale identity/order refusal | `trackReorderCapture.test.ts` atomic/stale cases | Kept unchanged; no mounted semantic replacement claimed |
| Mounted save path and durable local intent | None needed | Covered through actual hook/handoff/session/outbox; no detached manual patch producer |
| Full v2 accepted `{data, receipt}` binding | Existing Runtime fixture/tests | New test supplies `steps`, `merge_mode`, and matching `receipt.result` in its mock, but does not assert receipt-result equality or complete authoritative accepted data |
| Full v2 conflict 409 | Existing client/session classifier behavior | Mock has status/base/current/conflicts/code/path/hint/suggested command but omits required `head`; only code/path/hint are asserted |
| Reject → rollback → revalidate → message | Existing session path | Mock `loadTimelineCommandBasis` returns unchanged `r0/p0`; rollback is observed, changed-head revalidation is not |
| Generated client POST/body/idempotency header | Existing `localSaveSession.v2.test.ts` | New mounted test ends at mocked `DataProvider.commitTimeline`; generated `WorkspaceClient` transport is not wired into this witness |

## Hold / next step

Keep HOLD. If authorized, complete the refusal envelope and make the mock
return a distinct changed canonical head so revalidation and preserved details
are asserted. Then connect the mounted harness to the existing generated-client
transport seam and assert exact serialized body/path/header. Preserve all old
capture tests and the same-order no-op distinction.
