# P2 current real-path review

Reviewed exact HEAD `c0fe88994405fd517b58473c14678a0d1b73056d`. No product, test, schema, helper, or instrumentation changes were made.

| Case | Current real path | Scope / ownership / reads | Outbox route and qualification |
|---|---|---|---|
| `transitionNone` single | `three-products.p2-tour.spec.ts` selects the Transition combobox after `.clip-action[data-clip-id]`; `ClipTransitionSection` → `PropertiesPanel.handleSelectedClipChange` → `useClipEditing` | Parent clip scope. `transitionClearBasis` verifies resolved-config identity and exact `{transition: undefined}` patch. Handoff preserves child closure, captures transition presence/value and pinned groups. | Parent `doc.patch` via `timelineLocalSaveHandoff` → `localSaveSession` C0 commit. Source-qualified; no current defect. Browser identity, POST, receipt, reload, and Undo remain UNKNOWN. |
| `transitionNone` bulk | Real app clip click plus shift-click transition clip; `BulkClipPanelBody` → `handleUpdateClipsDeep` → same handoff | Same parent ownership, with both selected parent clip IDs and exact field-only guard/read capture. | Same C0 `doc.patch` route and original reload/Undo assertions. Source-qualified; live UNKNOWN. |
| `registerAsset` | `dropFileOnTimeline` targets `.timeline-wrapper`; `useExternalDrop` → `handleFileDrop` → `prepareGenerationAsset` → `placePreparedAsset` → mounted prepared-media commit | Parent track scope. Guard rejects conflicting parent occurrences; validates exact media identity fields and registry state. | Semantic `clip.add-media` through persisted local save/outbox, with original row/media/registry guards. Source-qualified; live file-drop, upload, receipt, reload, and Undo UNKNOWN. The journey uses prepared-media, not direct `registerAsset`. |
| `automaticchildplacement` | Embedded canonical shot opens via `openEmbeddedCanonicalShot`; `dropFileIn` targets the child `.clip-action`; mounted `ShotTimelinePreview` → `ShotTimelineMediaControls` → scoped popup persistence binding → `sharedPopupMediaCommands` | Single-occurrence fixture is intentionally unshared. Current production branch emits `occurrence.add-media`, owns the occurrence, and reads occurrence/shot/internal pins plus authenticated media selection. | Semantic `occurrence.add-media` through the C0 outbox. The prior unshared static failure is obsolete: current production provider code now handles the one-added-row/no-change case. Real drag/drop, mounted binding, receipt, reload, and Undo remain UNKNOWN. |
| `popupSWAP` | Shared popup selector `.clip-action[data-clip-id="${popup.sharedOccurrenceId}:${TARGET_CLIP_ID}"]`; mounted Swap control/file input → same popup provider | Shared fixture intentionally has multiple occurrences. Provider verifies pins and closure, authenticates old/new selections, and scopes the replacement to the occurrence. | Semantic `occurrence.fork` plus `occurrence.swap-media`; C0 request preserves steps, merge, reads, source, rationale/group metadata, and outbox idempotency. Source-qualified; live browser/receipt/reload/Undo UNKNOWN. |

The original waits, exact field assertions, guards, reload checks, rollback/Undo checks, and legacy-route assertions remain in the existing journeys; none were weakened or removed.

Prior helper/provider passes are not live acceptance: they exercised isolated handoff or command logic, not the actual selectors, mounted callbacks, browser `DataTransfer`/file input, scoped persistence binding, upload/selection waits, C0 response, reload, or Undo. The automatic-child result is stronger than the prior report because the current fix is in the production mounted provider branch, not only in a test helper.

No source-confirmed current defect was found. If a live run fails, the smallest bounded owners are the mounted A2 parent save path for the transition/file-drop cases, and the mounted A3 popup provider/binding for the two child-popup cases. Catalog, params, popup-planner, and parent-mounted boundaries were treated as owned by the referenced reviews and were not edited.

Checks:

- `git diff --check` — passed.
- `git status --porcelain=v1 --untracked-files=all` — clean.
- Focused `rg`/`git show` checks — confirmed the exact current callers and source paths.
- No tests, browser, backend, HTTP, service, or full-suite runs, per task scope.