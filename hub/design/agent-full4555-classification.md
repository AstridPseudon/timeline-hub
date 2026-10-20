# Agent full c13 a8a40afd classification

Date: 2026-10-20 22:41 UTC

## Result

Classified the existing run only:
`agent-full-c13-a8a40afd-integration-1020212508-4555`.

- Source: Agent commit `a8a40afd37e5560a14fa5e1a09ace6018596793e`, tree
  `b614c4d7036ad8b93517969fc595e9f43c9f8ff4`.
- The source tree is exactly the older `a8a40afd` snapshot. Current-integration
  WC2 `d30894a7a` and sheet-owner changes are outside this run.
- Environment: `/home/user/work/venv-agent-child-c13-a8a40afd`, Python 3.13.16;
  Node `/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node`, v20.19.4;
  Remotion project `/home/user/work/runtimes/agent-remotion-0013`; test Node
  modules `/home/user/work/runtimes/agent-remotion-0013/node_modules`;
  Runtime checkout `/home/user/work/runtime`.
- The selected Remotion runtime is the approved 0.0.13 package. Its installed
  package manifest is present; the full command also used the exact child
  environment named for `a8a40afd`.
- Exact command: `env -i HOME=/root LANG=C.UTF-8 PATH=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin:/nix/var/nix/profiles/default/bin:/root/.local/bin:/root/.cargo/bin:/usr/local/go/bin:/opt/node22/bin:/opt/maven/bin:/opt/gradle/bin:/opt/rbenv/bin:/root/.bun/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin ASTRID_REMOTION_PROJECT_DIR=/home/user/work/runtimes/agent-remotion-0013 ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node ASTRID_TIMELINE_SCHEMA_PYTHONPATH=/home/user/work/venv-agent-child-c13-a8a40afd/lib/python3.13/site-packages ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime ASTRID_TEST_NODE_MODULES=/home/user/work/runtimes/agent-remotion-0013/node_modules ASTRID_VIBECOMFY_CHECKOUT=/home/user/work/fixtures/vibecomfy PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent-child-c13-a8a40afd/bin/python -m pytest -q -n 3`.
- Result directory: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/agent-full-c13-a8a40afd-integration-1020212508-4555`.
- Result: **19 failed, 14,813 passed, 452 skipped, 4 xfailed, 565 subtests
  passed, 84 warnings; exit 1; 4,460.95s (1:14:20)**. There were no
  collection errors.

All 19 nodes are new against the prior full 32631 failure set except the
structure node, whose cause is new and is therefore new debt under the settled
classification rule. There are **8 new source regressions/drifts, 11 proven
setup/environment failures, no existing-baseline carryover, and no UNKNOWN**.

## Per-node classification

| Failed node(s) | Class | Proven cause and smallest owner/fix | Exact nodes to rerun after the fix |
|---|---|---|---|
| `tests/packs/rendering/test_remotion_backend.py::RemotionBackendRegistryGenerationTest::test_registry_generation_uses_pack_registry_and_composition_env`; `...::test_remotion_render_env_is_explicit_not_host_inherited`; `...::test_render_regenerates_registries_before_remotion_and_writes_props` | New source regression: test-fixture contract | `scripts/gen_effect_registry.py` now fail-closed checks the installed public Composition registry, but `_write_fake_remotion_project` in `tests/packs/rendering/test_remotion_backend.py` creates an empty fake `@banodoco/timeline-composition` directory. All three stop at `scripts/gen_effect_registry.py:153` because that fake project has no `package.json`. Fix the fixture to provision the approved package/registry API; preserve the production missing-package refusal. | The same three backend nodes. |
| `tests/packs/rendering/test_remotion_layer_tail_compat.py::test_fully_covered_pre_tail_layer_window_keeps_legacy_native_positive`; `...::test_fully_covered_pre_tail_root_callback_accepts_native_extent`; `...::test_ordinary_full_tail_and_no_clock_controls_remain_distinct`; `...::test_legacy_service_keeps_covered_pre_tail_output[0-30]`; `...::test_legacy_service_keeps_covered_pre_tail_output[150-165]`; `...::test_middle_pre_tail_window_keeps_absolute_clips_and_tail_outside_output`; `...::test_unlayered_original_clock_native_windows_unchanged[0-30]`; `...::test_unlayered_original_clock_native_windows_unchanged[150-165]`; `...::test_unlayered_original_clock_native_windows_unchanged[300-330]`; `...::test_support_and_locked_props_keep_pre_tail_positive[0-30]`; `...::test_support_and_locked_props_keep_pre_tail_positive[150-165]` | Setup/environment | Every node stops at `tests/packs/rendering/test_remotion_layer_tail_compat.py:202`: `Root callback probe requires TypeScript`, because `/home/user/work/app/node_modules/typescript/lib/typescript.js` is absent. `/home/user/work/app/node_modules` itself is not provisioned, while the immutable Remotion0013 runtime does contain TypeScript. Provision the shared App dependency set or make this test use the explicitly selected private runtime dependency without mutating shared installs. Do not skip these positive compatibility checks. | All 11 layer-tail nodes. |
| `tests/packs/rendering/test_remotion_render_contract.py::TextCardVisibleMarkupTest::test_text_card_renders_visible_markup` | New source regression: stale source path | The test reads the deleted wrapper path `astrid/packs/rendering/rendering/elements/effects/text-card/component.tsx`. Commit `c1d49291a` intentionally removed that duplicate; the current source has the local implementation at `astrid/packs/local/rendering/elements/effects/text-card/component.tsx`. The node therefore fails with `FileNotFoundError` before SSR. Update the contract to the canonical current/public component source, keeping the visible-markup and registry-identity assertions. | This TextCard node. |
| `tests/packs/rendering/test_scene_host.py::test_native_host_resolves_custom_transition_defaults_and_boundaries[end]` | New source regression: host transition boundary | The fully provisioned native host runs and returns active frames `[21, 22, 26, 29, 30, 33, ...]`, but the required `end` boundary is 22; the assertion fails with `21 == 22`. This is a behavioral mismatch in the current generated host/transition mapping, not a missing-runtime error. The smallest owner is the rendering registry/host path (`scripts/gen_effect_registry.py` and its transition-default handoff); preserve the asserted half-open boundary. | This scene-host node. |
| `tests/test_artifact_manifest.py::test_committed_artifact_manifest_is_current` | New source regression: generated artifact drift | `artifact_manifest.check()` reports 10 changed/removed entries, first `astrid/packs/rendering/elements/catalog.ts: changed`. The source snapshot contains post-manifest changes but the committed artifact manifest was not regenerated. Owner: the Agent generated-artifact path; regenerate the manifest with the test-prescribed commands on the final tree. | This artifact-manifest node. |
| `tests/test_structure_contracts.py::test_giant_file_inventory_matches_rationale` | New debt, new cause | This is the sole node overlapping prior full 32631. Prior 32631 failed on `filmstrip_cards.py` (1,968 vs 1,917). This run fails on `astrid/sdk/remote.py`: exact source count 2,824 versus rationale claim 2,727, delta 97. Update `docs/giant-file-rationale.md` after the intended source tree is final; keep the 50-line tolerance. | This structure node. |
| `tests/timeline/test_effects_catalog.py::EffectsCatalogTest::test_generator_outputs_package_owned_registries` | New source regression: public-owned registry omission | The bundled generator output omits `text-card` from `EFFECT_IDS`, while the installed public Composition 0.0.13 package contains `EFFECT_IDS = ["text-card"]`. The source-less public-winner path in `scripts/gen_effect_registry.py` filters the descriptor and does not re-add the public winner when it is already canonical. Fix that generator path so the host registry retains the public-owned ID and identity; keep the package-owned behavior asserted by this test. | This effects-catalog node. |

## Prior evidence and comparison

- Prior full 32631 report: `design/agent-full32631-classification.md`.
  It recorded 52 failures (14,760 passed) and 51 exact-new nodes caused by
  the stale 0.0.12 artifact fixture, plus the structure node as the only
  overlap. The current approved 0.0.13 run does not reproduce that 51-node
  failure family.
- Supported-environment evidence: `design/agent-baseline-109-cutlist.md`
  (the original 109-node set was 79 failed and 30 errored under the old
  0.0.8 environment) and `design/agent-baseline-recheck-0900.md` (the
  supported 0.0.10 recheck reduced that set to 23 environment nodes, three
  decision/fix nodes, one flaky node, and one unexecuted integration node).
  Those reports are evidence for the old baseline/cutlist only; they do not
  reclassify this exact c13/a8a40afd result.

## Recommended next steps

1. Repair/provision the shared TypeScript dependency evidence and rerun the 11
   layer-tail nodes; do not skip or weaken them.
2. Repair the public-registry generator and its fake Remotion fixture, then
   rerun the three backend nodes, the effects-catalog node, and the scene-host
   `end` node as separate exact targeted lanes.
3. Update the TextCard contract path, regenerate the artifact manifest, and
   refresh the giant-file rationale; rerun each exact node listed above.
4. Preserve all currently passing behavior, especially the public registry
   fail-closed check, visible SSR markup, transition boundary, package-owned
   effect identity, and the 50-line structure tolerance.

No rerun, full suite, source edit, assertion edit, skip, monkeypatch repair,
or shared-dependency mutation was performed by this worker.
