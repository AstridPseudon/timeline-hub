# occurrence.duplicate v1 — candidate source contract (HELD)

Owner: agt-m2-occurrence-duplicate-b (continuation of agt-m2-occurrence-duplicate, which was lost to a usage limit with no WIP).
Base: tl/agt-m2-bundle2-final-qualify 027bd16d. Branch: tl/agt-m2-occurrence-duplicate-b (harness commit pending).
Status: candidate only. Not a change to the frozen Bundle 2 release/ref. Normal Runtime schema generation and consumer pins remain required. M2 integration remains HELD until PLAN records M1.

## Closed call

`{schema_version:1, op:"occurrence.duplicate", version:"1", select:"occurrence:<raw source occurrence id>", args:{occurrence_id:"<reserved new id>", shot_id:"<reserved new shot id>"}, intent:{ownership:"occurrence"}}`

- Python capture: `astrid.sdk.timeline.native_occurrence_duplicate.capture_occurrence_duplicate(bundle, owner, occurrence_id, shot_id)`.
- Golden: `tests/editing_conformance/fixtures/recipe_m2_occurrence_duplicate.json` (shared-shot source, 2 occurrences).
- Schema: new `OccurrenceDuplicateArgs` (closed, both IDs required, no `::` or `/`) plus one conditional dispatch entry. Existing definitions are untouched.

## Decision: independent copy, not source-bound reuse

Evidence from App HEAD (tl/integration):
- `src/tools/video-editor/components/AstridTimelineEditor.tsx` `handleDuplicateDocumentShotGroup` (≈L390-420) is the only live canonical duplicate caller. It calls `duplicateIndependentShot`, then publishes, and toasts "Independent shot duplicated".
- It is reached from the shot-group context menu item "Duplicate shot" (`ShotGroupContextMenu.tsx`), which passes the canonical occurrence identity.
- `duplicateLinkedOccurrence` (`shotCompositionEditor.ts`) has no non-test caller. Source-bound reuse therefore has no UI intent and is not implemented.

## Reserved and derived identities

- Reserved by the caller: the new occurrence ID and the new authoring shot ID. Both must be absent. The source's shot and occurrence IDs must differ.
- Derived, deterministic, collision-checked: item IDs (`_copy_shot_for_placement`, from project, timeline, new occurrence, new shot, source item). The compiled shot revision and internal timeline revision use the existing content-addressed `authoring-*-revision-*` identities.
- Tracks and clips: owned by the copied internal timeline, which is scoped to the new shot. They need no separate reservation.

## Writes and guards

- Exactly two creates: root `shot:<shot_id>` (`payload` = source's published content with remapped items, `internal_timeline` = exact copy) and root `occurrence:<occurrence_id>` (the source row, verbatim, with only `occurrence_id`/`shot_id` replaced and revision keys dropped).
- No source mutation, no parent-array write, no registry or physical purge.
- Guards: whole source row; its shot_id and published payload; its internal source; owner-scoped clip and track selections; a non-empty `pinnedShotGroups` returns `migration_needed`. Creates refuse occupied identities and derived item collisions with no mutation.
- Ordering: the copy is appended to the placement list. Its `at_ms` equals the source's, as in App `duplicateIndependentShot`, and no blocker check is run.

## Inverse and replay

- Inverse is the existing root-create inverse. No generic correction was needed (the delete branch needed one). Undo removes both roots, and redo reproduces the exact copied document.
- Inverse refuses every equal-value or ABA publication on source row, shot_id, shot payload, and internal source.
- Ordinary replay (identities_only) refuses on whole-row and source-clip ABA. It admits equal-value `shot_id` and shot-payload ABA, because the final-head value guard passes and the copy is identical. This is the engine's value-level policy and is pinned by a test.

## Dependency on the delete branch

`State.get` now serves `occurrence:<id>/shot` with `["payload"]` as the source-published payload, through `_remap_known_item_references` with the inverse of `item_id_map`. This is the same hunk as `tl/agt-m2-occurrence-delete`. If both land, the hunk must be identical.

## Known blocker for App adoption (decision needed)

App writes `stable_deep_link` and `output_identity` on each canonical occurrence row (`shotCompositionEditor.ts` L106-107). Both embed the occurrence ID. The Agent op copies them verbatim, so the copy would carry the source's values. This is pinned as a strict xfail `test_copy_does_not_carry_source_derived_identity_fields`. The App must supply reserved replacements, or the Agent contract needs an explicit args extension. The op does not invent that authority.

## Verified (targeted)

- `tests/editing_conformance/test_recipe_occurrence_duplicate.py`: 32 passed, 1 strict xfail (see report).
- `tests/editing_conformance` + `tests/timeline`: 1642 passed, 4 skipped.
- `tests/sdk -k timeline`: 935 passed, 2 skipped.
- ruff on changed files: clean. mypy on the new module alone: clean. Structure, import-cycles, and doc-refs gates pass.

## Hashes (sha256)

- `astrid/sdk/timeline/native_occurrence_duplicate.py`: `551302c17ba42326a3ccfdbf516126bdf35f4a423e5871f7598523978afbae3a`
- `astrid/core/timeline/schema/edit-command.schema.json`: `62c5719875548838bed440a58cd38acfd786ae1ea64230637b8c115e21367cdb`
- `tests/editing_conformance/fixtures/recipe_m2_occurrence_duplicate.json`: `2d0009f60947d4f5f2f8f8f204827315c14319f20da0373789578d0076b39b9f`
- `tests/editing_conformance/test_recipe_occurrence_duplicate.py`: `912ae2a699b399d30d84b3868bfe9f3e22a4a7acf0dae39d828925ca2a6b593f`

## Not verified here

Runtime generation, real Runtime/browser/restart reload, App native capture and reload, and the mypy baseline script (which fails on yaml stubs and numpy stubs in this environment, not on this change). No full suite was requested.
