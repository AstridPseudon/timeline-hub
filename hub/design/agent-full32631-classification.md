# Agent full32631 result classification

Date: 2026-10-20

## Run

Classified only the existing run
`agent-full-remotion13-s2-integration-1020184653-32631`, source commit
`490c10ac12d55f75d698213487353a7912d33067` / tree
`bf423cf5aeee9ca9081d22c4727e8f34a905ee45`, with the owner-provisioned
Remotion0013 child. Its recorded command was:

```text
env -i HOME=/root LANG=C.UTF-8 PATH=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin:/nix/var/nix/profiles/default/bin:/root/.local/bin:/root/.cargo/bin:/usr/local/go/bin:/opt/node22/bin:/opt/maven/bin:/opt/gradle/bin:/opt/rbenv/bin:/root/.bun/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin ASTRID_REMOTION_PROJECT_DIR=/home/user/work/runtimes/agent-remotion-0013 ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node ASTRID_TIMELINE_SCHEMA_PYTHONPATH=/home/user/work/venv-agent-child-s2-c13/lib/python3.13/site-packages ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime ASTRID_TEST_NODE_MODULES=/home/user/work/runtimes/agent-remotion-0013/node_modules ASTRID_VIBECOMFY_CHECKOUT=/home/user/work/fixtures/vibecomfy PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent-child-s2-c13/bin/python -m pytest -q -n 3
```

Result: **52 failed, 14,760 passed, 452 skipped, 4 xfailed, 565 subtests
passed, 83 warnings; exit 1; 5,118.19s.** No full run was requested,
cancelled, or rerun by this worker.

The supported-env baseline was the immutable 109-node set in
`agent-full-remotion-integration-1020031037-28578`: 79 failed and 30
errored. Exact-set comparison gives **one overlap** (the structure gate) and
**51 exact-new nodes**. The four xfailed nodes remain xfailed; they were not
reclassified as green or as failures.

## Classification

### 51 exact-new nodes: SOURCE / test-fixture drift

Every node below stops in the same readiness check with:

```text
installed Remotion package manifest has unexpected version: '0.0.12'; expected 0.0.13
```

The current source expects `0.0.13` in
`astrid/core/rendering/remotion_runtime.py`, and the approved source manifest
and lock also pin `0.0.13`. However,
`tests/packs/rendering/test_render_export_task_adapter.py:43-44` still sets
`COMPOSITION_ARTIFACT` to the retained compatibility archive
`banodoco-timeline-composition-0.0.12.tgz`. Its helper installs that old
archive into each temporary runtime, so the intended schema, launch-fence,
proof, and digest assertions are never reached.

Exact node set, grouped only for readability:

- `test_trusted_schema_readiness_requires_complete_install`: [`__init__.py`],
  [`generated.py`], [`materialize.py`], [`theme.py`],
  [`timeline.schema.json`], [`validate.py`] (6).
- `test_remotion_runtime_uses_absolute_node_not_hostile_path` (1).
- `test_launch_validation_owned_waits_before_publish_and_reuse_without_probe`
  (1).
- `test_launch_validation_rejects_context_or_foreign_launch_without_fallback`:
  [`HOME-/different`], [`LANG-`], [`PATH-/other`], [`TMPDIR-/other`],
  [`ASTRID_REMOTION_VALIDATION_LAUNCH-bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb`],
  [`ASTRID_REMOTION_VALIDATION_ROLE-foreign`] (6).
- `test_launch_validation_rejects_changed_installed_content`: [`node`],
  [`cli`], [`schema`], [`lock`], [`package`], [`added_package_file`] (6).
- `test_validation_failure_never_publishes_ready_artifact_and_preserves_receipt`
  (1); `test_parent_owned_reference_survives_worker_and_renderer_filters` (1).
- `test_launch_validation_startup_import_and_optional_availability_invalidation`:
  [`editable.pth`], [`safe_finder.py`], [`native_dep/extension.so`],
  [`native_dep/resources.json`], [`sitecustomize.py`], [`idna.py`] (6).
