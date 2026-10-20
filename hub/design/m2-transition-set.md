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

## Exact args, App capture mapping, guards (final, branch tl/agt-m2-transition-set-c)

```
clip.set v1  select = the TO clip (the transition belongs to the incoming clip)
args = { values: { transition?: {type, duration(s), revision?, params?, ...opaque},
                   elementRef?: {id, kind:"transition", revision, packId?} },
         clear: ["transition"|"hold"|"asset"], schema_source?: DocumentPin }
```

| App gesture | Capture |
| --- | --- |
| ClipTransitionSection type/duration/param edit | `values.transition` = the complete raw field (opaque keys carried forward by the consumer) |
| ElementsLibraryPanel -> `timeline.apply_transition` | one `clip.set` with `values.elementRef` + `values.transition` (id == type, same revision); project-pack ref adds `schema_source` |
| None / Remove | `values: {}, clear: ["transition"]` (absent, never null/empty/{}) |

Refusals: elementRef without transition; mismatched id/kind/revision; `id`,
`durationFrames`, `align`, `incomingPolicy` (compiled-only); non-positive,
non-finite or boolean duration; seconds rounding to zero frames (`Math.round`
of seconds*fps < 1, i.e. < 0.5 frame, at integer or rational fps); effect-layer
targets; `schema_source` with a builtin or without a selected pack transition;
values together with clear of the same field.

Guards (all in the recorded command): target and its same-lane immediate
predecessor (clip fields, relations, source asset digest), owner map fields, fps,
and the `transition.predecessor` selection (members, same-lane order, track
boundary). Other lanes stay independent. Inverse additionally refuses
intervening same-lane membership writes (A->B->A) and later transition edits.

### Incoming-neighbor windows (ratified policy)

Authoring never validates against neighbours: first clip (empty predecessor),
gaps, overlaps and oversized windows are all authorable; the single
canonical->compiled conversion owns clamping and half-open ends. Agent
guarantees only that the recorded predecessor query is stable and that the
authored seconds are a positive whole-frame window at the retained (possibly
rational) fps. Goldens: `recipe_m2_app_transition_windows.json` (10 cases:
first-before-successor, tie keeps collection order, gap, adjacent half-open,
overlap, oversized, and rational 30000/1001 first/adjacent/oversized/exact
half-frame), plus tests for the frame-quantization boundary.

## Executable contract gap: first-use document pin inverse

Decision (this worker): NOT implemented; strict xfail kept. Dropping an
introduced DocumentPin needs a recorded introduced-pins field on the native
record, a surviving-dependent scan over every later record's schema/snapshot
dependency and retained transcripts, and an inverse-history proof analogous to
`_inverse_media_removals` (~100 lines in commit.py/_recording.py) with
Runtime-side acceptance of the smaller manifest. That is not small. Authored
payload undo/redo is exact today; only the manifest keeps the extra pin.

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

## Goldens and mapping (recorded at composition, agt-m2-property-review-compose-b)

Composed worktree: `/home/user/work/wt/agt-m2-property-review-compose-b` (opacity + position + transition-set-b
+ effects-set-b on frozen 027bd16d). Same `clip.set`/`1` operation; ClipSetArgs values now admit
`hold`, `opacity`, flat position leaves, `transition` (+ paired `elementRef`), `entrance`/`exit`/`continuous`/`effects`;
`clear` enum is the union; optional `schema_source` (DocumentPin).

Portable goldens (byte-compared against replay of the stored commands):

- `tests/editing_conformance/fixtures/recipe_m2_app_transition_set.json` — `{bundle, commands, records, after_bundle}`
  from the App three-products bundle. Command: `clip.set` on the test's `PARENT` clip with `values.transition = {type: crossfade, duration: 0.75, params: {future: {literal: [null,false,0,"","ƒ(x)"]}}, future: [null, 2.0]}`;
  single write `{ref, path: ["transition"], before: absent, after: <transition>}`; selection `transition.predecessor`
  members `["parent/clip:f2-app-clip"]`.
- Sibling goldens from the composed branches: `recipe_m2_app_clip_position.json`, `recipe_m2_app_effect_fields.json`.

App mapping (ElementsLibraryPanel `timeline.apply_transition` → native): `clip.transition = {type, duration(s), revision, params?}`
plus `clip.elementRef = {id, kind: "transition", revision, packId?}` on the TO clip, written together by one `clip.set`.
None/Remove → `values: {}, clear: ["transition"]` (absent ≠ null/""/{}).

INCOMING policy tests (`test_recipe_transition_set.py`): `test_ratified_first_gap_overlap_and_oversized_windows` (30 fps and 30000/1001)
and `test_incoming_policy_validates_owner_only_without_neighbor_fit` — first clip (empty predecessor), gap, overlap and a 20 s
oversized window are accepted; only the target clip is written; neighbors are untouched; no predecessor/successor fit is required;
sub-frame durations are refused. The Agent timeline validator in this tree is still the outgoing (successor-fit) form; the
canonical-mode validator lives on held `tl/agt-m2-transition-validator` and is not composed here.
