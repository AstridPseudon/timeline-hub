# Agent source union: bounded compose

Status: complete, source-only; no callers activated.

## Union identity

- Reviewed source commits: literal `f448c4b40`, corrected movement `3b3208c43`, reference/order `85c90d526`.
- Complete worktree Git tree (including uncommitted union files): `ba9229f4110070fbcf12e6a3bb8244bde7f1b5b4`.
- Complete schema file SHA-256: `daec2964bb589d2087409446f99b84cfe9d6fb62b0b3af25e37363a78b170514`.
- Canonical schema SHA-256 used by the compact schema tests: `9c05ec496e957548fe4656ca655a67a7b936ff4f220bdedae474a680e6d32eb9`.
- Schema inventory: 62 definitions, 36 closed operation clauses.

## Ported scope

- Literal f448 remove/mute/opacity floors remain intact.
- Corrected movement source ports free multi-clip movement, rational/list FPS handling, repaired ABA/rebase guards, and parent `afterClip` media birth.
- Reference/order source ports guarded unplaced raw `timeline.reference` and parent `track.reorder`, with registry registration and schema clauses.
- Same-ID ordinary parent asset refusal is explicit and covered.
- Compact stripping tests reconstruct exact f448, movement3b320, reference/order85c, and exact84fc schema floors.
- No generation, freeze, pin, public/native proof, or activation artifacts were added. No Runtime/App/Composition callers are activated.

The pre-repair free-multi source with REQUESTCHANGES was not adopted; the reviewed corrected `a19192ea7`/`3b3208c43` unit was used instead. All three exact independent source reviews used here were APPROVE. The raw reference remains dependent on the optional verified `raw_media_info` port by design; absent verification is refused.

## Tests

Passed:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -B -m pytest -q -p no:cacheprovider tests/editing_conformance/test_recipe_free_move_set.py tests/editing_conformance/test_recipe_m2_parent_media.py tests/editing_conformance/test_recipe_m2_parent_reference.py tests/editing_conformance/test_recipe_track_order.py tests/sdk/test_timing_compiler.py
239 passed in 29.57s

... tests/sdk/test_timeline_materialization_schema_union.py::test_literal_three_union_reconstructs_each_reviewed_source_floor tests/sdk/test_timeline_materialization_schema_union.py::test_full_move_set_schema_reconstructs_its_exact_source_floor tests/sdk/test_timeline_composed_schema.py
7 passed in 1.54s

... tests/sdk/test_timeline_current_union_schema.py::test_next_successor_is_exactly_complete_frozen_s2_plus_reviewed_additions tests/sdk/test_timeline_current_union_schema.py::test_closed_union_operation_inventory_is_exactly_the_supported_cohort
2 passed in 0.28s

... tests/editing_conformance/test_recipe_m2_parent_reference.py tests/editing_conformance/test_recipe_track_order.py
10 passed in 1.02s
```

`git diff --check` passed. Full suites and external services were not requested or run.

## Handoff

The harness should commit the worktree using the worker commit message. Manager/peers own later freeze, caller activation, and public qualification.