- `test_launch_validation_missing_role_and_tampered_artifact_refuse_without_probe`
  (1); `test_launch_validation_explicitly_validates_startup_locale_transition`
  (1); `test_launch_validation_dependency_change_during_qualifying_import_refuses_publication`
  (1); `test_validation_acquisition_failure_retains_handle_and_blocks_replacement`
  (1).
- `test_launch_validation_loaded_bytecode_change_refuses_without_fallback`:
  [`delete`], [`replace`] (2); `test_schema_import_archive_absence_to_presence_refuses_without_fallback`
  (1); `test_launch_validation_oversized_artifact_refuses_before_publication`
  (1).
- `test_registry_readiness_qualifies_actual_canonical_transport_projection`
  (1); `test_launch_validation_shares_only_isolated_proof_preserving_six_registries`
  (1); `test_launch_validation_shared_proof_rejects_between_variants_and_before_publish[5]`
  (1).
- `test_launch_validation_separate_effective_contexts_have_fresh_owned_proofs`:
  [`LANG-C`], [`PATH-/different`], [`TMPDIR-/different`] (3).
- `test_launch_validation_proofs_never_cross_launch_transactions` (1);
  `test_launch_validation_changed_node_configuration_has_separate_proof` (1);
  `test_launch_validation_changed_schema_configuration_is_not_reused` (1).
- `test_launch_digest_memo_reuses_bytes_but_keeps_fences_and_fresh_consumers`
  (1); `test_launch_digest_memo_rejects_changes_at_every_fence`:
  [`same_size_restored_mtime-5`], [`add-5`], [`remove-5`], [`replace-5`],
  [`chmod-5`] (5).

This is not an installed-child/environment failure: the owner-provisioned
`/home/user/work/runtimes/agent-remotion-0013` has the approved `.13`
manifest, archive SHA
`9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`, and
lock SHA
`c4d7030bd5418d35f2246269b5aba7952d0ed69ccd0084815a0043dfbb7a4e24`.
The failure is created inside the test's temporary runtime from the source
tree's stale `.12` artifact reference.

The old10744 Sprite repair was a genuine setup/fixture registration failure
before product assertions. This run is different: the adapter tests reach
the production readiness validator, which correctly rejects the source test
fixture's old package. No Sprite-style environment repair is indicated.

### One overlapping baseline node: existing strict gap, not new

`tests/test_structure_contracts.py::test_giant_file_inventory_matches_rationale`
is the sole exact node shared with the supported 109-node baseline, so it is
not counted as a new failure and is not relabelled green. The current reason
is now `filmstrip_cards.py`: rationale claims 1,917 lines while the source
tree has 1,968 (51 over the 50-line tolerance). The baseline had the same
node red for a different inherited `generic_host.py` count mismatch. This is
source/document metadata drift for the current tree; refresh the rationale
only after the intended source tree is final, while preserving the existing
strict-gap accounting.

## Manager-next

1. Update the test helper's current-runtime fixture to install the approved
   `banodoco-timeline-composition-0.0.13.tgz` (retain `.12` only where an
   explicit compatibility test needs it). Then run the 51 exact adapter nodes
   as a named targeted lane in the correct Remotion0013 environment; do not
   rerun the full suite for this classification.
2. Refresh the `filmstrip_cards.py` rationale count against the final intended
   source tree, and retain the structure node as an explicit baseline gap
   until that documentation update is landed and verified.
3. Do not make product behavior or assertions weaker, and do not classify
   the 4 xfailed nodes as green.

## Scope limits

The classification is pinned to `490c10ac/tree bf423cf5`. Later changes
`d0a5072b`, `f82da322`, `a760ecca`, and `78ff61d5` are excluded and are not
being used as causes or evidence. No product files, assertions, shared
dependencies, runtimes, or venvs were modified. No targeted diagnostic was
needed because the exact common failure and source artifact mismatch are
visible in the immutable run log and source tree.
