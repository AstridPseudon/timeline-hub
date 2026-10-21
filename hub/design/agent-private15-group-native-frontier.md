# Agent private15 group native frontier

Status: one bounded C3d normal-provider consumer sequence is executable. This
does not qualify App activation, new-track groups, or free multi-move.

## Frozen source and evidence

- The reviewed Agent group source is c064
  (`c0644cf1a7b63c9bcff7f70502b953a07879c9f3`, tree
  `0699f877a4c809005536a80f5956b8051a814ef7`). Its reviewed schema digest is
  `27f2e3edaffdfc49665a858c5c1d6989dd89ef200932679b77367bc459329cfb`; the
  current private schema file in this worker is the `84fc0863...` digest.
- The current private staging point is Agent `8444290337e2f7cb22e39b995834a80cb1cc1ef2`
  (tree `238da4afbb635ca4ba3ea4730494a7bdb14c38e2`) paired to Runtime C3d
  `c3d26567ff6fe4e20a959476d40aff90ad23a0ca`. The normal provider used here is
  `create_runtime_commit_service()`; no PreparedProvider, SQL history, schema
  override, generation, or pin was added.
- The trusted ephemeral setup remains test-only: helper commit
  `54db299d6ebb9ec98649895760a4cd37cee6c147`, invoked by
  `seed_trusted_legacy_parent`. It creates the two-clip parent with the exact
  rational `30000/1001` fps, opaque/order data, and retained DocumentPin. The
  setup is not presented as an Agent migration or a public writer.

The c064 operation set used here is exactly:

- `timeline.migrate-groups` v1: `capture_migrate_groups` and `migrate_groups`
  in `astrid/sdk/timeline/new_group_commands.py`.
- `occurrence.move` v1: `capture_occurrence_move` and `occurrence_move` in
  `astrid/sdk/timeline/occurrence_commands.py`.
- The App-shaped read projection is `project_group_view` in
  `astrid/sdk/timeline/group_view.py`. It emits explicit occurrence, raw child
  clip, raw child track, and parent-track bindings. It does not infer ownership
  from display IDs or maintain a second pinned-group store.

The c064 capture/golden IDs are the inline pure tests, not checked-in JSON
fixtures in this checkout:

- `tests/editing_conformance/test_recipe_m2_group_migration.py::test_first_group_canonical_roots_full_provenance_pins_and_portable_golden`
- `tests/editing_conformance/test_recipe_m2_group_move.py::test_existing_lane_exact_app_view_capture_and_portable_golden`
- `tests/editing_conformance/test_recipe_m2_group_move.py::test_original_app_pinned_fixture_exact_existing_lane_visible_values`
- `tests/editing_conformance/test_recipe_m2_group_move.py::test_child_track_birth_is_typed_and_in_the_same_batch_and_undo`

The old group handoff (frozen commit `4a35b5a1f`) names a portable fixture
path, but that JSON file is absent from this current checkout; the executable
goldens above are the authoritative local evidence.

## Qualified sequence

`tests/sdk/test_timeline_group_migration_runtime.py::test_real_existing_lane_move_reload_inverse_exact_retry`
is parameterized over the golden and opaque parent variants and now performs
only this sequence:

1. trusted ephemeral legacy bootstrap;
2. normal C3d `timeline.migrate-groups` commit;
3. public canonical-closure reload;
4. captured `occurrence.move` onto existing parent lane V2 with explicit raw
   child lane `occurrence:new-occ/track:V2`;
5. public reload of the moved closure;
6. exact guarded inverse; and
7. retry of the inverse with the original request body and idempotency key.

Observed result is accepted migration, preserved opaque/provenance/pins,
explicit bindings, and rational-frame positions `1.001` and `3.001` for the
two children. Both parameter variants passed.

The implementation change is confined to the Runtime qualification test. No
new command, schema clause, generated client, or provider pin was introduced.

## Exact boundary still missing

The existing c064 move contract requires the destination parent output lane to
already exist. Its optional `new_child_track` only creates an occurrence-owned
raw lane; it does not create the parent lane. Therefore the App pinned-group
onto-new-V3 case still lacks an atomic, explicit parent-track creation + child
retrack/move set contract, including destination occupancy and inverse guards.

The free multi case is a separate private `clip.move-set` contract, not part of
c064 or the normal C3d tuple. Its missing contract includes one grouped
`track.create(V3)` plus move-set submission, authored member order distinct from
UI selection order, and exact parent/free-lane occupancy guards. No attempt was
made to add or qualify it here.

The original three App `it.fails` visible-outcome cases remain untouched and
were not rerun. No old lifecycle matrix or outer-speech matrix was rerun.

## Tests

Passed:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/editing_conformance/test_recipe_m2_group_migration.py tests/editing_conformance/test_recipe_m2_group_move.py tests/editing_conformance/test_group_read_view.py tests/editing_conformance/test_current_group_slice.py
85 passed in 4.75s

ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider -m integration tests/sdk/test_timeline_group_migration_runtime.py -k existing_lane_move
2 passed, 9 deselected in 5.02s

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m ruff check tests/sdk/test_timeline_group_migration_runtime.py
All checks passed!
```

The complete targeted integration file is not green because its pre-existing
negative probe
`test_public_seed_refuses_exact_rational_fps_legacy_input_atomically` expects
C3d to reject the exact rational-fps public seed after DocumentPin removal,
but frozen C3d accepts it. The precise first failure is
`tests/sdk/test_timeline_group_migration_runtime.py:58` (`DID NOT RAISE
ValidationError`). The exact command was:

```text
ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider -m integration tests/sdk/test_timeline_group_migration_runtime.py
```

It reports `10 passed, 1 failed`; this
report does not alter that expectation or add a schema override.

Not run: App Vitest/browser journeys, full suites, old lifecycle/outer-speech
matrices, new-track/free-move-set qualification, generation, or pinning.
