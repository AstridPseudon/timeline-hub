# D134 finite D100 applicability map check

## Verdict

`PASS_FINITE_D100_APPLICABLE_UNAPPLIED`.

The corrected wording is supported for exactly 30 original managed-edge
selectors. The held D100 source at `42040a9c…` directly addresses the common
first physical item-birth correspondence boundary through the existing
registered `doc.patch`/provider route. This is source applicability only; it
does not qualify current behavior, setup, the all-tail, normal-home state,
REG/core, or release.

## Exact finite scope

The six unchanged original files partition the exact 30 selectors as 4 + 6 +
4 + 6 + 7 + 3. The selector strings, source SHA-256 values, byte counts,
selector AST hashes, shared `inputs()` AST hash, original `_create_fixture()`
AST hash, and assertion counts were independently compared to the author
manifest. All matched; the selectors are distinct and the partition sums to
30.

The six selector groups are:

- video unplace: image/video × keep false/true (4);
- completion auto-placement: image/video × anchor/absent plus two provider selectors (6);
- placement create/unplace: replay create/unplace plus two provider selectors (4);
- shared auto-placement: four replay cases plus two provider selectors (6);
- shot pool: three replay cases, add/remove, two promotion cases, and the pooled round trip (7);
- occurrence media: same-alias whole-payload plus provider add/swap (3).

## Common first boundary

Static source tracing on unmodified a30e shows the same boundary for all six
callers:

1. `test_commit_runtime_occurrence_media.py:_create_fixture:21-115` begins
   from the empty bootstrap and explicitly patches parent `occurrences=[]`.
2. Registered `occurrence.create` creates the physical shot with `items=[]`
   (`native_occurrence_create.py:41-50`).
3. The first authored shot patch restores `item-1`, its media/opaque fields,
   internal timeline, and managed source fields.
4. A parent occurrence leaf patch restores authored occurrence fields while
   retaining provider-managed edges.

The video-unplace caller has the same sequence directly in its setup
(`test_commit_runtime_video_unplace.py:73-143`). Auto-placement and shot-pool
call `_create_fixture` directly. Placement and shared-auto use the
`GenuineTimeline.create` wrappers, which call that same helper. Occurrence
media uses `runtime_occurrence.editing.__wrapped__`, whose setup calls the same
helper at line 227. Thus no cohort has a different first failing seam hidden
by a broad label. Their auto-placement, placement, pool, shared-owner, and
media operations are downstream and are not claimed here.

## D100 mapping and independent positive

Current a30e `State.shot_item_map` still turns an empty physical map into the
baseline item set, so the newly authored non-empty list cannot pass the strict
`_item_ids` equality check. The held 42040 `_command_state.py` changes
`shot_item_map`, `_item_ids`, and `project_shot_items` to recognize the exact
physical source case: same shot/revision/digest, same internal timeline
identity/revision/digest, empty `item_id_map`, unique non-empty physical item
IDs, and no alias-map extension. Copied/remapped placements retain strict
correspondence.

The held positive test
`test_first_physical_item_preserves_custody_and_opaque_fields` asserts that
the new item is accepted while source mappings and the empty `item_id_map`
remain unchanged. The held negative tests retain no-write refusal for changed
physical custody and copied/remapped birth, missing, duplicate, owner, and
map damage. The held product file's independently computed SHA-256 is
`018f174004bf9b9c275aa23ef6ceb432ce9d7294d71e3024f96353c25fa808a3`.

## Limits and disposition

No behavior or setup acceptance is claimed. The current joined original9 was
not rerun; its recorded App FPS declaration typed-location failure remains in
the separate reviewer2100 scope. No new API, fixture author, source rewrite,
provider/service/socket/browser/full-suite run, or refused-route retry was
performed. D100 remains held pending meaningful qualification of the current
registered path.
