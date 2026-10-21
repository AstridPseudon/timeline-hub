# Agent existing write-order carrier schema review

Decision: **APPROVE the exact Agent source candidate** `ed5fd33c4a7fa9956178f9b24eb127415eaca9e6` on parent `13a9d375be2a56842040984a78631957e7b7100d`.

## Exact artifact identity

- Commit: `ed5fd33c4a7fa9956178f9b24eb127415eaca9e6`
- Tree: `f4a632e4f627499e0b15d8477db9aaab78ebb3d2`
- Raw `astrid/core/timeline/schema/edit-command.schema.json` SHA-256: `6dd2b082ebdb630b4fc8ec3eeeea3b40c1eebe910c84557e45ab8fab05322b16`
- Canonical schema SHA-256 (`json.dumps(json.load(schema), indent=2) + "\\n"`): `9f5612ff34a5758ecacae948d5c0bfb1acc867d6ecb7a6af037bf8e3974fd9d6`
- Candidate schema shape: 65 definitions / 37 `EditCommand` clauses.

## Review result

The worker delta is limited to three files: the semantic schema and two focused test files. The only product-schema change is the existing optional `AgentWrite.insertion_order` property, an array whose items are strings; it is not required and `additionalProperties` remains closed. No operation, command argument, DTO, store, generator, pin, freeze, endpoint, or Runtime/App source was introduced.

The existing project-data remover emits the carrier only when pruning an empty/null namespace. For an input `config.app` order of `["before", TARGET, "after"]`, the recorded namespace write carries exactly that list. After JSON reload, the existing guarded inverse restores `["before", TARGET, "after"]`, and redo returns the removed `["before", "after"]` state byte-for-byte. An ordinary absent-key removal emits no `insertion_order` key.

Schema validation refuses the malformed carriers `null`, `["before", null]`, and `[1]`. A direct probe through the existing trusted inverse boundary also refused `[]` and `["before", "after"]` (missing target) with `history_unavailable`. The source-generated carrier is a Python dict-key order and is therefore unique and complete; the unchanged trusted-provider path does not impose a separate uniqueness/membership schema constraint. Duplicate/extra strings are ignored as non-members by the existing setter and still produced the exact restored sibling order in the probe.

The predecessor reconstruction remains canonical `322733a57e781847e50228f91b6c6a9237ad2237406a188515c8f9da5e554bcc`; the existing raw-OLD floor remains canonical `d3274d7ed2d4bd80691472dd94daf8f4b8041fc184f39f1dd562d5de5d6a15c2`; and the ordinary floor remains `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`. The focused floor tests passed.

This is approval of the Agent source/schema correction only. It does not approve a generated Runtime wire tuple or downstream pin/adoption; those remain the separately required next step.

## Evidence

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime \
  /home/user/work/venv-agent/bin/python -B -m pytest -q -p no:cacheprovider \
  --basetemp=/tmp/agt-write-order-schema-review --disable-warnings \
  tests/editing_conformance/test_recipe_m2_project_data.py::test_remove_pruned_namespace_restores_exact_order_after_reload_and_redo \
  tests/editing_conformance/test_recipe_m2_project_data.py::test_remove_absent_key_omits_order_carrier \
  tests/editing_conformance/test_recipe_m2_project_data.py::test_private_schema_and_registry_are_closed \
  tests/sdk/test_timeline_materialization_schema_union.py::test_write_order_successor_preserves_frozen_10226_schema_bytes \
  tests/sdk/test_timeline_materialization_schema_union.py::test_only_carrier_additions_separate_union_from_exact_complete_ordinary_source \
  tests/sdk/test_timeline_materialization_schema_union.py::test_transcript_successor_strips_to_exact_raw_old_schema
=> 6 passed in 2.00s

git diff --check 13a9d375be2a56842040984a78631957e7b7100d..ed5fd33c4a7fa9956178f9b24eb127415eaca9e6
=> passed
```

No full, native, HTTP/socket, generation, pin, freeze, or adoption run was performed.
