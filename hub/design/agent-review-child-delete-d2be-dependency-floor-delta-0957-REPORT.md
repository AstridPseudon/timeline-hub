# Independent source review: APPROVE

Reviewed `d2be6511d411b1c0eb1f3b2a9c74ad3e369fb3ed`, tree
`c87a1a8a07ab486e6d52a24ff01e65b909420931`, against its parent dormant
child-delete source.

The scoped `_unreferenced(ctx, owners=[owner])` call runs before the child
clear. A surviving sibling with `app.astrid.on == "clip-b"` is refused as
`unsupported_dependency`, with the sibling ref/path, and the input remains
unchanged. The independent case retains the existing occurrence selection and
order reads, source-bound capture hook, and sibling physical isolation. The
existing exclusive/shared-source, source/order, replay/ABA, retarget, and
opaque-field behavior remains preserved.

The source-bound floor remains exactly these 13 operations:
`clip.move`, `placement.move`, `track.create`, `clip.set`, `clip.set-element`,
`track.set`, `shot.set`, `clip.set-params`, `occurrence.add-media`,
`occurrence.swap-media`, `placement.create`, `placement.unplace`, and
`shot.pool`. `clip.delete` is only in the separate additive
`SOURCE_BOUND_V2_ADDITIONS` set. The current schema has a positive v2 child
branch while the v1 branch and prior floor/hash stripping checks remain exact;
production schema SHA-256 is
`fc786bb530d197ae65a0b4f9e6e09e7d5a79ae2d28094ba0dc125d17cd71e8a8`.

## Verification

- `pytest -q -p no:cacheprovider tests/editing_conformance/test_recipe_clip_delete.py tests/sdk/test_timeline_materialization_schema_union.py tests/sdk/test_timeline_current_union_schema.py` — **128 passed**.
- `pytest -q -p no:cacheprovider tests/editing_conformance/test_materialization_map.py tests/editing_conformance/test_materialization_version_boundary.py` — **66 passed**.
- `pytest -q -p no:cacheprovider tests/editing_conformance/test_recipe_add_delete_composition.py -k delete` — **14 passed**.
- `pytest -q -p no:cacheprovider tests/editing_conformance/test_recipe_m2_parent_media.py -k 'delete or unplace or replacement_composes'` — **3 passed, 88 deselected**.
- Direct invariant probe — **passed**: exact 13-op floor, additive v2 set, positive v2 schema/command validation, unchanged schema hash, source-capture hook invocation, and isolated sibling write.
- `git diff --check` — **passed**; no source changes made in this review.

Prior repair evidence reused as unchanged: materialization/schema/version/clip **119 passed**, materialization map **41 passed**, composition delete **14 passed**, and the occurrence-delete neighbor's **30 passed / 2 pre-existing failures** as documented by the repair worker. No full, live, native, body, renderer, browser, install, registration, generation, or pin checks were run.

No counterexample or new SHA/schema defect found. Recommended next step: peer ACK and normal harness integration of `d2be`.
