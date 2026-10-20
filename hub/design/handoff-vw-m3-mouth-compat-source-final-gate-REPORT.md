# D09 presenter compatibility source final gate

## Verdict

**APPROVE the exact Agent source commit `ee71010a0` for owner review**, with
physical default/partial qualification explicitly still unclaimed.

The commit is bounded to the approved presenter compatibility seam:

- `motion.ts` preserves semantic `mouthAnchor`/`motionAt` normalization and
  derives compatibility inspection from the existing drawing helpers.
- `scene.ts` publishes the result through the existing `diagnostics.mouth`
  compatibility diagnostic. The existing `motion` diagnostic remains intact;
  no separate semantic diagnostic was erased.
- Explicit `{x:151,y:104,w:19}` remains a 799-pixel inspection crop at
  640x360; partial `{x:151,y:104}` uses legacy width 16 and is 697 pixels.
- An absent/default raw mouth is unknown and skips inspection; malformed raw
  anchors are unknown and never fabricate an ROI. Mosaic and outer-geometry
  unknowns remain conservative.
- The existing four-still 387-pixel erase control and strict `>2%` controls,
  private crop, and private statistics were not deleted or changed.

The actual registered path was inspected: Composition's existing
`prepareCompositionScene` passes the admitted effect clip through
`resolveParams`, which is a pass-through of `clip.params` for effects. The
capability therefore sees raw mouth presence before component defaults, with
no new context/type/DTO/flag/factory/clock/hash or Python geometry.

## Verification

The exact source commit diff against its parent contains only the five
expected presenter source/direct-test files. `git diff --check` passed.

Using a private `/tmp` extraction of the candidate Agent ref, a private copy
of the valid Node `v20.19.4`, the read-only f816 peer graph, and the immutable
public12 artifact (`0a7b6152...f0f1a3`):

```text
pytest -q -o addopts= -p no:cacheprovider --tb=short \
  tests/packs/rendering/test_presenter_scene_capability.py::test_presenter_existing_registered_ssr_markup \
  tests/packs/rendering/test_presenter_scene_capability.py::test_presenter_public_scene_contract \
  --basetemp=<private-temp>
6 passed in 8.27s
```

This is the existing parent-snapshot-versus-candidate SSR identity check plus
all five registered scene contract cases. The full direct targeted lane also
passed:

```text
pytest -q -o addopts= -p no:cacheprovider --tb=short \
  tests/packs/rendering/test_presenter_scene_capability.py \
  tests/packs/rendering/test_presenter_crop_equivalence.py \
  tests/packs/astrid_motion/test_astrid_motion_pack.py \
  tests/packs/rendering/test_remotion_element_generation.py \
  tests/packs/rendering/test_timeline_visualize_motion_views.py \
  --basetemp=<private-temp>
55 passed, 2 skipped in 22.55s
```

The two skips are the existing esbuild-dependent neighbour cases. No full
suite, browser, render, socket, network, install, or manifest regeneration
was run.

## Limits and next steps

This approves source behavior for owner review only. It does not qualify
physical default/partial crops, activate a production consumer, delete the
private crop/statistics path, or claim Gate 6 evidence. The Agent artifact
manifest is intentionally stale for these three changed source entries; the
Agent owner must perform the normal manifest regeneration in its own allowed
unit, and must not weaken the manifest test.
