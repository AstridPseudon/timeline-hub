# Private candidate handoff: ordinary project-data replace

Worker: `agt-m2-project-data-replace-native-contract`

## Ownership classification

The App authored timeline projection stores extension data at:

```text
parent.config.app[extension_id][key]
```

This is the existing authoring bundle / sole EditCommand surface. Project
catalog or unplaced-project catalog state is a separate scoped operation and
is intentionally not mapped to this command.

## Candidate command wire shape

The candidate uses the existing `select: "parent"` scope and carries the
explicit extension target in the closed args schema:

```json
{
  "schema_version": 1,
  "op": "project-data.write",
  "version": "1",
  "select": "parent",
  "args": {
    "target": "com.example.compiler-canary",
    "key": "__dsl__:dsl://com.example.compiler-canary/main.json",
    "value": "{...}",
    "mode": "replace"
  }
}
```

Only `mode: "replace"` is admitted. `target` follows the existing App
extension-ID grammar (case-insensitive ASCII segment IDs, max 128 chars),
`key` is a non-empty string, and `value` is finite JSON. Opaque keys,
including `__proto__`, `constructor`, and `prototype`, remain authored data.

## Agent candidate source

- `astrid/sdk/timeline/_project_data_commands.py`
- `astrid/sdk/timeline/commands.py`
- `astrid/core/timeline/schema/edit-command.schema.json`
- `tests/editing_conformance/test_recipe_m2_project_data.py`
- `tests/editing_conformance/fixtures/recipe_m2_project_data.json`

The handler uses the existing `State`/`Recording` seam. It records container
creation only when a scope is absent/null, writes one exact key, preserves
other extension entries, and therefore gets existing guarded inverse/rebase
behavior. No store/table/endpoint or new canonical reference was added.

## Runtime pairing required before qualification

Runtime must consume the same closed `ProjectDataWriteArgs` definition and
register `project-data.write` in its provider operation registry. Its handler
must apply the command to the existing authored timeline payload at the path
above, inside the existing `/v1` commit transaction, retaining command order,
atomicity, accepted-revision identity, and idempotency behavior. It must not
route to project/catalog storage or invent a public alias. The target is an
args field; no `TargetKey` or canonical-reference extension is needed.

This file and the Agent changes are private candidate material pending
peer-review; do not freeze, release, or retire the App snapshot fallback from
this handoff alone.
