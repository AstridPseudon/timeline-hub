# REQUEST CHANGES — Agent free-multi full-source contract

Reviewed source-only `922317bd58aa4db8f7cced85b37dd96038ae17df` (tree
`c0f735f1381de9c7fef621c1f1157bbd44b54201`, schema
`ba0c42d6a9359c32d89d8088416f7bc9092481dbd05f236e4d7e6e019c9246e7`,
60 definitions / 34 clauses / 12 v2 clauses) against frozen `4d4535882f1e028805c3da178bf9a7fa53696da8` / 84fc.

The three move-set donor artifacts are byte-identical to `f0289c451`:
`_move_set.py`, `test_recipe_free_move_set.py`, and its fixture. Removing
only `clip.move-set` from the candidate schema reconstructs SHA-256
`84fc0863a1f925f32c00b171eaf51b8f06afb7d34064296394bc8592386cbbc5`
(59 definitions / 33 clauses / 12 v2 clauses). No frozen 84fc/C3d source was
mutated.

## Blocking findings

### 1. Forward equal-state ABA is refused for move-set

`astrid/sdk/timeline/rebase.py:12-16` disables the `identities_only` replay
path for every plan containing `clip.move-set`, forcing complete intervening
write rejection. This conflicts with the settled PLAN rule that a forward
edit is allowed when the final value and identity are unchanged. It is
distinct from inverse/later-intent protection, where the same-value write
must remain a conflict, and from recreated identity protection.

Executable counterexample (run from this worktree):

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python - <<'PY'
import copy
from astrid.sdk.timeline._command_state import CommandError
from astrid.sdk.timeline.rebase import replay
from tests.editing_conformance.test_recipe_free_move_set import staged_drag
from tests.editing_conformance.test_recipe_m1_commands import later

original, plan = staged_drag()
head = copy.deepcopy(plan.bundle)
intervening = [
    later('parent/clip:clip-1', ['hold'], 3),
    later('parent/clip:clip-1', ['hold'], 2),
]
try:
    replay(plan, head, intervening_records=intervening)
except CommandError as error:
    print('forward_equal_value_aba:', 'REFUSED', error.kind, str(error))
else:
    print('forward_equal_value_aba: ACCEPTED')
PY
```

Observed: `forward_equal_value_aba: REFUSED intervening_write ...` even though
the final `hold` value is again `2` and `clip-1` has the same identity. Keep
the full membership/source/recreated-identity protections, but do not make a
source-value ABA publication alone reject forward replay.

### 2. The move-set quantizer rejects Main's list rational-FPS spelling

Main accepts both rational output spellings, as exercised by
`tests/sdk/test_timing_compiler.py::test_fixed_source_window_and_rational_half_frame_ties`:
`{"numerator": 30000, "denominator": 1001}` and `[30000, 1001]`.
`astrid/sdk/timeline/capture.py:39-49` accepts the mapping but falls through to
`number()` for the list. Consequently `_move_set.py:48-54` cannot perform the
required common-delta quantization for the list spelling.

Executable probe:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python - <<'PY'
from astrid.sdk.timeline._command_state import CommandError
from astrid.sdk.timeline.commands import execute
from tests.editing_conformance.test_recipe_free_move_set import basis, capture

for spelling in ({'numerator': 30000, 'denominator': 1001}, [30000, 1001]):
    bundle = basis()
    bundle['parent']['config']['output']['fps'] = spelling
    try:
        plan = execute(bundle, [capture(bundle, on=3.004)])
        rows = plan.bundle['parent']['clips']
        print(repr(spelling), 'ACCEPTED', [row['at'] for row in rows])
    except CommandError as error:
        print(repr(spelling), 'REFUSED', error.kind, str(error))
PY
```

Observed: the mapping is accepted with starts `[1.003, 3.003]`; the list is
refused as `unsupported_timing fps must be a finite number`. The common-delta
calculation must accept both existing Main spellings without falling back to a
direct 30000/1001 placement or refusing the valid list form.

## Positive evidence

- The exact same-batch `track.create(V3)` + `clip.move-set` golden passes:
  tracks `V1,V2,V3`; clip-1 `(V2,1,2)`; clip-2 `(V3,3,2)`; no
  `pinnedShotGroups`; resolved members and authored member order preserved.
- Source/membership reads, destination bindings, created-track recording,
  occupied-ID refusal, surviving-dependent refusal, exact inverse, redo, and
  JSON reload checks pass in the focused move-set probes.
- The candidate's schema/registry `resolved` integration and floor tests pass;
  the only new registry operation is `clip.move-set`, with no Runtime DTO or
  App writer changes.
- Existing source-bound carrier and v2 compatibility probes pass; move-set is
  parent-only and remains v1, while existing source-bound operations and their
  12 v2 clauses are unchanged.

## Exact tests run

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/editing_conformance/test_recipe_free_move_set.py -k 'exact_app_drag_golden_selection_order_and_created_track_are_one_unit or shared_rational_quantized_delta_preserves_windows_holds_and_opaque or half_open_destination_contacts_and_real_blockers or memberships_sources_and_aba_refuse_atomically or created_track_surviving_dependent_refuses_after_own_moves_are_reversed or create_and_two_own_move_stages_have_exact_inverse_and_redo or source_registry_reads_and_same_value_assignments_remain_guarded'
# 11 passed, 56 deselected

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider \
  tests/sdk/test_timeline_materialization_schema_union.py::test_full_move_set_schema_is_a_new_source_descendant_of_the_84fc_floor \
  tests/sdk/test_timeline_materialization_schema_union.py::test_private_extent_proposal_is_one_addition_on_voiceover_floor \
  tests/sdk/test_timeline_materialization_schema_union.py::test_removing_group_and_project_data_additions_reconstructs_private_carrier_bytes \
  tests/sdk/test_timeline_current_union_schema.py::test_next_successor_is_exactly_complete_frozen_s2_plus_reviewed_additions \
  tests/sdk/test_timeline_current_union_schema.py::test_closed_union_operation_inventory_is_exactly_the_supported_cohort \
  tests/sdk/test_timeline_composed_schema.py::test_every_registered_operation_has_closed_canonical_args_and_a_valid_golden \
  tests/editing_conformance/test_pristine_initialize.py::test_complete_s2_schema_is_retained_additively
# 7 passed

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/sdk/test_timing_compiler.py::test_fixed_source_window_and_rational_half_frame_ties
# 2 passed

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider \
  tests/editing_conformance/test_materialization_map.py::test_product_capture_json_recovery_and_exact_source_pin_across_stale_heads \
  tests/editing_conformance/test_materialization_map.py::test_source_bound_batch_preserves_earlier_stages_and_strict_inverse_guards \
  tests/editing_conformance/test_materialization_version_boundary.py::test_source_bound_v2_cannot_use_an_unverified_legacy_bundle \
  tests/editing_conformance/test_materialization_version_boundary.py::test_complete_public_s2_v1_keeps_original_capture_records_output_and_map
# 6 passed
```

Not run: full/462/173 suites, Runtime/App qualification, generation/pinning,
native, browser, live-socket, and full integration tests, as prohibited by the
brief. No repository files were changed.

## Required next steps

1. Adjust move-set forward replay so source-value equal-state ABA follows the
   settled rule while retaining membership/order, source identity, created-ID,
   inverse, and later-intent guards.
2. Normalize both Main rational FPS spellings through the shared `rate()` path
   and add a move-set regression for the list form, including the same expected
   common-delta result.
3. Re-run the focused probes and obtain the separately required Runtime/App
   qualification before treating this source-only contract as approved.
