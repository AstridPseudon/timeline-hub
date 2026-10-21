# App2 ordered-carrier source review

## Verdict

**SOURCE ACK; downstream readiness HOLD.** The exact Agent source candidate is
compatible with App2's acknowledged shape. App2 must wait for the matching
normally generated successor before any private pin, adoption, native
execution, or activation.

## Exact identities

- Agent commit: `ed5fd33c4a7fa9956178f9b24eb127415eaca9e6`
- Agent tree: `f4a632e4f627499e0b15d8477db9aaab78ebb3d2`
- Parent: `13a9d375be2a56842040984a78631957e7b7100d`
- Frozen Agent floor: `10226a7f08a739ba3e41f8e91de6971eed63aa9d`, tree
  `e2c08fbe9b21a3082db7bcf62d9677babfc15e98`
- Raw schema SHA-256: `6dd2b082ebdb630b4fc8ec3eeeea3b40c1eebe910c84557e45ab8fab05322b16`
- Canonical schema SHA-256: `9f5612ff34a5758ecacae948d5c0bfb1acc867d6ecb7a6af037bf8e3974fd9d6`
- Schema size: 65 definitions / 37 `EditCommand` clauses

## Source/schema result

The exact committed schema delta is only the optional `AgentWrite.insertion_order`
property: an array whose items are strings. The four existing fields remain
required and `additionalProperties: false` remains in force. No command
argument, metadata alias, endpoint, second writer, or side-channel carrier was
introduced.

The committed source uses the existing path:

- `_project_data_commands.py` takes `list(config.app)` only when pruning an
  empty namespace.
- `_recording.py` copies that optional iterable into the write only when it is
  non-`None`; ordinary absent-key writes omit the property.
- `_command_state.py` restores the target among existing sibling keys using the
  recorded order and refuses a missing target/order mismatch as
  `history_unavailable`.
- `inverse.py` forwards the same field through normal and staged inverse paths.

The independent Agent source review records the source-created prune record
with `insertion_order: ["before", "com.example.compiler-canary", "after"]`,
JSON reload, inverse, and redo restoring that exact sibling order. Its schema
checks refuse `null`, arrays containing `null`, and arrays containing non-string
values; its trusted inverse probe refuses invalid order claims such as an empty
order or an order missing the target. Ordinary absent-key removal emits no
`insertion_order` field.

The same source review's floor checks reconstruct the frozen-10226 canonical
hash `322733a57e781847e50228f91b6c6a9237ad2237406a188515c8f9da5e554bcc`, the
raw-old canonical hash
`d3274d7ed2d4bd80691472dd94daf8f4b8041fc184f39f1dd562d5de5d6a15c2`, and the
ordinary floor hash
`6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`.

## Evidence

Exact Git-object inspection performed here:

```text
git -C /home/user/peteromallet/astrid-agent show -s --format='commit=%H%nparent=%P%ntree=%T%nsubject=%s' ed5fd33c4a7fa9956178f9b24eb127415eaca9e6
=> commit/tree/parent matched the identities above

git -C /home/user/peteromallet/astrid-agent show ed5fd33c4a7fa9956178f9b24eb127415eaca9e6:astrid/core/timeline/schema/edit-command.schema.json | sha256sum
=> 6dd2b082ebdb630b4fc8ec3eeeea3b40c1eebe910c84557e45ab8fab05322b16

git -C /home/user/peteromallet/astrid-agent diff --check 13a9d375be2a56842040984a78631957e7b7100d..ed5fd33c4a7fa9956178f9b24eb127415eaca9e6 -- astrid/core/timeline/schema/edit-command.schema.json tests/editing_conformance/test_recipe_m2_project_data.py tests/sdk/test_timeline_materialization_schema_union.py
=> passed
```

Reused independent existing Agent evidence from
`design/agent-write-order-existing-carrier-schema-review.md`:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime \
  /home/user/work/venv-agent/bin/python -B -m pytest -q -p no:cacheprovider \
  --basetemp=/tmp/agt-write-order-schema-review --disable-warnings \
  [3 project-data tests] [3 schema-floor tests]
=> 6 passed in 2.00s
```

An exact-source rerun was attempted from `git archive ed5fd33c...` in a
temporary directory using the same six test nodes. It did not start because the
current environment has no `jsonschema` module (`ModuleNotFoundError`); no
dependency was installed and no shared environment was changed. The six-pass
result above is therefore reused prior evidence, not claimed as a new run here.

## Generated binding consequence and boundary

The next normal generator invocation must consume this exact schema and emit
the optional carrier in the ordinary generated AgentWrite projections (Python
optional `list[str]`, TypeScript optional `Array<string>`, and the generated
schema/resource bundle). App2 must consume those generated types; it must not
hand-edit a field, add a cast, or introduce another metadata carrier.

No App source was edited. Live callers changed: **NONE**. No private version
allocation, source freeze, generated edit, pin, adoption, native execution,
activation, full suite, browser, daemon, socket, install, or new App copy was
performed.

