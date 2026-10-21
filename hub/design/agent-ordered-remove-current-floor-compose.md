# Agent ordered project-data remove current-floor composition

## Exact source

- Product: Agent / Astrid SDK timeline source, current private base `6a8dfb2286659dd67c108a230d24f14ba4599344` (`private6a8`), carrying the reviewed private voiceover/extent schema floor.
- Reviewed semantic source: Agent `b4493c75947f8605e61852f340e56b27e24c4adb` (`project-data.remove` ordered inverse).
- Current schema floor: `84fc0863a1f925f32c00b171eaf51b8f06afb7d34064296394bc8592386cbbc5`.
- Composed schema SHA-256: `c49a6058cfb49fec3dd12e8d93868de6433f121b07a56a943257e34b239f9b7c`.

## Bounded delta

Adds only the reviewed `project-data.write` `mode: "remove"` union and its ordered inverse record carrier. Removal remains the sole remove spelling: one declared key is cleared; empty target/app containers are pruned; absent target, explicit null, opaque JSON, own namespace, disjoint sibling order, serialized reload, inverse, and redo retain their guarded semantics. The b449 insertion-order record is used only when restoring a pruned map entry, preserving later disjoint siblings without parent replacement.

Changed source/test paths:

- `astrid/core/timeline/schema/edit-command.schema.json`
- `astrid/sdk/timeline/_project_data_commands.py`
- `astrid/sdk/timeline/_command_state.py`
- `astrid/sdk/timeline/_recording.py`
- `astrid/sdk/timeline/inverse.py`
- `tests/editing_conformance/test_recipe_m2_project_data.py`
- `tests/sdk/test_timeline_materialization_schema_union.py`

The existing 84fc schema is reconstructed byte-for-byte by stripping only the new remove union. Existing lower floors remain covered by the schema-neighbor guards. No frozen C3d/client/lock/generation artifact was changed, and no new DTO, endpoint, store, framework, or whole-parent replacement was added.

## Callers

None. This is source/schema composition only; Runtime, App, generated clients, pins, generation, adoption, and native workflows are untouched.

## Evidence

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime \
  /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider \
  tests/editing_conformance/test_recipe_m2_project_data.py \
  tests/editing_conformance/test_inverse_clear_batches.py \
  tests/editing_conformance/test_recording_clear.py \
  tests/sdk/test_timeline_materialization_schema_union.py \
  tests/sdk/test_timeline_current_union_schema.py \
  tests/sdk/test_timeline_composed_schema.py
=> 251 passed in 176.53s

/home/user/work/venv-agent/bin/ruff check \
  astrid/sdk/timeline/_command_state.py \
  astrid/sdk/timeline/_project_data_commands.py \
  astrid/sdk/timeline/_recording.py \
  astrid/sdk/timeline/inverse.py \
  tests/editing_conformance/test_recipe_m2_project_data.py \
  tests/sdk/test_timeline_materialization_schema_union.py
=> All checks passed

git diff --check
=> passed
```

No full suite, browser, HTTP/live socket, Runtime/App qualification, pinning,
generation, adoption, or release was run.
