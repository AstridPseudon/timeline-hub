# Agent source handoff: producer clip leaves and literal position

Status: source-only review request for Runtime and App2. These are unfrozen
Agent source units. This packet requests contract ACK or a concrete mismatch;
it does not request generation, pinning, activation, or a Runtime/App release.

## Exact source identities

| source | commit / tree | schema file SHA-256 | inventory |
| --- | --- | --- | --- |
| producer clip leaves | `57af3fffe192ad369c4282d9ab3a67efd57dc51c` / `319013e799d244497deac26719282595c213b658` (parent `f448c4b40c60d08f4092e232688b0de99bb07243`) | `0b747d87c763a8f0ba0dcc5027390ab04d6296cfddfffa8c049020334ca3ec92` | 59 definitions / 33 closed clauses |
| literal position | `f2a2cfbb58926b7c9d47d206ae294acf376b0c2e` / `8c5674a5e329ab8dc5dcb4711251268a61b81847` | `b06d49c1be645ec6631bad109963697a3e5eb956786953751fd57b650be19836` | 55 definitions / 29 closed clauses |

The producer source strips structurally to its exact `f448c4b40` parent
(`d4508b9fa5db9b2a2774fc5acc811fc34814c53d`); the existing source-union
guard also reconstructs the exact `84fc0863a1f925f32c00b171eaf51b8f06afb7d34064296394bc8592386cbbc5`
floor. The position source strips structurally to the ordinary Main014 source
`6efc81500a0e0688c2bb41e736503f0fc3e04abb` / tree
`2ed2b8a12b5b3391ca221ba6ff05390f71a73556`, whose exact schema SHA-256 is
`6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`.

The current bounded union is a separate source identity:
`5672d2b7deee2bfe2ab375fd6db5fc35a192591d` / tree
`6dd13b552c4f07fff5586b1fa772bdbdf64accba`, raw schema
`daec2964bb589d2087409446f99b84cfe9d6fb62b0b3af25e37363a78b170514`,
canonical formatted schema `9c05ec496e957548fe4656ca655a67a7b936ff4f220bdedae474a680e6d32eb9`,
62 definitions / 36 clauses. Its `clip.set` carrier contains neither the
producer leaves nor the position leaves. Do not describe either source as the
current full floor. The later composition must strip exact `f448`/`84fc` for
the producer unit and exact `6ba` for the position unit, then prove the
resulting 62/36 composition; no such composition or activation is claimed by
this handoff.

## Main witness

The inspected App/Main checkout is commit
`1557c312b999ddc0a21c1728acbc64052ef6491f`, tree
`cf94daef960fe1426f6f50e4000b00c0fc42867e`.

Producer witness: `src/tools/video-editor/dev/transcript-lane/extension.ts:394-419`
builds a flat output with `track`, `at`, `duration`, `clipType`, `label`,
`text`, and the flat caption box (`x`, `y`, `width`, `height`), then creates
`__generated__` metadata with `createHostGeneratedObjectMeta`. The same file at
`:421-443` uses `clip.add` for a new deterministic clip and `clip.update` for
the update; regeneration removes only matching owned/provenance clips at
`:449-467`. The metadata shape is defined by
`src/sdk/video/timeline/sourceMap.ts:251-285`.

Position witness:

- `src/tools/video-editor/lib/timeline-data.ts:44-76` declares flat top-level
  `x`, `y`, `width`, `height`, `cropTop`, `cropBottom`, `cropLeft`, and
  `cropRight`; there is no stored scale or nested position object.
- `src/tools/video-editor/components/PropertiesPanel/ClipPanelBody.tsx:408-435`
  writes the four box leaves and treats opacity as a separate property.
- `src/tools/video-editor/hooks/clip-editing/useClipPositioning.ts:21-30,46-56`
  clears the four box leaves plus the four crop leaves by removing presence.
- `src/tools/video-editor/hooks/useTimelineCommandsService.ts:732-735` shallow
  merges the clip patch and rounds only `at`; position leaves are not converted.
- Agent's `astrid/core/timeline/schema/timeline-config.schema.json:181-200`
  independently declares the same eight top-level numeric leaves; `params` is
  a separate opaque object.

## Producer carrier contract

The source extends existing version-1 `clip.set`; it adds no operation or
DTO. `args.values` is closed and adds only:

- top-level `label` (string);
- `text.content`, `fontSize`, `color`, `bold`, and `align` (known leaves);
- existing-owner `app.managedBy` and the complete `app.__generated__` JSON
  leaf.

