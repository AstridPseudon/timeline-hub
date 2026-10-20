# Native incoming transition SET (worker contract; M2 held)

Source worktree: `/home/user/work/wt/agt-m2-transition-set`.
Existing export: `astrid.sdk.timeline._clip_scalar_commands.capture_clip_set`.
Existing operation/version: `clip.set` / `1`. No alias operation.

Closed args remain `{values, clear}`, with optional `schema_source` (the existing
DocumentPin). Values admit `hold`, `transition`, and paired `elementRef` only.
`elementRef` requires transition SET and must select the same transition ID and
optional authored revision, with kind `transition`. No generic reference writer.
Capture additionally accepts existing `schema_inputs` and `realm_id` context.

Raw mapping, taken from App ClipTransitionSection and element-adapter:

- Selector/duration/params: `values.transition = {type, duration, params?}`;
  duration is positive finite seconds, not frames. Authored spelling is literal.
- ElementsLibraryPanel calls `timeline.apply_transition`; its legacy adapter
  writes `clip.elementRef = {id, kind, revision, packId?}` and
  `clip.transition = {type, duration, revision, params?}` on the TO clip.
  Native capture writes those two fields together via the same clip.set.
- None/Remove: `values: {}, clear: ["transition"]`. ABSENT is distinct from
  null, empty string, empty object, or a transition SET. Existing clear bodies,
  including their guards and treatment of elementRef, remain unchanged.

Canonical transition is INCOMING. A recorded same-owner, same-track predecessor
query uses stable authored start ordering (ties preserve collection order).
First clip has an empty predecessor selection. Gaps, overlaps and oversized
windows remain authorable; no native outgoing fit constraint or renderer call.
Only target/pair timing, identity, source and selection are guarded; other lanes
remain independent. Original capture claims must be replayed unchanged.

Selected project-pack parameters use the existing exact DocumentPin, immutable
snapshot resolver and retained source machinery. Changed known properties are
validated without coercion/defaults; unknown properties stay literal. Built-in
schemas come from the existing transition catalog. Unregistered transitions
without a selected pack remain opaque JSON; they make no renderability claim.
No inline schema, type-only pack fallback, new endpoint, or pin mutation.

Portable actual-App fixture captures and tests will be recorded below after
implementation. Runtime generation must use a NEW source tree later; frozen
schema 472622 / client 0.2.3 remain untouched. App writer deletion still needs
actual accepted consumer/reload/retry/undo and zero-legacy-traffic proof.
