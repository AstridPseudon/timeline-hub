# Agent free-multi full-source composition

## Result

Composed the reviewed source-only `clip.move-set` implementation, capture
helper, and conformance golden into the private group/voiceover carrier in
this worktree.

Reviewed donor: `hub/timeline/agent/tl/agt-m2-free-move-set`, commit
`f0289c451` (based on `8fe7a42f7`). The new files
`astrid/sdk/timeline/_move_set.py`,
`tests/editing_conformance/test_recipe_free_move_set.py`, and
`tests/editing_conformance/fixtures/recipe_m2_free_move_set.json` are
byte-identical to that donor commit. No duplicate move-set implementation was
present before composition; the registry now has one `clip.move-set` handler.

The carrier base was the current `4d4535882` private4d source with schema
source `84fc`. Existing group and voiceover source was retained. The composed
operation preserves explicit parent/member order, same-batch `track.create`
(V3), source windows/holds/opaque fields, one guarded undo/redo, created-ID
and membership/ABA safety, and the existing schema floor. The focused replay
guard change runs full intervening read/selection validation for move-set
plans, while retaining the existing identity-only fast path for other plans.

## Schema inventory

- New canonical composed schema JSON hash:
  `ba0c42d6a9359c32d89d8088416f7bc9092481dbd05f236e4d7e6e019c9246e7`
- New inventory: 60 definitions, 34 clauses, 12 explicit v2 clauses.
- Removing only `clip.move-set` reconstructs the exact `84fc` floor:
  `84fc0863a1f925f32c00b171eaf51b8f06afb7d34064296394bc8592386cbbc5`,
  with 59 definitions, 33 clauses, and the same 12 explicit v2 clauses.
- `clip.move-set` is a new source proposal identity; original4d/84fc/C3d
  source artifacts remain immutable. No normalprivatepair request was made.

## Validation

Targeted free-multi/source lane:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider \
  tests/editing_conformance/test_recipe_free_move_set.py \
  tests/editing_conformance/test_recipe_m1_commands.py \
  tests/editing_conformance/test_recipe_add_delete_composition.py \
  tests/editing_conformance/test_recipe_m2_clip_add.py \
  tests/editing_conformance/test_recipe_clip_delete.py \
  tests/editing_conformance/test_recipe_scalar_commands.py \
  tests/editing_conformance/test_recorded_graph_roots.py \
  tests/sdk/test_timeline_semantic_reservations.py
```

Result: **462 passed** in 76.83s.

Bounded group-floor lane:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider \
  tests/sdk/test_timeline_composed_schema.py \
  tests/sdk/test_timeline_current_union_schema.py \
  tests/sdk/test_timeline_materialization_schema_union.py \
  tests/editing_conformance/test_pristine_initialize.py \
  tests/editing_conformance/test_current_group_slice.py \
  tests/editing_conformance/test_group_read_view.py \
  tests/editing_conformance/test_recipe_m2_group_migration.py \
  tests/editing_conformance/test_recipe_m2_group_move.py
```

Result: **173 passed** in 192.34s.

Focused schema/free subset:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider \
  tests/editing_conformance/test_recipe_free_move_set.py \
  tests/sdk/test_timeline_composed_schema.py \
  tests/sdk/test_timeline_current_union_schema.py \
  tests/sdk/test_timeline_materialization_schema_union.py \
  tests/editing_conformance/test_pristine_initialize.py
```

Result: **129 passed** in 195.71s.

Quality checks:

```text
ruff check astrid/sdk/timeline/_move_set.py astrid/sdk/timeline/_collections.py astrid/sdk/timeline/_recording.py astrid/sdk/timeline/capture.py astrid/sdk/timeline/commands.py astrid/sdk/timeline/rebase.py tests/editing_conformance/test_recipe_free_move_set.py tests/sdk/test_timeline_composed_schema.py tests/sdk/test_timeline_current_union_schema.py tests/sdk/test_timeline_materialization_schema_union.py tests/editing_conformance/test_pristine_initialize.py
git diff --check
```

Result: Ruff passed and the diff check was clean.

No Runtime code/DTO, App code, generation/pin/freeze/adoption, mixedwriter
fallback, full suite, browser suite, or live-socket suite was run. The three
existing App `it.fails` assertions were not changed. Runtime/App qualification
therefore remains intentionally unverified and outside this source-only
assignment.