`hold` remains source seconds. The producer leaves have no producer-specific
clear entries: omission is a no-op, and null/empty reset encodings are not
valid. Existing opaque siblings survive because execution writes known nested
leaves rather than replacing `clip`, `text`, or `app`. No IDs are allocated;
fresh rows remain on the existing complete `clip.add` path.

Guards are explicit. The selected clip must already have a non-empty
`app.managedBy`; user/unowned and foreign-owner clips refuse atomically. An
incoming owner must match. Generated metadata must already exist, retain
`extensionId` and `contributionId`, have `extensionId == managedBy`, and must
not change fixed `generatedAt` or `sourceMapEntryId`; provenance may change for
regeneration. Unknown text leaves and whole-object writes refuse. `at` and
`track` remain `clip.move` authority; geometry is intentionally not carried by
this producer source.

## Position carrier contract

The source also extends existing version-1 `clip.set`; it adds no operation,
DTO, endpoint, scene, or selected-element schema. The eight accepted values
are flat top-level leaves: `x`, `y`, `width`, `height` in raw composition
canvas pixels, and the four crop fields as raw edge fractions. There is no
clamping, normalization, rounding, defaulting, or display-scale conversion
in capture. Negative/offscreen coordinates, zero or negative sizes, and crop
fractions outside `[0,1]` remain literal finite numbers.

`clear` explicitly removes any of those eight leaves. Absence is a no-op;
null, strings, empty strings, expressions, non-finite numbers, duplicate
clears, and set/clear overlap are rejected. Opaque fields, timing, order,
source state, and unrelated occurrence state remain untouched. Parent and
explicit occurrence targets retain stable clip/owner, source/type/media, and
occurrence bindings. Original per-leaf values, including absent/null/opaque
states, are recorded as guards; same-leaf stale and ABA inverse writes refuse,
while disjoint leaves rebase.

## Concrete mismatch to resolve before consumer ACK

The Main producer witness calls the update field `duration` and emits a
`clip.update` patch, while the Agent source carrier is existing `clip.set` and
accepts `hold` (source seconds). Main also includes the flat caption geometry
in that producer output, while the producer carrier deliberately refuses
geometry. Runtime/App2 must identify the existing translation and confirm
whether one producer proposal is split into `clip.move`/`clip.set` plus the
position `clip.set`; this packet does not infer that mapping.

The position UI constrains width/height to non-negative composition bounds,
but the canonical raw schema has no such bounds. That is a UI-input narrowing,
not a reason to normalize the source carrier; the peer review should confirm
that direct command producers retain the raw numeric contract.

## Capture and source evidence

Producer source tests:

- `tests/editing_conformance/test_recipe_producer_clip_set.py::test_main_shaped_producer_capture_preserves_opaque_siblings_and_roundtrips`
- `...::test_producer_metadata_refuses_user_foreign_and_identity_adoption_without_writes`
- `...::test_producer_clip_shape_is_closed_and_geometry_stays_on_params_recipe`
- Result: **3 passed**; clip-scalar neighbours **113 passed**; schema/current-union
  focused checks **12 passed, 15 deselected** and **3 passed, 31 deselected**;
  Ruff and whitespace checks passed.

Position source tests:

- `tests/editing_conformance/test_recipe_clip_position.py::test_app_position_panel_and_reset_exact_capture_roundtrip`
- `...::test_position_set_clear_preserves_tagged_old_values_and_opaque_fields`
- `...::test_position_set_rejects_non_numeric_or_nonfinite_values`
- `...::test_position_args_are_closed_and_set_clear_are_disjoint`
- `...::test_position_disjoint_leaves_rebase_without_recapture`
- `...::test_same_leaf_unchanged_write_and_aba_inverse_refuse_stale_history`
- `...::test_position_preserves_timing_dynamic_values_and_has_no_time_dependency`
- `...::test_position_schema_is_closed_numeric_and_raw_timeline_fields_are_numeric`
- `tests/sdk/test_timeline_clip_scalar_provider.py::test_provider_position_route_accepts_parent_and_occurrence_leaves_with_inverse_redo`
- Result: **168 passed** for the position/provider lane and **34 passed** for
  the current-union schema lane; JSON validation, Ruff, and `git diff --check`
  passed.

These are source/local in-process proofs only. No Runtime/App2 generated pair,
HTTP, browser, live socket, pin, activation, or full suite was run or inferred.

## Request to Runtime/App2

Please review the exact commits, trees, schema hashes, Main witness, and the
`duration`/`hold`, `clip.update`/`clip.set`, and geometry split above. Return a
bounded source ACK or a concrete mismatch with the required field mapping.
Keep both units unfrozen until the 6ba and f448/84fc stripping checks and the
later 62/36 composition are independently reproduced.
