# Agent e010 full-carrier/project-data source review

Date: 2026-10-20

## Verdict

**APPROVE — bounded source composition only.**

The e010 source is an additive project-data successor over the complete private
613 carrier. It preserves the existing carrier and ordinary floor exactly, and
the command-engine changes do not narrow or bypass the existing capture,
version, F1/P1, or created-ID guards. This is not approval for normal
generation, a schema freeze, a consumer pin, release, adoption, or a native
pair; those remain held until both manager peer reviews ACK.

## Reviewed identities

- Agent commit: `e010e6a3868e963471244491bb6672c3e4a5135e`
- Agent tree: `70414cf6875d2c97c45f33e0a5158c80bd7391d9`
- Parent/private carrier: `a53703ce66de7119b6bef51376e274b8ad6296e7`
- New schema SHA-256: `39211e63a50b9fb495fdf3feb5beaf0e4d0b4eab9a7e13f4d5f769e0d317429d`
- Reconstructed private carrier SHA-256: `613123b2760150f9f33e23485516d757359c3eaebfe02d552bc97155309aaad3`
- Reconstructed ordinary floor SHA-256: `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`
- New inventory: 56 definitions, 30 operation clauses, 12 explicit v2 branches.

## Source composition findings

`git diff a53703ce..e010e6a3` changes only the schema, the project-data
handler, the command-engine project-data path, and their focused tests. The
schema diff adds exactly one `ProjectDataWriteArgs` definition and one
`project-data.write` conditional. Removing those two additions reproduces the
frozen 613 bytes; the existing carrier-only projection then reproduces the
ordinary 6ba floor. No existing definition, operation clause, v2 branch, or
source-bound materialization rule is edited.

The handler is bounded to `parent.config.app[target][key]`: target/key/mode
validation is closed, values remain finite opaque JSON, and only the requested
leaf is written. Existing namespace members are not normalized or replaced.
`ctx.object` records missing/null/empty container births and refuses malformed
non-object/non-null shapes.

In `astrid/sdk/timeline/commands.py`, the new claim exception is limited to
`project-data.write`, `parent`, and exactly the `config`, `config.app`, and
target namespace paths. It permits a disjoint replay through an absent, null,
or object container, but the requested leaf remains an ordinary authoritative
expectation. A same-leaf change therefore still fails, and malformed container
shapes fail visibly before any write.

The generalized `expect`/`reads`/`authorship` comparison remains exact for
every non-project-data operation: missing authoritative claims fail, and extra
claims fail unless they are the narrowly recognized project-data containers.
For project-data, extra container claims are accepted only with the expected
absent/null setup state (and `direct` authorship); they cannot replace or omit
the authoritative leaf. The pre-existing v2 completeness gate, source-closure
requirement, materialization capture, inverse handling, and created-identity
collision checks remain in place. No `capture.py`, `inverse.py`, or
`_materialization.py` source was changed.

## Evidence

Read-only identity/source checks:

```text
git rev-parse e010e6a3868e963471244491bb6672c3e4a5135e^{tree}
  70414cf6875d2c97c45f33e0a5158c80bd7391d9
sha256sum astrid/core/timeline/schema/edit-command.schema.json
  39211e63a50b9fb495fdf3feb5beaf0e4d0b4eab9a7e13f4d5f769e0d317429d
git diff --name-status a53703ce e010e6a3
  M schema/edit-command.schema.json
  A astrid/sdk/timeline/_project_data_commands.py
  M astrid/sdk/timeline/commands.py
  A focused project-data test
  M two carrier inventory tests
```

Bounded Agent tests (no full suite, whole-root pytest, sockets, or browser
suite):

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider \
  tests/sdk/test_timeline_materialization_schema_union.py::test_removing_only_project_data_addition_reconstructs_private_carrier_bytes \
  tests/sdk/test_timeline_materialization_schema_union.py::test_only_carrier_additions_separate_union_from_exact_complete_ordinary_source \
  tests/sdk/test_timeline_materialization_schema_union.py::test_complete_reviewed_private_s2_is_preserved_without_a_copied_frozen_schema \
  tests/sdk/test_timeline_current_union_schema.py::test_next_successor_is_exactly_complete_frozen_s2_plus_reviewed_additions \
  tests/sdk/test_timeline_current_union_schema.py::test_closed_union_operation_inventory_is_exactly_the_supported_cohort \
  tests/editing_conformance/test_recipe_m2_project_data.py::test_disjoint_keys_rebase_and_same_key_aba_refuses \
  tests/editing_conformance/test_recipe_m2_project_data.py::test_disjoint_key_rebase_births_an_absent_namespace_without_losing_the_other_key \
  tests/editing_conformance/test_recipe_m2_project_data.py::test_replace_preserves_namespace_and_restores_absent_null_and_opaque_values \
  tests/editing_conformance/test_materialization_map.py::test_source_bound_batch_preserves_earlier_stages_and_strict_inverse_guards
  10 passed in 3.64s
```

The selected nodes were the private-carrier reconstruction, ordinary-floor
reconstruction, complete S2 preservation, exact 56/30 inventory, project-data
same-leaf ABA refusal, absent-namespace disjoint rebase, exact inverse/redo,
and the existing scoped non-project-data v2/F1 capture control.

The read-only in-memory probe covering same-leaf stale replay, malformed
config/app/target namespace refusal, and retained leaf expectation also passed:

```text
PASS same-leaf refusal, malformed namespace refusal, and leaf guard preservation
```

Existing unsafe-capture/version and created-ID controls passed without source
edits:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider \
  tests/editing_conformance/test_materialization_version_boundary.py::test_v1_placement_version_flip_cannot_supply_source_proof_and_v2_reauthor_succeeds \
  tests/editing_conformance/test_materialization_version_boundary.py::test_sealed_v2_missing_original_proof_fails_closed \
  tests/editing_conformance/test_materialization_map.py::test_item_identity_cannot_be_allocated_twice_inside_one_recipe \
  tests/editing_conformance/test_recipe_m2_placement_create_unplace.py::test_later_consumer_of_created_binding_blocks_inverse
  10 passed in 2.62s
```

No generation, pin, freeze, release, integration, or native-pair command was
run. The Runtime ACK's known normal-generation prerequisite (root export and
inventory update before private regeneration) remains downstream work.
