# AMsprite public bounds: ready for owner review

Completed the bounded capability task from Agent `cf7448ed6c1298b172d004914cfe2bb8c99048e7`. Only AMsprite's existing component and one new direct test file change. No SDK/check/cache/reflow/mouth changes and no caller activation or D09 retirement.

## Audit and implementation

The previous raw probe was not a realistic rendered-input fixture. It supplied no source/registry dimensions, invented params.width/height (not consumed by AMsprite), and compared unconverted positions against private layout math. Existing `project_shot_composition` plus the normal renderer `_serialize_timeline` preserve stored logical units. The normal editor `from_canvas` performs the existing grid conversion; no new projector or conversion was added.

- Raw stored x4212/y20 with a renderer-selected 16x16 source and scale8 draws at x25272/y120, size128x128. It does not draw the earlier private bbox4212,20,4340,148.
- Canvas x4212/y20 entered through normal unit conversion stores x702/y3 and draws x4212/y18, size128x128 (the existing six-pixel snap).
- The first valid compiled-input tests failed twice before the change: both returned `Component has no declared evaluated bounds`. Therefore a fixture-only correction was insufficient; the component capability was missing.

AMsprite now exposes its existing drawing geometry through `prepareSceneCapability`, forwarded by the normal generated owner dispatch into the immutable installed public12 scene host. One local helper shares held poses, entrance/blink/strip clock, scale, dimensions and rectangle with the actual component. No math copy, new public field/type, package bump, helper source outside the granted directory, or manifest change. The existing source-selection helper remains authoritative. The helper stays in component.tsx, preserving its declared source closure.

Known bounds describe the declared source/strip envelope, not occupied alpha. PNG decoding/alpha, opacity and paint presence remain UNKNOWN. Missing source/dimensions, dimensions from an unrelated static fallback, outline/shadow bounds, and unsupported outer crop/animation geometry remain explicit unknowns. No opaque assumption is made from authored alpha/opaque fields. Stamp/blink absence remains known. Original registered SSR output is unchanged across 35 samples (five cases, seven frames); aggregate SHA256 `963140ecb235706a8f4c0ab57f5ba8f17984bad9ed58fa4f3647a128d888ca2b` was recorded before refactoring.

The new positive test proves the original rocket/off-canvas, runner/run-in, overlapping scale8-vs6, and damaged-art .70/.56 source facts on compiled occurrence rows, joined by the compiler's explicit source_clip_id and selected asset key. It does not implement the SDK diagnostic join; the original SDK address-positive test is retained unchanged and passes.

Read PLAN, COMMON, current viewing INBOX, the 21:50 grant and 11:59 MAIN ruling. MAIN5/fade1/cap4 remains opacity .5; renderConfig is withdrawn and no replacement field is introduced.

## Exact validation

All commands ran from `/home/user/work/wt/vw-m3-d09-am-sprite-public-positive`. Common test prefix:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" ASTRID_NODE_EXECUTABLE=/tmp/vw-m3-agent-gate-node20.19.4/bin/node ASTRID_TEST_NODE_MODULES=/home/user/work/wt/vw-m1-ssr-snapshot/remotion/node_modules /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider -o addopts= --tb=short
```

1. Prefix + `--basetemp=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-d09-am-sprite-public-positive/pytest-final tests/packs/rendering/test_sprite_scene_capability.py tests/packs/rendering/test_scene_host.py tests/sdk/test_timeline_checkout.py::test_check_flags_offcanvas_mixed_scale_and_damaged_sprite_by_address`: **33 passed in 25.94s**. Log: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-d09-am-sprite-public-positive/targeted-final.log`.
2. After the last test-only portability adjustment (normal pinned-node resolution and default peer path), prefix + `--basetemp=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-d09-am-sprite-public-positive/pytest-portable tests/packs/rendering/test_sprite_scene_capability.py`: **17 passed in 20.44s**. Log: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-d09-am-sprite-public-positive/portable-final.log`. Includes strict TypeScript noEmit against actual public12 declarations, owner selection, source precedence, source/registry preservation, compiled geometry, run-in, mixed scales, source provenance, unknown media alpha, hidden frames, strips and unchanged registered SSR.
3. `/home/user/work/venv-agent/bin/python -m ruff check --no-cache tests/packs/rendering/test_sprite_scene_capability.py`: **All checks passed**. `git diff --check`: **exit 0**.

Initial fixture development failures are not hidden: first run failed 2 tests because track label was missing; fixing that gave the two expected missing-capability failures described above. The first expanded run had 14 pass/3 fail due to two invalid string animation references and an assertion that Remotion Img exposes src in SSR; valid object references and the actual existing elementSource helper resolved those fixture issues. SSR itself never emits decoded pixels or a src attribute here. Intermediate lint findings were corrected. No original test assertion was weakened; no skip/xfail was added.

The reused host fixture validates tar SHA256 `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`, version0.0.12 and unchanged 77 installed package files. The new test also compares all 77 bytes/digests to the archive and typechecks against its declarations. Private stages own real scope directories and leaf peer links into the clean f816 graph; shared dependencies and caches are read only. Host runtime status is replaced by the existing fixture: these are direct package/registration/SSR checks, not authenticated production-source admission or native environment qualification.

## Limits and next step

Nothing blocked in this scope. No full suite, make check, network, install, browser, render, socket, physical parity, git mutation or shared dependency write. No package or App/scene graph modifications. Review/merge this bounded unit through Agent ownership, then have the Agent caller owner join exact prepared source rows to the existing diagnostics before deleting private geometry. Other D09 positives and caller migrations remain outstanding.

Companion artifacts (flat absolute paths):
- `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-d09-am-sprite-public-positive-exact.patch`
- `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-d09-am-sprite-public-positive-filelist.txt`
- `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-d09-am-sprite-public-positive-replacement-test-map.md`
