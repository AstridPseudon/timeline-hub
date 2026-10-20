# Agent Main-current ordinary 6ba source stage

Date: 2026-10-20 UTC

## Result

SOURCE ONLY ordinary registry stage completed on Agent `11511a9a90c1bd38edd2638b5cecd74f159a6179` (tree `2491b3e9fb8706628e9fe93d1773eeee719b5073`). The reviewed source was applied as the exact non-pin delta from current-preserving descendant `06aadccd3e3b59f56cca3942695dfbe4c60e374e` (tree `403b89d77575d031a62f266d2859593e41bd58e1`) whose parent is `ab4e6f6a6f37e544d10e13c838007607c064b3b7`.

The frozen ordinary basis is Agent `310e54840fa5fb8eb7e51bb64ed2c34b7a1063b3` (tree `c5a8a3ec7e9e01c61c5ae31834da53bed4be406a`). The canonical schema is byte-identical to that frozen source and hashes:

```text
sha256:6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d
```

It contains 55 `$defs` and 29 closed `EditCommand` operations. The source registry imports and resolves 27 ordinary handlers; `timeline.inverse` and `timeline.restore` remain the two executor-owned operations, for the complete 29-operation schema inventory.

## Exact source closure

The worktree changes exactly the 61 paths in the reviewed `06aadccd^..06aadccd` non-pin source delta. No generated Runtime client or lock path is included.

```text
astrid/core/timeline/schema/edit-command.schema.json
astrid/sdk/remote.py
astrid/sdk/timeline/__init__.py
astrid/sdk/timeline/_clip_scalar_commands.py
astrid/sdk/timeline/_collections.py
astrid/sdk/timeline/_command_state.py
astrid/sdk/timeline/_delete_commands.py
astrid/sdk/timeline/_recording.py
astrid/sdk/timeline/_root_inverse.py
astrid/sdk/timeline/_timing_evaluators.py
astrid/sdk/timeline/commands.py
astrid/sdk/timeline/commit.py
astrid/sdk/timeline/inverse.py
astrid/sdk/timeline/native_auto_placement.py
astrid/sdk/timeline/native_initialize.py
astrid/sdk/timeline/native_occurrence_create.py
astrid/sdk/timeline/native_occurrence_media_commands.py
astrid/sdk/timeline/native_parent_media_commands.py
astrid/sdk/timeline/native_text_binding.py
astrid/sdk/timeline/native_word_anchor.py
astrid/sdk/timeline_media_replacement.py
tests/editing_conformance/fixtures/native_word_anchor.json
tests/editing_conformance/fixtures/pristine_initialize.json
tests/editing_conformance/fixtures/recipe_m2_parent_media.json
tests/editing_conformance/fixtures/recipe_m2_text_binding.json
tests/editing_conformance/fixtures/recipe_parent_media.json
tests/editing_conformance/fixtures/reviewed_native_s3.json
tests/editing_conformance/fixtures/current-union-command-schemas/agent-frozen-s2-26ef2bbb.json
tests/editing_conformance/fixtures/current-union-command-schemas/agent-word-caea687e.json
tests/editing_conformance/fixtures/current-union-command-schemas/next-command-additions.json
tests/editing_conformance/fixtures/current-union-command-schemas/text-command-additions.json
tests/editing_conformance/native_word_anchor_fixture.py
tests/editing_conformance/test_commit_runtime_media_manifest_inverse.py
tests/editing_conformance/test_commit_runtime_occurrence_create.py
tests/editing_conformance/test_commit_runtime_occurrence_media.py
tests/editing_conformance/test_commit_runtime_parent_auto_completion.py
tests/editing_conformance/test_commit_runtime_parent_media.py
tests/editing_conformance/test_commit_runtime_parent_media_swap.py
tests/editing_conformance/test_commit_runtime_text_binding.py
tests/editing_conformance/test_grouped_clip_cache_inverse.py
tests/editing_conformance/test_native_word_anchor.py
tests/editing_conformance/test_native_word_anchor_vectors.py
tests/editing_conformance/test_next_command_cohort_runtime.py
tests/editing_conformance/test_next_ordinary_union_runtime.py
tests/editing_conformance/test_pristine_initialize.py
tests/editing_conformance/test_producer_insertion.py
tests/editing_conformance/test_recipe_clip_delete.py
tests/editing_conformance/test_recipe_m2_parent_media.py
tests/editing_conformance/test_recipe_occurrence_create.py
tests/editing_conformance/test_recipe_parent_auto_completion.py
tests/editing_conformance/test_recipe_parent_media.py
tests/editing_conformance/test_recipe_text_binding_native.py
tests/editing_conformance/test_recipe_text_binding_spike.py
tests/editing_conformance/test_recorded_graph_roots.py
tests/editing_conformance/test_s3_reviewed_cohort_runtime.py
tests/editing_conformance/test_timing_retained_inputs.py
tests/helpers/trusted_seed.py
tests/sdk/test_timeline_current_union_schema.py
tests/sdk/test_timeline_pristine_initialize_provider.py
tests/sdk/test_timeline_pristine_initialize_runtime.py
tests/test_timeline_clip_replacement.py
```

The two fixture paths under `tests/editing_conformance/fixtures/` are retained exactly as ordinary source fixtures; the four current-union paths are the reviewed schema-floor fixtures. The list above was checked against the computed 61-path non-pin delta; the worktree has no other repository changes.

