# Agent AM snap-plate current-artifact gate

Date: 2026-10-20

## Scope and source

Worker base: `ded9b0c9` (`feat(rendering): gate current AM-sprite artifact`).
The approved plate unit from `48f3eef4bfe876fe2481d950ae33fa370fd03c58` was ported
after the reviewed sprite source. No integration worktree or frozen branch was
modified. The five plate source/direct-test files below are byte-identical to
the approved commit:

| File | SHA-256 |
| --- | --- |
| `astrid/packs/astrid_motion/rendering/elements/effects/am-snap-plate/component.tsx` | `93fc2fb7ab03a4d64d9e1c53a9a40de6de75860576b77f5b6f2c31cbd9c292ee` |
| `astrid/packs/astrid_motion/rendering/elements/effects/am-snap-plate/scene.ts` | `e43bb6dfe94a770df11e21bcf5e959e9591387d7952dda11176c79fc9e2c686e` |
| `astrid/packs/astrid_motion/rendering/elements/effects/am-snap-plate/surface.ts` | `5c844e62bd6d32673d16ad17d61435380050ffbe2cb92036d2251ac3579edd49` |
| `tests/packs/rendering/test_am_snap_plate_scene_capability.py` | `4008e2531149329d59ac821557d8ed5316f977499fda9ca20307ddb317064820` |
| `tests/packs/test_am_snap_plate_fill.py` | `dba93ca344215033cd910d5635a60f543c33203f91918884038f0076f80555f9` |

The normal generated files after refresh are:

- `astrid/packs/rendering/elements/catalog.ts`: `e981170d497f9483aa4682bee9defba367b6fdb155071420a19e8e827f59dcba`
- `artifacts.json`: `6963e3393d22b8e46d1df5f2cb81f401bee7080407bd3f61f108560a2ef9a176`

The reviewed sprite row/digests remain exact:

- catalog revision: `am-sprite = sha256:da9e894e6ad65f4503f60a9adf80596ad88ec1436302dcf57783d880496e1966`
- manifest digest: `am-sprite/component.tsx = sha256:fc79cee164d9d7aeb2a008d9d924e7b41710856b0b630bbc91137ff504b5172e`

## Evidence

- `PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q tests/packs/test_am_snap_plate_fill.py` — **2 passed**.
- `ASTRID_TEST_NODE_MODULES=<private /tmp overlay of current Remotion peers> ASTRID_TEST_COMPOSITION_ARTIFACT=/home/user/work/runtimes/agent-remotion-current/artifacts/banodoco-timeline-composition-0.0.12.tgz ASTRID_NODE_EXECUTABLE=/home/user/work/node-v20.19.4-linux-x64/bin/node PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q tests/packs/rendering/test_am_snap_plate_scene_capability.py` — **14 passed in 45.85s**. This includes the real registered public Composition SSR coverage; pinned Node was `v20.19.4`, Remotion peers were private symlinks, and shared dependency trees remained read-only.
- `python3 scripts/gen_element_catalog.py` — pass; normal catalog refreshed.
- `python3 scripts/artifact_manifest.py` — pass; wrote manifest version `sha256:2f525459601d8a3adfd29825b40a7522e536c6e809795691fa39c3e9d8b474e6`.
- `python3 scripts/gen_element_catalog.py --check` — pass.
- `python3 scripts/artifact_manifest.py --check` — pass (`artifacts.json is current`).
- `git diff --check` — pass.

## Protected bytes

The following were unchanged from this worker's exact `ded9b0c9` base and were
recorded with these hashes:

| File | SHA-256 |
| --- | --- |
| `astrid/core/rendering/verified_source.py` | `c0dcabd27230f9661be59b2461c9759716daad215e1b508c8f9e73bb96e326d8` |
| `tests/packs/rendering/test_verified_source.py` | `aa087e5840fbe84606ef8cdf85f971e5d9a17c8038c6cad23bd8513b6467b9c5` |
| `tests/fixtures/current-union-command-schemas/published-sources.json` | `1deac01582348b27a90455c27010622280178919ee2c3daed1e0c025b571dda6` |
| `astrid/sdk/remote.py` | `7f6e67cde9e6de48dbd3ffdb603d5cbd46ab23bf87dcd0e037d6e54418f033ff` |
| `astrid/sdk/timeline/commit.py` | `25920c4c155d81cf66a807e0129b7289b76c02ab7988054231b459bab56d4c5f` |
| `runtime.lock.json` | `c2ed617f38bc53e4f90dc082f082d38828d8f68a93e61776300ec7082ef23311` |
| `docs/design/visual-compile-contract.md` | `94581609e327918152ee6779e8fb3915391c091167eba8758ecbe38a4200cbf4` |
| `remotion/artifacts/banodoco-timeline-composition-0.0.12.tgz` | `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3` |
| `remotion/package-lock.json` | `cca94d49f4bae0b3f16198d70ad08cd963f7d6061554d4276310deb6fe87f597` |

The two SDK hashes differ from the older small-unit review's 6a6d92d snapshot,
but are unchanged on this worker base; no SDK files were edited here.

## Remaining gates / limits

This is only the approved Agent AM plate unit. No full suite, browser journey,
live socket, Runtime admission, physical pixel/audio parity, artifact repack,
Composition 0.0.13 change, D09 closure, private-crop deletion, or legacy-caller
deletion was run or claimed. Sprite manager acceptance/merge remains the prior
gate; this worker preserved its current source/catalog row and did not perform
integration mutation.
