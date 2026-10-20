# Opaque item remap contract — M1, 2026-10-20

Integrated Agent: `a610cd304ba22fe89d132e00bc9bbe2561032aae`, tree `8f046de1844963feab3732cb4ffda7064c49f64e`; approved worker chain ends `a76c6537c816c3f3023b7d78edbe75210d7a69f5`. Context-aware helper first introduced by `875a9aff4e658def3fa912cacd13f28a911fe89a`.
Source: `astrid/core/timeline/authoring_bundle.py::_remap_known_item_references` (line229 on integrated source). App owns the equivalent `authoringBundle.ts` port and permanent parity tests; no schema, command argument, compiler seed or wire change.

The helper accepts a complete shot payload and the exact source-item→materialized-item map. Deep-copy the payload, then inspect ONLY its top-level `items` records:

1. Each item's authoritative identity is `item_id` if that key exists, otherwise `id`. Remap the identity only through an exact key in the supplied map. When both identity keys exist, remap `id` as a mirror ONLY when its original value equals the authoritative original `item_id`; a different secondary `id` is opaque and stays literal.
2. The known source-dependency descriptor is `item.metadata` when it is an object/mapping; otherwise it is the item record itself. At that ONE descriptor location, remap string-valued `source_item_id` and `source_item` through the exact map. Non-string values and unmapped strings are unchanged. Do not inspect record fallback fields when object metadata exists.
3. Everything else is preserved exactly: unknown keys, namespaced data, values, null versus absence, list order, opaque secondary IDs, repeated strings, nested metadata/data/app/opaque objects, and strings equal to an item ID. Key spelling alone confers no reference meaning. In particular, `foreign_item_id`, `foreign_item_ids`, `selected_item_id`, `parent_item_id`, and nested `item_id` are NOT recursively remapped.

Known source-link consumers are `astrid/packs/shots/dependencies.py::_meta/_descriptor` and Runtime `runtime_protocol/shot_dependencies.py::_meta/_descriptor`. This is an explicit codec/context rule, never an arbitrary suffix search. New declared reference locations require their own reviewed schema/consumer rule; this fix does not infer them.

Permanent fixture/test sources on the integrated commit:

- `tests/timeline/test_authoring_bundle.py`: eight direct item-codec/remapper/compiler cases at the end of the file; all three codecs (`item_id`, `id`, equal mirrors), non-mirror opaque `id`, metadata versus record fallback, unknown nested namespaces, null/order/source immutability and known-source-link positives.
- `tests/editing_conformance/test_commit_runtime_opaque_items.py`: `opaque()`, parameterized `opaque_film`, `assert_preserved`; six REAL Runtime cases across the three codecs. The namespace fixture is `org.example.notes/v1`, with foreign IDs/list/null/nested item-like keys. Move→accept→immutable readback→restart/exact persisted request/key retry→undo preserves all namespaces and the complete original canonical closure. No xfail.
- `tests/editing_conformance/test_commit_runtime_shared_inverse.py`: ten REAL shared-source cases, including exact undo→redo→second undo and stable rematerialization, newer disjoint siblings/parent and ABA refusals.
- `tests/editing_conformance/test_recipe_m1_commands.py::test_reverse_materialization_alias_requires_exact_source_and_occurrence`: exact scoped identity positive and source/project/timeline/owner refusal controls.

Final central proof `agt-m1-shared-redo-compat-opaque-preservation-integration-1020015432-27788`: **23 passed in29.21s**, exact integrated tree above + Runtime `9f9b25c000485e919f30f1411831fe2d5a3c1316`. Command: `env ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q -m integration tests/editing_conformance/test_commit_runtime_opaque_items.py tests/editing_conformance/test_commit_runtime_shared_inverse.py tests/editing_conformance/test_commit_runtime_identity.py tests/editing_conformance/test_commit_runtime_m1.py tests/sdk/test_timeline_commit_provider_runtime.py`.

Historical publications are never rewritten. Original corruption evidence is `managers/agent/notes/opaque-remap-probe.md`; full integration review is `managers/agent/notes/m1-opaque-final-review.md`. One postmerge full is running separately; 23 passing cases do not claim full-green, owner-film inspection or App parity. M1 closure now also waits Runtime's explicit-null-speed preservation and App's parity port per orchestrator01:58.
