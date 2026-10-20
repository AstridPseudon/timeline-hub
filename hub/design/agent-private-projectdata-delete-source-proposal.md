# Agent project-data deletion source proposal

Status: **UNFROZEN proposal; Runtime and App 2 ACK required before generation or
consumer activation.** The frozen `e010e6a3…/39211e63…` source is unchanged.

## Source successor

The committed proposal is `0e341206235da8b9861c618c2a9304de6c50fa98`, with
source tree `47dfad89eac12597c1ed27410553b9396187eff2`, and its parent is
`e010e6a3868e963471244491bb6672c3e4a5135e` with tree
`70414cf6875d2c97c45f33e0a5158c80bd7391d9`. It changes
only the existing project-data source, its direct recorder proof, and the
successor schema hash assertion:

- `astrid/core/timeline/schema/edit-command.schema.json`
- `astrid/sdk/timeline/_project_data_commands.py`
- `tests/editing_conformance/test_recipe_m2_project_data.py`
- `tests/sdk/test_timeline_materialization_schema_union.py`

Successor schema SHA-256, recomputed from the committed ref:
`23b87833ca837bfafc6972e3dd4702c88525f230cb16a50ace745053afc4289c`.

`commands.py`, the operation name, Runtime ABI, endpoint, DTO, provider,
store, journal, and generated artifacts are unchanged. Removing the existing
project-data addition still reconstructs the frozen carrier hash
`613123b2760150f9f33e23485516d757359c3eaebfe02d552bc97155309aaad3`; the
ordinary-carrier reconstruction remains covered by the union tests.

## Proposed closed carrier

The existing `project-data.write` v1 operation remains the only operation:

```json
{
  "schema_version": 1,
  "op": "project-data.write",
  "version": "1",
  "select": "parent",
  "args": {
    "target": "com.example.extension",
    "key": "opaque-key",
    "mode": "remove"
  }
}
```

`ProjectDataWriteArgs` now has two closed forms:

- `mode: "replace"` requires the existing `target`, `key`, `value`, and
  `mode` fields exactly as before;
- `mode: "remove"` requires only `target`, `key`, and `mode`, and forbids
  `value`.

The target/key grammar, reserved outer-key refusal, UTF-8 key limit, and all
existing replace value/namespace limits are unchanged. Remove does not use a
null write, empty sentinel, root replace, normalization, or a second semantic
writer.

## Recorder semantics

The handler addresses only `parent.config.app[target][key]`:

- a missing target is a guarded no-op;
- a null or empty target namespace is removed as an empty namespace;
- a non-empty object loses only the declared key, preserving sibling values
  and insertion order, including present `null`, `false`, `0`, empty string,
  array, and object values;
- removing the last key removes that target namespace, and removing the last
  namespace removes empty `config.app`;
- malformed non-null/non-object target namespaces refuse visibly.

Leaf deletion is recorded with the existing `clear`/`assign` primitives. When
container pruning is required, target and `config.app` clears are recorded in
the same command, so inverse restores exact raw presence/value states and redo
reapplies the same ordered deletion. Existing project-data container claim
handling remains the disjoint-key replay seam; same-key changes, including
A→B→A, remain guarded refusals. Batches continue to execute atomically in
input order through the existing command runner.

## Evidence and gate

Fresh targeted checks in the worker worktree:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/editing_conformance/test_recipe_m2_project_data.py
=> 21 passed

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/editing_conformance/test_recipe_m2_project_data.py tests/editing_conformance/test_inverse_clear_batches.py
=> 121 passed

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/sdk/test_timeline_materialization_schema_union.py tests/sdk/test_timeline_current_union_schema.py -k 'project_data or carrier_additions or complete_reviewed_private_s2 or next_successor or added_definition or closed_union'
=> 7 passed, 45 deselected

/home/user/work/venv-agent/bin/python -m ruff check astrid/sdk/timeline/_project_data_commands.py tests/editing_conformance/test_recipe_m2_project_data.py
=> All checks passed

git diff --check
=> passed
```

No full suite, Runtime generation, Runtime HTTP qualification, App consumer
activation, pin, release, or frozen-artifact mutation was performed. Runtime
and App 2 should ACK this exact successor source and semantic floor before any
generated counterpart or native consumer work.
