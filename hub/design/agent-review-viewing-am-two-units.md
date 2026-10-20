# Agent AM two-unit review

Date: 2026-10-20. Current Agent integration: `8e3107853d17453758a933d1f47215cc1c002660`. Common candidate base: `cf7448ed6c1298b172d004914cfe2bb8c99048e7`.

## Verdicts

| Unit | Verdict | Integration condition |
|---|---|---|
| AM-sprite `9d93e66e4` | **APPROVE unit** | Land the bounded AM unit first; do not merge its stale ancestry over current Agent. |
| AM-snap-plate `48f3eef4b` | **APPROVE unit / HOLD sequencing** | Land only after sprite is separately accepted, then regenerate the normal catalog on the combined current tree. |

The product decisions are unchanged. The candidate branches are stale descendants of the common base: `current..sprite` is 59 paths and `current..plate` is 62 paths. Those broad differences include current Agent source-certification, SDK, schema, lock, and test changes. They are not part of these approvals and must not be overwritten by a branch-wide merge.

## Sprite unit

Exact commit `9d93e66e4e031b98fc042235334d1a4723006ebb`, parent `bdd02bd3f753e24092b982772bd481afc84f49da`. The common-base exclusive scope is exactly:

* `astrid/packs/astrid_motion/rendering/elements/effects/am-sprite/component.tsx`
* `tests/packs/rendering/test_sprite_scene_capability.py`
* `astrid/packs/rendering/elements/catalog.ts`

The follow-up commit itself changes only the generated catalog revision. `spriteAt` is shared by draw and capability evaluation. Declared known bounds require a resolved source and declared dimensions; alpha/decoding remains unknown; hidden frames are absent; missing/raw-invalid dimensions and decorated bounds remain unknown. Unsupported crop/entrance/exit outer geometry remains public-host `UNKNOWN`. No private crop/statistics path, D09 deletion, source factory, DTO, clock, or pixel claim was added.

### Sprite evidence

Exact candidate-tree targeted replay, using the read-only Remotion-0012 peers and Node 20.19.4:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/tmp/agt-review-am-two.yha2Dv \
ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node \
ASTRID_TEST_NODE_MODULES=/home/user/work/runtimes/agent-remotion-0012/node_modules \
/home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider -o addopts= \
  --tb=short --basetemp=/tmp/agt-review-am-two-sprite-pytest \
  tests/packs/rendering/test_sprite_scene_capability.py \
  tests/packs/rendering/test_scene_host.py \
  tests/sdk/test_timeline_checkout.py::test_check_flags_offcanvas_mixed_scale_and_damaged_sprite_by_address
# 33 passed in 106.51s
```

Additional exact-candidate checks:

```text
scripts/gen_element_catalog.py --check                         # pass
ruff check --no-cache tests/packs/rendering/test_sprite_scene_capability.py  # pass
tests/core/test_editor_element_catalog.py::test_checked_in_typescript_projection_is_current  # 1 passed
git diff --check cf7448ed6c1..9d93e66e4e  # pass
```

The handoff's independent public SSR comparison remains bounded evidence: 35/35 parent/candidate samples byte-equal, aggregate `963140ecb235706a8f4c0ab57f5ba8f17984bad9ed58fa4f3647a128d888ca2b`. This is markup identity, not physical pixel or media-alpha proof.

## Plate unit

Exact commit `48f3eef4bfe876fe2481d950ae33fa370fd03c58`, parent `c35b317c1104dda20f5ecfa59c00f7f9a9edbeae`. The common-base exclusive scope is exactly:

* `astrid/packs/astrid_motion/rendering/elements/effects/am-snap-plate/component.tsx`
* `astrid/packs/astrid_motion/rendering/elements/effects/am-snap-plate/scene.ts`
* `astrid/packs/astrid_motion/rendering/elements/effects/am-snap-plate/surface.ts`
* `tests/packs/rendering/test_am_snap_plate_scene_capability.py`
* `tests/packs/test_am_snap_plate_fill.py`
* `astrid/packs/rendering/elements/catalog.ts`

`plateSurface` is the single resolver used by draw and capability paths. It uses current props/theme resolution with `background ?? fill ?? paper`; explicit background wins over fill, an asset still draws, and a fill can draw assetlessly. Empty/raw-invalid backing remains unknown, non-opaque CSS remains unknown, and public12 outer crop/entrance/exit geometry remains unknown. No D09 deletion, private evaluator math, source factory, DTO, clock, or pixel claim was added.

### Plate evidence

Exact candidate-tree targeted replay, same read-only Remotion-0012 peers and Node:

```text
tests/packs/rendering/test_am_snap_plate_scene_capability.py
tests/packs/rendering/test_scene_host.py
tests/packs/rendering/test_scene_source_carry.py
tests/core/timeline/test_onscreen.py
tests/core/timeline/test_onscreen_more.py
tests/sdk/test_coverage_empty_cut.py
tests/sdk/test_timeline_commit_provider.py::test_move_reload_and_inverse_import_no_renderer
# 108 passed in 87.99s

tests/packs/test_am_snap_plate_fill.py
# 2 passed in 0.25s

