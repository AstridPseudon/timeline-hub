# WC10 populated timeline duplicate: bounded native-source plan

Status: **bounded contract gap; keep the Main positive live** (2026-10-21).
This is source planning only. It does not register an operation, change a
schema, add a Runtime port, or convert the existing duplicate into a refusal.

## The exact Main positive

The live CLI path is `timelines duplicate`:

- `astrid/packs/timeline/cli_working.py:456-466` calls
  `duplicate_timeline(project, ref, slug, name, revision)` and reports the new
  head.
- `astrid/sdk/timeline_duplicate.py:187-200` opens the requested source head,
  checks it before creating anything, then calls `timelines.create_empty` with
  a deep copy of the populated source parent config.
- `astrid/sdk/timeline_duplicate.py:209-226` opens the real destination,
  copies the source content, validates the stored shot count, and publishes
  the destination. On failure `:227-232` archives that real destination.
- The positive is explicitly covered without a renderer by
  `tests/sdk/test_scene_save_core.py:143-160`; it expects the populated
  duplicate to publish and produce two writes. The pure content and chapter
  positives are in `tests/packs/timeline/test_verbs_working_copy.py:144-169`
  and `tests/sdk/test_timeline_restructure.py:358-387`.

This is not a pristine initializer. The duplicate must continue to succeed for
a populated source, including a source with a non-default raw config. No
native migration may turn that positive into `not_pristine`, `migration_needed`,
or an unsupported-operation refusal.

## What the current copy actually preserves

`copy_content` is useful evidence, but it is not a native command batch:

- `astrid/sdk/timeline_duplicate.py:79-96` preserves placement order and
  copies the source config, registry, and parent clips into a new target map.
- `:99-126` maps source shot/occurrence identities, copies the source payload
  and internal timeline, and retains repeated source shots as one destination
  shot with repeated destination occurrences.
- `:115-120` deliberately removes source-bound payload fields and clears
  `text_bindings`; `:128-136` records that loss or rebinds narration from text.
  Therefore this helper cannot be advertised as exact source-revision or full
  opaque-payload preservation.
- `assert_copy_equals_source` at `:142-169` checks placement count/order,
  identity mapping, placement timing, and internal clip lists. It does not
  prove equality of the complete raw parent, payload, source mapping, immutable
  revision closure, or dependency manifest.

The existing pure helper is therefore a good *copy-materialization primitive*
for a future source-aware path, but not the missing authority boundary.

## Existing native pieces and their limits

The smallest same-timeline native birth/copy chain is already visible in the
current command family:

1. The settled WC10 `timeline.init@2` source accepts only an authenticated
   pristine bootstrap and writes the raw `parent.config`, `name`, and `slug`
   as scoped fields. Its empty-structure guard is intentionally not a
   populated-document carrier.
2. Existing `track.create` can add destination parent tracks. The first
   canonical shot/occurrence is `capture_occurrence_create` in
   `astrid/sdk/timeline/native_occurrence_create.py:15-50`; it creates an empty
   typed `shot:<id>` and `occurrence:<id>` and derives timing from the
   destination output. Its capture wrapper is `:53-61`.
3. Existing `occurrence.duplicate` is the closest source-copy operation:
   `astrid/sdk/timeline/native_occurrence_duplicate.py:11-55` reads one
   `occurrence:<id>` from the current bundle, selects that occurrence's clips
   and tracks, reads its internal source and payload, and creates typed shot and
   occurrence roots. It refuses legacy `pinnedShotGroups` at `:15-16` and
   reserves destination identities at `:25-55`. The source shot copy and item
   remapping are delegated to the existing `_copy_shot_for_placement` helper
   (`astrid/core/timeline/authoring_bundle.py:280-313`).
4. The destination root factories are already centralized: shared source shots
   become an authoring identity through `_authoring_shot_id`
   (`authoring_bundle.py:218-228`); present destination root identity fields
   are re-derived by `_rederive_root_identity` (`:231-253`); and
   `compile_authoring_candidate` materializes the immutable shot/internal
   closure and parent occurrence (`authoring_bundle.py:778-1050`).
5. Typed-root creation, reservation, and guarded inverse/redo are existing
   machinery. The compact native proof is
   `tests/editing_conformance/test_recipe_occurrence_duplicate.py:65-83` and
   `:107-150`; typed-root reservation checks are in
   `tests/sdk/test_timeline_commit_graph_roots.py:30-55` and `:97-139`.

