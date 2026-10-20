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

Implementation notes:

- Portable golden: `/home/user/work/wt/agt-m2-transition-set/tests/editing_conformance/fixtures/recipe_m2_app_transition_set.json`.
  Uses `app_bundle()` from the original App three-products harness rows, with
  unchanged numeric/opaque JSON, command claims, accepted records and after image.
- Query `transition.predecessor` records the target as query owner, its immediate
  predecessor as members (empty for first), the same-lane sorted identity vector
  as order, and the owning track identity as boundary. Membership/order changes
  on this lane refuse; other-lane edits remain independent. Inverse also checks
  intervening membership writes, including same-lane A→B→A.
- Product scope includes a small `commit.py` extension: existing schema hydration
  and selected-reference resolver now handle clip.set alongside clip.set-params.
  It reuses params.schema/params.snapshot dependency keys so existing inverse
  snapshot resolution and retention apply unchanged. No Runtime source changed.
- SET carries the complete raw transition field; params are literal JSON, with
  explicit replacement/reset semantics. Consumers must carry forward opaque
  nested data for duration/param changes, as the duration panel already does.
- Built-in unselected type-only writes use the existing shipped transition
  catalog schema if registered; unregistered types remain opaque. Selected shipped built-ins require an exact id/kind/packId/revision match
  through the existing catalog descriptor resolver (no type-only fallback).
  Other selected pack references require an admitted immutable snapshot.


Canonical SET accepts App `type` and seconds `duration`; compiled-only
`id`, `durationFrames`, `align`, `incomingPolicy` fields are refused in this
bounded input. Extra opaque keys remain literal. Seconds must quantize to a
positive safe whole-frame window at the retained rational frame rate.

## Executable contract gap: first-use document pin inverse

`tests/sdk/test_timeline_transition_schema.py::test_first_selected_transition_exact_document_inverse`
is a strict expected failure. First applying a selected pack can introduce its
DocumentPin. Existing document_from_bundle keeps that pin after inverse even
when the authored transition/elementRef are exactly restored. Authored payload
undo/redo and retained snapshot reads pass; the entire manifest/revision image
does not return byte-exactly to the original. This is existing retention behavior,
not justification to rewrite the expected exact-document assertion.

Smallest proposed contract: record introduced DocumentPins on the existing
native record, analogously to introduced media, and let the existing guarded
inverse drop a newly introduced manifest pin only when no surviving/later
binding depends on it. Keep immutable historical custody available for redo.
This worker does not invent a second retention mechanism or silently claim
exact first-use selected-pack undo. M2 and that consumer deletion remain held.