Excluded and unchanged: `astrid_runtime_client/__init__.py`, `astrid_runtime_client/contract_metadata.py`, `astrid_runtime_client/generated.py`, `astrid_runtime_client/timeline_commit_types.py`, and `runtime.lock.json`. The published 0.2.13 consumer pin is unchanged. No private carrier 392/84fc, materialization, project-data/remove, mute, transition, opacity, or provenance proposal paths/content were added.

## Current preservation and import closure

The current Main source paths for restore/session facade, retry/error custody, canonical read/verified-source images, extracted filmstrip cache, sheet/cut ownership, checkout/parent trim support, and Gate 3 assertions are byte-identical to the `11511a9a` base. In particular:

```text
astrid/sdk/timeline/sync.py
astrid/sdk/workspace_client.py
astrid/core/execution/generic_host.py
astrid/sdk/timeline_filmstrip.py
astrid/core/rendering/verified_source.py
astrid/packs/rendering/actions/timeline_visualize/_filmstrip_cache.py
astrid/sdk/timeline_sheet.py
astrid/sdk/timeline/checkout.py
astrid/sdk/timeline/native_checkout.py
tests/sdk/test_timeline_checkout_facade.py
tests/sdk/test_timeline_checkout_history_boundaries.py
tests/editing_conformance/test_owned_move_publish_runtime.py
tests/sdk/test_timeline_owned_move_publish.py
```

The current P1 same-batch inverse/ABA behavior and original selected-pin behavior were exercised by the preserved neighboring tests; current parent trim/clear and SDK extraction files were not replaced. The direct import probe resolved all 27 ordinary registry handlers and verified the frozen schema digest, 55 definitions, and 29 operations.

## Evidence

All pytest commands used the shared read-only Runtime source only through `PYTHONPATH="$PWD:/home/user/work/runtime"`, with bytecode and pytest cache writes disabled.

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" \
  /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider \
  tests/sdk/test_timeline_current_union_schema.py \
  tests/editing_conformance/test_pristine_initialize.py \
  tests/editing_conformance/test_native_word_anchor_vectors.py \
  tests/editing_conformance/test_recipe_m2_parent_media.py \
  tests/editing_conformance/test_recipe_occurrence_create.py \
  tests/editing_conformance/test_recipe_parent_auto_completion.py \
  tests/editing_conformance/test_recipe_parent_media.py \
  tests/editing_conformance/test_recipe_text_binding_native.py \
  tests/editing_conformance/test_producer_insertion.py \
  tests/editing_conformance/test_grouped_clip_cache_inverse.py \
  tests/editing_conformance/test_recorded_graph_roots.py \
  tests/editing_conformance/test_timing_retained_inputs.py \
  tests/test_timeline_clip_replacement.py
```

Result: **457 passed, 8 skipped** in 181.38s.

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" \
  /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider \
  tests/editing_conformance/test_recipe_clip_delete.py \
  tests/editing_conformance/test_recipe_text_binding_spike.py \
  tests/editing_conformance/test_recipe_parent_media.py \
  tests/editing_conformance/test_recipe_parent_auto_completion.py \
  tests/editing_conformance/test_recipe_occurrence_create.py \
  tests/editing_conformance/test_recipe_m2_parent_media.py \
  tests/editing_conformance/test_recipe_text_binding_native.py \
  tests/sdk/test_timeline_pristine_initialize_provider.py \
  tests/test_timeline_clip_replacement.py
```

Result: **355 passed, 1 skipped** in 36.18s.

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" \
  /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider \
  tests/editing_conformance/test_recipe_scalar_commands.py \
  tests/editing_conformance/test_recipe_clip_scalar_fields.py \
  tests/editing_conformance/test_recipe_m2_clip_trim.py \
  tests/editing_conformance/test_parent_track_label.py \
  tests/sdk/test_timeline_selected_schema.py \
  tests/sdk/test_timeline_producer_guard.py
```

Result: **354 passed** in 32.57s.

Additional checks passed:

- direct import/registry/schema probe;
- schema `cmp` against frozen `310e548` source;
- `git diff --check`;
- exact 61-path allowlist comparison;
- no generated-client/lock changes;
- no forbidden proposal path or content additions;
- no build output or cache files.

The first pytest invocation without `/home/user/work/runtime` on `PYTHONPATH` failed at collection with `ModuleNotFoundError: runtime_protocol`; this was an environment-only setup miss, and the exact targeted lanes passed with the documented read-only Runtime source path.

No full/full-* suite, old 0.2.14 live pair, localhost/browser journey, or guard bypass/API fallback was run.

## Remaining final-pin task

This is intentionally STAGED/HOLD. Runtime must first publish/provide the new Main-current ordinary014 producer and its compatible artifact. Then the Agent owner should run the normal `vendor_lock.py update` and `check` against that new producer, regenerate only the normal generated client outputs, and perform the separate consumer qualification. Do not reuse the historical `a0dca169` client or change the published 0.2.13 pin in this source stage. No live-native proof is claimed for the intentionally broader 55/29 source against the installed 0.2.13 wire.

The prospective worktree has no harness commit SHA yet; its exact uncommitted source diff hash is `1300d4ebe3b0607ea673329ec4d2ce11d19634891e2dc47009541d262d09fadd`.
