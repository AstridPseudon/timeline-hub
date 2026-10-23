# A2 mounted Undo/Redo review handoff

**Verdict: PASS for the reviewed cumulative tree**, with the inherited
placement URL failure disclosed below.

Reviewed `835f052512cb81078e3be495e5a31f3ec3f98dd7` (tree
`ecf144fb9587ec45afae6d6a23b0573fbb9d2a5f`), based on WIP
`8ff4ab537e3ac9c81544f7df61fa8fe705f1f21f`, original mounted-owner base
`7eb59d8f93adacc5c9a862f31cb2e62ad082a69a`, against current App integration
`890b9561666c3619f69335dd747b15e042b3a9a3`.

The production flow is verified as:

`useTimelineState` → `useTimelineHistory(remoteHistory)` →
`useTimelineSave.localDocumentSave` → `timelineLocalSaveHandoff` → existing
`LocalSaveSession`/durable outbox → `RuntimeDataProvider.commitTimeline` →
existing generated client commit endpoint. Undo/Redo submits guarded
`timeline.inverse` with the authoritative publication target and current
acknowledged revision/publication pair. No snapshot fallback, fake history,
new executor, or alternate transport is present.

Authoritative matching-pair history reconstructs targets on reload through
`previous`/`undo_of`; unknown, partial, cyclic, paginated, or mismatched history
fails closed. Canonical accepted replies are adopted, and refused/invalid/lost
ACK cases retain visible state and exact durable request bytes/key. Upload,
interaction, editability, retry, conflict, and recovery guards remain active.

Evidence:

- Eight targeted files: **112/112 passed**.
- Root/App/Node TypeScript checks, scoped ESLint, and `git diff --check` passed.
- Runtime lock check passed against producer `34eac0041b0891e9011966b39bcbd26053fde5bc`.
- Exact Composition archive hash is
  `819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234`;
  private exact graph evidence is 80/80 archive members, with generated public
  exports confirmed. The shared install is older `0.0.8` and was not changed.

Known inherited issue: the author's broader neighboring run was 244/245 due
only to unchanged `dataProvider.test.ts:1224`, which expects an absolute
`http://runtime.test/v1/objects/...` URL but receives relative `/v1/objects/...`
for managed placement. No assertion, fixture, allowance, provider, or placement
source was changed.

Limits: no live HTTP/browser/service/full-suite proof and no Python guarded
inverse execution. Current Runtime integration is `a5d4258312c979024865ee704da2d632ca5b2730`,
the prior exact Agent execution pin is `4edc4b321cae5cfc58252d7ed89e3f0408238646`,
and the App client remains on frozen consumer lock `34eac004…`; no repin was
attempted. App home should port the reviewed behavior to a fresh current branch
with own commit and retain the inherited root-hook wiring.
