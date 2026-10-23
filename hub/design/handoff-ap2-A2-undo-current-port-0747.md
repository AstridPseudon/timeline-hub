# A2 current Undo/Redo port handoff

**Verdict: PASS for the current App port.**

## Identity

- Base commit: '890b9561666c3619f69335dd747b15e042b3a9a3'
- Base tree: '20c8c1ed5e9ca48bc1f56f66f0404c83f8d97473'
- Reviewed source: '835f052512cb81078e3be495e5a31f3ec3f98dd7'
- Reviewed source tree: 'ecf144fb9587ec45afae6d6a23b0573fbb9d2a5f'
- WIP provenance: '8ff4ab537e3ac9c81544f7df61fa8fe705f1f21f'
- Current port final commit: harness-assigned after worker exit (not available
  before commit); the seven worktree blobs are listed in WORKERreport.

## Scope and overlap

The port is exactly the cumulative 'cffa91c93..835f05251' Undo delta:
localSaveSession.ts, timelineLocalSaveHandoff.ts,
useTimelineHistory.test.ts, useTimelineHistory.ts,
useTimelineSave.test.tsx, useTimelineSave.ts, and
useTimelineState.ts. No stale WIP ancestry was merged.

timelineLocalSaveHandoff.ts was checked against current '890'. Current '890'
contains no Move handoff delta. Move 'f2d6d62c7' is a queued child of '890', so
it was deliberately not imported; no Move read intent was overwritten. Current
paired-head and startup-spec changes remain present.

## Caller and behavior

The production caller remains:

'useTimelineState → useTimelineHistory(remoteHistory) →
useTimelineSave.localDocumentSave → timelineLocalSaveHandoff →
LocalSaveSession/outbox → RuntimeDataProvider.commitTimeline → generated client'.

Undo/Redo reconstruct targets from complete matching-pair authoritative history,
submit guarded 'timeline.inverse' through the existing outbox/client, adopt
canonical accepted/merged replies, and fail closed for unknown, partial,
cyclic, paginated, or mismatched history. Refusals, invalid responses, and
lost ACKs retain visible state and exact retry body/key. Upload, interaction,
editability, retry, conflict, and recovery guards remain active. There is no
snapshot fallback, alternate transport, product refactor, or schema/client
change.

## Evidence

- Exact eight-file targeted Vitest: **112/112 passed**.
- Root/App/Node TypeScript checks: **PASS**.
- Scoped ESLint and git diff --check: **PASS**.
- Runtime normal lock: **PASS**, producer
  '34eac0041b0891e9011966b39bcbd26053fde5bc'.
- Private exact Composition archive: **PASS**, SHA-256
  '819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234',
  80 files, version '0.0.14', generated public subpaths resolved from the
  private extracted graph.

The frozen 835f source review disclosed an inherited dataProvider.test.ts:1224
managed-placement URL mismatch. The same named test passes on current 890
(1 passed, 74 skipped) through the existing paired-head integration. No
assertion, fixture, provider, or placement source was changed by this port.

## Limits

No browser, live HTTP/socket/service, build, full suite, central test request,
or Python guarded-inverse execution was run. The targeted tests use scripted
Runtime envelopes and do not qualify live Runtime receipts.