These pieces compose only when the source occurrence is already in the bundle
being edited. `occurrence.duplicate` has no source-timeline selector and no
cross-timeline read authority. `occurrence.create` cannot substitute for it:
it creates an empty shot and cannot carry source opaque fields, media, source
revision pins, or occurrence order.

The detached document-diff adapter cannot bridge this gap either. It explicitly
requires placement membership/order to remain unchanged at
`astrid/sdk/timeline/document_diff.py:315-327` and refuses shot creation or
deletion at `:329-343`. It is a bounded view editor, not a duplicate importer.

## Scope proof: restore is not a cross-timeline source carrier

`timeline.restore` must not be used as an implicit source import:

- `astrid/sdk/timeline/commands.py:188-189` makes restore the sole command.
- `astrid/sdk/timeline/commit.py:402-409` loads a revision and requires its
  `project_id`, `timeline_id`, and parent revision ID to match the current
  request context.
- The restore path repeats that exact scoped load at
  `astrid/sdk/timeline/commit.py:914-923` and `:990-997`; a stale destination
  head is refused rather than rebased.
- Historical closure use is likewise same-timeline: `document_from_bundle`
  rejects a foreign source bundle at `astrid/sdk/timeline/commit.py:299-305`.

Thus a source revision ID from Main cannot be placed in a destination
`timeline.restore` command. The existing inverse/restore guarantees are strong
and should remain so; weakening the scope check would turn a safe restore into
an unauthorized whole-document writer.

## One compact pure witness

The existing occurrence helper proves the positive that is available today,
without Runtime or persistence. This is the smallest reusable witness (the
same assertions are already present in the conformance test cited above):

```python
source = bundle_from_document(document_fixture())
before = copy.deepcopy(source)
command = capture_occurrence_duplicate(
    source, "occurrence:occ-0", "occ-copy", "shot-copy"
)
plan = execute(source, [command])
reloaded = bundle_from_document(document_from_bundle(plan.bundle))

assert source == before                         # source is read-only
assert plan.records[0]["created"] == [
    {"ref": "shot:shot-copy", "kind": "shot", "owner": None},
    {"ref": "occurrence:occ-copy", "kind": "occurrence", "owner": "parent"},
]
assert document_from_bundle(reloaded) == document_from_bundle(plan.bundle)
```

The identity/opaque/order/media witness extends this same pure setup with the
existing `identity_document` fixture: the current test asserts the derived
destination root identities, exact copied internal payload, unchanged source
rows, unchanged media manifest, reload, guarded inverse, redo, and replay at
`tests/editing_conformance/test_recipe_occurrence_duplicate.py:111-150`.
That is evidence for same-timeline occurrence duplication, not evidence for
Main's cross-timeline duplicate workflow.

## Smallest honest proposal / gap disposition

There is no existing command batch and caller context that meets all requested
properties at once. The minimum future native source contract would have to
retain these boundaries, without inventing a second whole-document writer:

1. Read the source through an authenticated, exact source-timeline revision
   closure: parent revision, ordered occurrences, each linked shot revision and
   internal revision, raw opaque fields, and the dependency/media manifest.
2. Materialize destination roots with the existing typed-root factories and
   `_copy_shot_for_placement`, remapping only identities that are required to be
   destination-local. Preserve all other raw fields and occurrence order;
   re-derive only the destination root factory fields already identified by
   `_rederive_root_identity`.
3. Record source-scope reads/selections and destination creates in one guarded
   command batch. The batch must be retryable from its original source pin,
   reloadable from the accepted destination closure, and invertible using the
   existing typed-root inverse. Destination edits must block inverse when a
   copied root, source selection, order, or dependent occurrence changed.
4. Keep source and destination timeline IDs explicit throughout. A
   destination-local `timeline.restore` remains invalid for the source; no
   cross-timeline restore exemption is part of this proposal.

The current Main duplicate remains the live positive until that source-aware
carrier exists and is paired with Runtime authority. The bounded M2 action is
therefore to record this gap and preserve the positive—not to add a dummy
timeline, route an empty `timeline.init@2` around its pristine guard, or turn
the duplicate into a refusal.

## Evidence boundary

This document is based on source inspection and the existing pure/native tests.
No Runtime/App/HTTP/browser/render/full qualification is claimed here.
