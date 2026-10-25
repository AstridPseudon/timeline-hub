# P2/A3 independent source review — PASS

## Verdict

PASS for the bounded conclusion in `app-A3-bulk-noPOST-0150`: the retained evidence proves the intended commit POST was absent, but does not prove the first App boundary or a source cause. I found no basis for a product patch or Runtime attribution.

Reviewed lineage remains distinct:

- Original failed run: `fd2f843a`
- Reviewed App source: `4b98436552bf30f5fb28bbb958b1817430b12e34`
- Normal App HEAD: `24865fa212148e9bc149a1285936372656037e55`
- The only `4b984..HEAD` changes are manifest/lock files, not this path.

## Source trace

The actual mounted path is wired as follows:

- `PropertiesPanel.tsx:521-555` — multi-selection renders `BulkClipPanel` and passes `handleUpdateClipsDeep(selectedClipIdsList, ...)`.
- `PropertiesPanelBody.tsx:224-246,356-391` — resolves selected clip IDs and passes the same callbacks.
- `BulkClipPanelBody.tsx:538-558` — Transition → None calls `onChangeDeep(() => ({ transition: undefined }))`.
- `useClipEditing.ts:216-247` — validates IDs, creates the transition-clear basis, and calls `applyRowsEdit`.
- `useTimelineCommit.ts:401-405` — emits `scheduleSave`.
- `useTimelinePersistence.ts:1013-1017,1094-1160` — captures before debounce and schedules the save.
- `timelineLocalSaveHandoff.ts:488-587,608-620` — reads both transition fields, appends the document intent, then flushes.
- `useTimelineSave.ts:319-323` — sends through `provider.commitTimeline`.

Relevant source blobs: `PropertiesPanel.tsx@1c6a6784`, `PropertiesPanelBody.tsx@a2e4a71f`, `BulkClipPanelBody.tsx@e04f155e`, `useClipEditing.ts@2b74f874`, `useTimelineCommit.ts@873fe8ead`, `useTimelinePersistence.ts@b289d039`, `timelineLocalSaveHandoff.ts@4bce50f2`, `useTimelineSave.ts@6b069ffd`.

## Control coverage finding

The 119 passing controls do not exercise the same mounted bulk callback and exact two intended identities:

- `PropertiesPanel.mounted.test.tsx` selects only `authored` at line 120 and edits the Content field at line 146; it never mounts the bulk transition path.
- `useClipEditing.test.ts` exercises `handleUpdateClipsDeep(['selected', 'sibling'])` at hook level, without mounted DOM selection or outbox transport.
- `timelineLocalSaveHandoff.test.ts` calls handoff capture directly.
- `BulkClipPanelBody.test.tsx` uses mocked controls and a single fake clip.

The retained mounted fixture does contain the exact missing control: `f2-app-clip` and `f2-transition-clip` (`harness.ts:1228`), selected with click + Shift-click and cleared through the real Effects/Transition/None DOM flow (`three-products.p2-tour.spec.ts:669-677`). Its expected request is explicitly two `remove` patches, exact reads, `merge: 'fields'`, and intent `Clear transitions: f2-app-clip, f2-transition-clip` (`:797-816`, helper `:476-529`).

## Finite missing observation and next task

Add one PR-sized mounted test in `PropertiesPanel.mounted.test.tsx` (or a focused sibling test) using:

- IDs `f2-app-clip` and `f2-transition-clip`
- Both clips carrying transitions, same track, retained ordering/opaque fields
- Head pair `r0/p0`, canonical `r1/p1`, held ACK, existing `createCommitOutbox()` inspection
- Real mounted selection of both clips, Effects tab, Transition → None
- Assertions for two exact transition reads/removes, `label: 'Edit timeline'`, exact clear intent, `merge: 'fields'`, `source: { via: 'app' }`, outbox persistence, and `commitTimeline` invocation

Keep the existing wrong-editor, stale, forged, missing, closed, and sibling guard tests unchanged. This control would identify whether the first observable boundary is mounted selection/callback, local capture/outbox, or provider dispatch without adding a collector or weakening refusals.

## Tests run

- Targeted Vitest command over the five retained control files: **5 files, 119 passed**
- Root/app/node TypeScript `tsc --noEmit --incremental false`: **passed**
- Scoped ESLint with `--max-warnings 0`: **passed**
- `git diff --check`: **passed**
- No full suite, browser journey, Runtime service, build, install, or product edits run.

No source changes were made.