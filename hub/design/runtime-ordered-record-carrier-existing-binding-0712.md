# Existing ordered-record carrier: concrete source answer

Date: 2026-10-21 UTC  
Scope: frozen Agent `10226a7f08a739ba3e41f8e91de6971eed63aa9d` (tree
`e2c08fbe9b21a3082db7bcf62d9677babfc15e98`) against Runtime da77
`da77e2ddc35bf07ddd8d9e1aae5e31ea69e82406` (tree
`486fe045f66182b33520bea971d31add3f713ea9`).

## Answer

The existing source-created record does carry an ordered inverse guard, but the
current generated Runtime carrier does not. The Agent reciprocal HOLD is
confirmed. There is no alternate metadata/type/side-channel carrier in the
reviewed source that makes this lossless.

No product, generation, pin, schema, or test files were changed.

## Exact source binding

- `astrid/sdk/timeline/_project_data_commands.py:114-124` computes
  `app_order = list(app["value"])`. A `project-data.write` with `mode:
  "remove"` passes it to `ctx.clear(..., insertion_order=app_order)` when the
  extension namespace is null/empty (`:119`), or after removing its last leaf
  (`:121-124`). The leaf-only removal at `:121` has no ordering field.
- `astrid/sdk/timeline/_recording.py:137-151` accepts the optional argument,
  copies it with `list(insertion_order)`, and emits the key only when
  `insertion_order is not None`. `:156-157` routes `clear` through that path.
  Thus the field is absent for ordinary writes; an explicitly passed empty
  iterable would still be emitted as `[]`.
- `astrid/sdk/timeline/_command_state.py:391` accepts the optional value.
  During a present-value restore, `:552-572` requires the target key to occur
  in the list, chooses the next surviving key (or previous surviving key), and
  rebuilds the dict in that order. The source does not separately validate the
  list's JSON type or uniqueness; the project-data source is a Python dict-key
  order, so its emitted values are strings and naturally unique.
- `astrid/sdk/timeline/inverse.py:100-102` forwards
  `write.get("insertion_order")`; the normal inverse application forwards it
  again at `:488` and `:496-497`. The generic `_patch` path also accepts the
  value at `:31` and uses it for ordered collection-alias insertion at `:70-82`.
- Rebase has no separate ordering interpretation: `rebase.py:15` checks the
  recorded addresses and `:32-35` re-executes the command. Accepted-history
  trust is structural at `commit.py:605-620` (record key set/ordinal) and
  semantic at `:716-753` (before-state checks and replay). Neither path adds
  or transports a missing field; `:742` calls `state.set` with the forward
  `after` value, where order is irrelevant for a clear.

The only frozen source command call sites that emit this field are the two
`project_data_write` calls at `_project_data_commands.py:119` and `:124`.

## Minimal real source-created record

This reuses frozen source fixture helpers and the existing test scenario
`tests/editing_conformance/test_recipe_m2_project_data.py::test_remove_pruned_namespace_restores_exact_order_after_reload_and_redo`
(`:190-210`). Input `config.app` order is:

```json
{
  "before": {"keep": true},
  "com.example.compiler-canary": {"gone": false},
  "after": {"opaque": [null, 0]}
}
```

The source-created record has these writes (the second write is the carrier in
question):

```json
[
  {
    "ref": "parent",
    "path": ["config", "app", "com.example.compiler-canary", "gone"],
    "before": {"state": "present", "value": false},
    "after": {"state": "absent"}
  },
  {
    "ref": "parent",
    "path": ["config", "app", "com.example.compiler-canary"],
    "before": {"state": "present", "value": {}},
    "after": {"state": "absent"},
    "insertion_order": ["before", "com.example.compiler-canary", "after"]
  }
]
```

After execution, the remaining app order is `["before", "after"]`. After
JSON reload, inverse restores `["before", "com.example.compiler-canary",
"after"]`; the existing source test passed. This is why dropping the field is
lossy even though the forward removal itself can appear correct.

## Current Runtime refusal

The exact generated Runtime definitions are closed and contain only
`ref/path/before/after`:

- `contract/schemas/edit-command.json:257-280`, `$defs.AgentWrite`;
- `contract/schemas/timeline-commit.json:490-554`, `$defs.CommandRecord`;
- `runtime_protocol/schemas/timeline-commit-bundle.json:501-524`,
  `$defs.AgentWrite`;
- `runtime_protocol/timeline_commit_types.py:17` and
  `packages/python/astrid_runtime_client/timeline_commit_types.py:17`;
- `packages/typescript/src/timeline-commit-types.ts:15`.

All corresponding schema/type definitions omit `insertion_order`, and the
schema sets `additionalProperties: false`. Validating the exact source record
against:

`https://astrid.haus/workspace/v1/schemas/timeline-commit.json#/$defs/CommandRecord`

reported:

```text
valid= False
error_path= ['writes', 1]
error_message= Additional properties are not allowed ('insertion_order' was unexpected)
```

This is an explicit refusal, not silent stripping. The source record does not
genuinely fit the current generated envelope.

## Smallest schema-owner alignment and handoff

The Agent schema owner should add one optional `insertion_order` property to
the semantic `$defs.AgentWrite` in
`astrid/core/timeline/schema/edit-command.schema.json`, with an array-of-string
shape and no new required field. Keep the existing source presence semantics;
do not move it into command args, metadata, or a wire alias. The Agent owner
should hand Runtime the new raw schema bytes plus source commit/tree and
SHA-256.

Runtime then needs to update its reviewed source-pin metadata and regenerate
all projections from that raw source, using the existing path:

```text
python generators/generate.py --check --agent-command-schema <exact-agent-schema>
python generators/generate.py --check
```

The first command is the read-only compatibility/check form already used for
da77; after the new source pin is accepted, the normal generation invocation
must produce the Runtime schema, bundle resources, Python types, and
TypeScript types together. Do not hand-edit generated types. Re-run the
bounded Runtime schema/type tests and this exact source probe before a new
tuple is reviewed.

## Evidence

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PROBE:$RTPROBE" \
  /home/user/work/venv-agent/bin/python <worker-scratch>/probe_ordered_carrier.py
  -> valid=False; writes[1]; insertion_order unexpected

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PROBE:$RTPROBE" \
  /home/user/work/venv-agent/bin/pytest -q -p no:cacheprovider \
  "$PROBE/tests/editing_conformance/test_recipe_m2_project_data.py::test_remove_pruned_namespace_restores_exact_order_after_reload_and_redo"
  -> 1 passed in 0.70s
```

`PROBE` is an extracted, read-only frozen Agent snapshot and `RTPROBE` is an
extracted, read-only Runtime da77 protocol package under this worker's scratch
directory. No full, HTTP, browser, socket, native, install, or old private
suite was run.
