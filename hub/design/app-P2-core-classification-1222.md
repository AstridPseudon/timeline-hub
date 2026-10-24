# P2 classification report

Baseline audited: `d99396bca7c3853435cfa5a5991f5b1073187be4`, tree `3311baa327c8963d007cfc3a1b2f04617085f3b3`.

Decision: all eight original P2 gestures are CORE. No approved non-core category exists for these behaviors. Five are source-proven live but were NOT RUN; they are not dead.

Common production funnel:

`mounted caller → applyEdit/command session → persisted localSaveSession outbox → RuntimeDataProvider.commitTimeline → generated POST /v1/projects/{project}/timelines/{timeline}/commit with Idempotency-Key`.

The source preserves the C0 request/reply fields, canonical document, digest/id map, authoritative steps/dependencies, merge modes, accepted/merged/historical rebased replies, conflicts, invalid errors, dry-run, durable receipts, reload, guarded undo, and zero-legacy-route behavior.

| # | Original case / operation / classification | Core guarantee and non-core aspect | Current 11933 proof |
|---|---|---|---|
| 1 | `tests/e2e/local/three-products.p2-tour.spec.ts:690` — single parent clip drag to `at=5`; `doc.patch` guarded `parent/clips/id:<id>/at`. Caller: `useClipDrag.helpers.ts:501-513` → track management/`applyEdit` → move gesture handoff. | CORE: only the selected parent clip’s timing changes; reload/history and guarded Undo restore it; no legacy POST. Pixel geometry and receipt-ID formatting are test mechanics, not separate product scope. | **FAIL** in 11933: HTTP 200 accepted/merged-shaped reply, but test oracle required `receipt.receipt_id === Idempotency-Key`; durable history was not reached. This is an oracle/proof boundary, not grounds for declassification. |
| 2 | `three-products.p2-tour.spec.ts:722` — single Transition=None clear; guarded `doc.patch` remove of `transition`. Caller: transition selector → `PropertiesPanelBody` → `useClipEditing.handleUpdateClips` → transition-clear handoff. | CORE: explicit raw transition removal preserves opaque siblings/order and is undoable after reload. Selector label/UI wording is non-core presentation only. | **NOT RUN**; no behavior conclusion. |
| 3 | `three-products.p2-tour.spec.ts:742` — bulk Transition=None clear; one guarded patch batch removing both selected transitions. Caller: same path via `handleUpdateClipsDeep`. | CORE: both intended transition fields clear atomically, with unknown data/order preserved and guarded inverse. Batch layout is implementation detail, but atomicity is core. | **NOT RUN**; no behavior conclusion. |
| 4 | `three-products.p2-elements-assets.spec.ts:377` — Elements catalog Apply, followed by params edit; `doc.patch` list insert then params set. Caller: Properties panel `handleSelectedClipChange` → `useTimelineSave.ts:803-814` → element handoff (`timelineLocalSaveHandoff.ts:337-365`). | CORE: admitted/pinned element identity, exact params, parent closure isolation, reload, and two-step guarded Undo. Dialog status text `applied` is a test/UI oracle, not a reason to cut the gesture. | **FAIL** with 3 retained lifecycle events: Apply request started with Idempotency-Key, remained pending, and had no observed response/failure/abort/receipt. The pending transport boundary is not a product refusal. |
| 5 | `three-products.p2-elements-assets.spec.ts:468` — registerAsset file drop; semantic `clip.add-media` with authenticated media selection. Caller: file drop → `useExternalDrop`/asset preparation → `applyEdit` → `timelineLocalSaveHandoff.ts:385-460`. | CORE: imported media, one parent row, registry entry, exact fields, reload, and guarded Undo. File-picker/import UI details are non-core presentation. | **NOT RUN**; no behavior conclusion. |
| 6 | `three-products.p2-elements-assets.spec.ts:526` — automatic child placement from embedded shot file; `occurrence.add-media`. Caller: `ShotTimelineMediaControls.tsx:260-274` → `commands.addClip` → occurrence command session → outbox. | CORE: occurrence-owned child/asset creation, closure custody, unchanged parent/siblings, reload, and Undo. File-picker/thumbnail details are non-core. | **NOT RUN**; no behavior conclusion. |
| 7 | `three-products.p2-popup.spec.ts:815` — popup ADD on selected shared child; `occurrence.fork` + `occurrence.add-media`. Caller: popup `ShotTimelineMediaControls` → shared occurrence fork path → outbox. | CORE: fork only the edited shared occurrence, add authenticated media, preserve siblings/opaque data, reload, and guarded Undo. Popup layout is non-core. | **FAIL** before accepted-reply correlation: expected added row track `V2`, received `plate`. This is an unresolved product/oracle boundary, not evidence of non-core behavior. |
| 8 | `three-products.p2-popup.spec.ts:823` — popup SWAP; `occurrence.fork` + `occurrence.swap-media` with authenticated old/new selections. Same production caller as row 7. | CORE: fork ownership, authenticate old/new media, preserve all unrelated closure/history data, reload, and Undo. Popup presentation is non-core. | **NOT RUN**; no behavior conclusion. |

Why all eight remain CORE:

- PLAN §3 explicitly makes P2 the gesture tour and A3 explicitly includes popup add/swap, placement, element, and registerAsset saves.
- The editing foundation requires one writer through the persisted outbox, strict C0 request/reply data, reload, history, guarded undo, and zero old-route traffic.
- The prior bounded source assessment proved the five unreached gestures have production callers; they are not dormant.
- The frozen R4 App branch has no P2 files or equivalent v2 save funnel, so there is no upstream positive behavior to inherit or use to waive regression risk. Current risk is regression of the integrated App path, not scope classification.

Evidence status is exactly `11933: 0 passed / 3 failed / 5 not run`.

Exact retained run:

```text
wait-test app-P2-final-pure-integrated-1036-full-e2e-three-products-1024115551-11933
exit 1, 469s; 0 passed, 3 failed, 5 not run
```

Read-only checks performed:

```text
git status --short --branch       # clean
git diff --check                  # PASS
git rev-parse HEAD                # d99396b...
git rev-parse HEAD^{tree}         # 3311baa...
rg -n '^test\(' ...               # 3 + 2 + 3 = 8 original cases
```

No product/test/config changes, test edits, skips, xfails, probes, full-suite rerun, upstream fetch, or Git mutation. `commit-msg` and `DONE` were created. No D54–D56 header entry was present during audit; no new cut policy was invented.