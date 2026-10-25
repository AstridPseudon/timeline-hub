# D118d verdict

## First failing correspondence

The first failure is `astrid/sdk/timeline/_command_state.py:369`, reached from the real registered provider while applying the fixture’s source-item `doc.patch` at `tests/sdk/test_timeline_capture_projection.py:311`. The guard receives one candidate item row, while its authenticated baseline/source map proves zero item rows. `set(candidate_item_ids) != expected_item_ids`, so it raises `identity_conflict: shot item correspondence changed`.

This is a membership/allocation mismatch, not the earlier canonical child-row shape seam. The physical shot revision alias and source pins are accepted as the same source; the failure is the attempted introduction of a new item identity into an empty source list without an accepted allocation boundary.

## Ownership and identity distinctions

- The authoring identity is placement-local and is created only when a copied/duplicated placement remaps an existing source item. This original source placement has no pre-existing authoring item.
- An accepted physical identity would be the item identity in Runtime’s canonical shot payload and `shot_items` row. The retained run rejects before acceptance, so the candidate row never receives that status.
- The patch’s shot-revision root alias identifies the physical immutable shot image, not an item identity.
- `source_mapping.shots[...]` carries source revision custody and `item_id_map`; for this un-copied empty source the map is empty. It is not an allocation ledger and cannot authorize the new row.

## Whole-path result

Runtime registration and provider execution are genuine. The provider rejects before Runtime acceptance, persistence, or the fixture’s canonical reread. Consequently the later duplicate and saved-projection assertions are not evidence of post-setup behavior in this run. Existing source code shows the normal passing shape: once an accepted physical item exists, canonical reread supplies it; duplication then creates a placement-local alias through the source-to-authoring map. That downstream path remains unverified for this failing fixture.

No product or test files were changed. No pytest, replay, service body, full suite, or safety-held SWAP inspection was run.
