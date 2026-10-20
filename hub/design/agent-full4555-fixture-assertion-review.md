# Agent full4555 fixture assertion review

Date: 2026-10-20T23:01:52Z
Reviewer: `agt-review-full4555-fixture-assertions`
Candidate: `26842a4dca9ec6285f3728c22aba38764d265491`
Meta base: `b43cd95717a5018940f5ffa4123d2db3ff34b8f0`

## Verdict

**APPROVE.** The candidate repairs the three test-file fixture/setup failures without changing product code or weakening an assertion. The 15-node targeted result supplied by the worker is green: 15 passed, exit 0. No new skip or xfail was added.

## One-to-one assertion and active-surface mapping

The candidate changes only these three files: `test_remotion_backend.py`,
`test_remotion_layer_tail_compat.py`, and `test_remotion_render_contract.py`.

| Old assertion/setup at the meta base | Equivalent active-surface assertion/setup in `26842a4dc` | Coverage judgment |
|---|---|---|
| Backend fake projects created an empty `node_modules/@banodoco/timeline-composition` directory. The three affected tests therefore stopped before their existing command-order, cwd, environment, render, and props assertions when the generator's public-registry probe required `package.json`. | `_write_fake_remotion_project()` symlinks `@banodoco/timeline-composition` to the selected runtime package; `_selected_composition_package()` requires the explicit `ASTRID_REMOTION_PROJECT_DIR`, an existing manifest, and version `0.0.13`. The fake `subprocess.run` lets the real `--input-type=module` registry probe execute while continuing to fake only generator/render commands. | Real installed public package/API is used. Existing backend assertions remain active: one generator call, command/cwd/env isolation, generator-before-render ordering, props/provenance, and no host-secret inheritance. The production missing-package refusal is not bypassed. |
| Layer-tail `_root_probe()` hard-coded `/home/user/work/app/node_modules/typescript/lib/typescript.js` and asserted that path existed. | It resolves `resolve_remotion_project_dir() / node_modules/typescript/lib/typescript.js`, asserts that selected-runtime file exists, and passes that exact path to Node. | The compatibility probe still executes the same Root callback and retains all window, clock, extent, half-open, and locked-props assertions. It now uses the immutable configured Remotion runtime rather than an unrelated App dependency. |
| D10-era TextCard probe copied the deleted `astrid/packs/rendering/rendering/elements/effects/text-card/component.tsx` into `component.mjs`, then asserted `PublicTextCard !== EFFECT_REGISTRY['text-card']` (failure means wrapper and registry identity diverge). | It obtains `resolvedTextCard = resolveElementRegistries(DEFAULT_THEME).effects['text-card']`, asserts `resolvedTextCard !== EFFECT_REGISTRY['text-card']` (failure means the public resolver and public registry diverge), then renders that resolved public component. | This is the same identity invariant on the current public seam. The actual SSR and all visible-markup checks remain: non-empty HTML, exact visible content, absolute positioning, flex layout, and no `opacity:0`. |

## D10 rationale and boundary checks

D10 physically deleted the duplicate rendering text-card wrapper. Keeping the old
source copy in this test would either fail at a dead path or recreate the retired
implementation as a fixture. The replacement resolves the component from the
installed `@banodoco/timeline-composition` public registry and renders it through
the real `renderToStaticMarkup` path with the existing Remotion providers. Thus the
test still proves visible output, while also proving public registry resolution and
identity rather than a private wrapper's re-export.

The fake-project setup is not a fake public API: it uses a symlink to the selected,
immutable 0.0.13 package and runs the real Node registry probe. The candidate does
not patch `resolveElementRegistries`, fabricate registry output, copy a renderer,
or disable production validation. In the unchanged production generator,
`_public_registry_ids()` still raises when the selected project's public package
manifest is absent (`scripts/gen_effect_registry.py:150-156`), and it still fails
closed on a missing Node executable or invalid public-registry response. The test
fixture now satisfies that boundary instead of suppressing it.

The diff adds no `skip` or `xfail`; pre-existing opportunistic skips for generated
typecheck artifacts remain unchanged. No behavior assertion was converted to a
refusal or removed.

## Evidence

The central targeted run was executed by the repair worker against the immutable
Remotion 0.0.13 environment, not rerun by this independent reviewer per the brief:

```text
env -i HOME=/root LANG=C.UTF-8 PATH=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin:/nix/var/nix/profiles/default/bin:/root/.local/bin:/root/.cargo/bin:/usr/local/go/bin:/opt/node22/bin:/opt/maven/bin:/opt/gradle/bin:/opt/rbenv/bin:/root/.bun/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin ASTRID_REMOTION_PROJECT_DIR=/home/user/work/runtimes/agent-remotion-0013 ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node ASTRID_TIMELINE_SCHEMA_PYTHONPATH=/home/user/work/venv-agent/lib/python3.13/site-packages ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m pytest -q -n 2 tests/packs/rendering/test_remotion_backend.py::RemotionBackendRegistryGenerationTest::test_registry_generation_uses_pack_registry_and_composition_env tests/packs/rendering/test_remotion_backend.py::RemotionBackendRegistryGenerationTest::test_render_regenerates_registries_before_remotion_and_writes_props tests/packs/rendering/test_remotion_backend.py::RemotionBackendRegistryGenerationTest::test_remotion_render_env_is_explicit_not_host_inherited tests/packs/rendering/test_remotion_render_contract.py::TextCardVisibleMarkupTest::test_text_card_renders_visible_markup tests/packs/rendering/test_remotion_layer_tail_compat.py::test_fully_covered_pre_tail_layer_window_keeps_legacy_native_positive tests/packs/rendering/test_remotion_layer_tail_compat.py::test_fully_covered_pre_tail_root_callback_accepts_native_extent tests/packs/rendering/test_remotion_layer_tail_compat.py::test_ordinary_full_tail_and_no_clock_controls_remain_distinct tests/packs/rendering/test_remotion_layer_tail_compat.py::test_legacy_service_keeps_covered_pre_tail_output[0-30] tests/packs/rendering/test_remotion_layer_tail_compat.py::test_legacy_service_keeps_covered_pre_tail_output[150-165] tests/packs/rendering/test_remotion_layer_tail_compat.py::test_middle_pre_tail_window_keeps_absolute_clips_and_tail_outside_output tests/packs/rendering/test_remotion_layer_tail_compat.py::test_unlayered_original_clock_native_windows_unchanged[0-30] tests/packs/rendering/test_remotion_layer_tail_compat.py::test_unlayered_original_clock_native_windows_unchanged[150-165] tests/packs/rendering/test_remotion_layer_tail_compat.py::test_unlayered_original_clock_native_windows_unchanged[300-330] tests/packs/rendering/test_remotion_layer_tail_compat.py::test_support_and_locked_props_keep_pre_tail_positive[0-30] tests/packs/rendering/test_remotion_layer_tail_compat.py::test_support_and_locked_props_keep_pre_tail_positive[150-165]
```

Result: `15 passed in 64.52s`, exit 0. No full suite was run.

Independent non-test checks on the candidate:

```text
git diff --check b43cd95717 26842a4dc                  # passed
ast.parse on all 3 changed test files                  # 3 files parsed
diff-added skip/xfail token scan                        # none
```