scripts/gen_element_catalog.py --check                         # pass
ruff check --no-cache tests/packs/test_am_snap_plate_fill.py tests/packs/rendering/test_am_snap_plate_scene_capability.py  # pass
tests/core/test_editor_element_catalog.py::test_checked_in_typescript_projection_is_current  # 1 passed
git diff --check cf7448ed6c1..48f3eef4b  # pass
```

The corrected registered SSR test uses real `TimelineComposition`, `resolveHostRegistries`, and the candidate component. It proves assetless fill, image drawing, and explicit background-over-fill precedence. The handoff's independent parent/candidate SSR identity is 90/90 samples (10 variants x 9 frames), with unchanged default theme. This remains SSR/markup evidence, not physical pixel/audio or media-alpha proof.

## Protected bytes and integration limits

The following current Agent bytes are protected and were not part of either bounded AM unit. A full stale-branch merge would overwrite them; the unit must be ported/cherry-picked with current content preserved:

| Current path | Current SHA-256 | Stale candidate SHA-256 |
|---|---|---|
| `astrid/core/rendering/verified_source.py` | `c0dcabd27230f9661be59b2461c9759716daad215e1b508c8f9e73bb96e326d8` | `c6d9665a453fab9b5cc7fab644d7b684370a61d65937ee010159806bd3003b71` |
| `tests/packs/rendering/test_verified_source.py` | `aa087e5840fbe84606ef8cdf85f971e5d9a17c8038c6cad23bd8513b6467b9c5` | `707637f5c42d8dbe17722b8f042d9ee1b78f1e2eb7a45e4d58702682df3fd14f` |
| `tests/fixtures/current-union-command-schemas/published-sources.json` | `1deac01582348b27a90455c27010622280178919ee2c3daed1e0c025b571dda6` | absent |
| `astrid/sdk/remote.py` | `6d5c36420eeadc14e69f6414c843d8b5a17c5b893224b9ef364322907a2b175a` | `7103eb781b28d31a4c14d12f3249aac47113cd5a21891fa67acf9c71e557bb40` |
| `astrid/sdk/timeline/commit.py` | `524619491e5880b493f89175301098daa66cc37244e64572f8f00a93f0e3124e` | `485f7ac0d904feb40882bf9ac2e58d000268243a528a89f55d5e3e4138e26560` |
| `runtime.lock.json` | `c2ed617f38bc53e4f90dc082f082d38828d8f68a93e61776300ec7082ef23311` | `bf1009669501ce8e6c37fa9263edd9a56d8c2477f0c45950b98461d017fdf36c` |
| `docs/design/visual-compile-contract.md` | `94581609e327918152ee6779e8fb3915391c091167eba8758ecbe38a4200cbf4` | `a39616990ac476991e2490ad003fb23fa4bec93d83a4739c1137ead985f65220` |

Presenter bytes are identical across current and both candidates: `am-presenter/component.tsx` `b1dea928a4c709e1148525ceb88c704952b93fdf6f2b89c49e6e668afb7e84cc`, `presenter-core.ts` `6f3bc8fbf8f612c3ba369cfdac811294b2d53a88b853b15a8be64576d8bfe731`, and presenter motion/scene test bytes are unchanged. The PCM/source bytes are likewise identical: `compiled-audio-source-clock.mjs` `6ce210e91547d8bca901dc23fe3b06eae0d463fa18d6e1cb79d23494f5145ffc`, `normal-audio-sources.mjs` `dc260d6980f3fc6ff0340b364d810cd4310cc3c663db836ab9c84f6ee5dd14e4`, `attempt-envelope-pcm.mjs` `db7bc06d2b3c9efecac015d59d965ef4dfa718e13f1ef303f190c3831bc95719`, and `pcm-aac-stitch.ts` `c1fe9d30844b60363190d971ddef430313b58121a3e83badbbe8fec20eb1a09d`. Public12 remains unchanged: artifact SHA-256 `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`; lock SHA-256 `cca94d49f4bae0b3f16198d70ad08cd963f7d6061554d4276310deb6fe87f597`.

## Catalog sequencing

The normal catalog generator checks pass; no hand-edited digest or copied plugin registry was used. The common/current AM revisions are sprite `f88ce18c3486aca0cf5a844420b822c554ff3b3eb396ab4c1ea54430a43be5b3` and plate `9050dc21d2306b4f7c1741b3814e4b81ded364fa83b45baf0da1b168c018711c`. Sprite changes only its line to `da9e894e6ad65f4503f60a9adf80596ad88ec1436302dcf57783d880496e1966`; plate changes only its line to `95e056c78f81e0455f49511dd8569438a5b9dc5975ea9672b8fa17bfe2cea296`.

The plate candidate's catalog still contains the old sprite revision because it was built before sprite. Therefore plate is gated after sprite, and the owner must run the normal generator on the combined current tree (or prove an equivalent three-way merge) so both new revisions survive. Do not apply the plate branch's catalog file wholesale over the landed sprite catalog.

No full suite, browser journey, live socket, network, physical pixel/audio parity, Runtime admission, artifact repack, or D09 closure was run or claimed. Worktree remained clean; no product or manifest files were edited.
