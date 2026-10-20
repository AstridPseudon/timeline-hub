# Agent owner review: presenter mouth partial compatibility

## Verdict

**REQUEST CHANGES** for exact source commit `ee71010a0947edcbbacbf8178e5fee11ab6bab3d` (tree `9e9971d62a870173af6065cc0af9ee8b79011ecc`), reviewed against current Agent `acc17162dd57b2cafc966098e44625ea25bfe461` (tree `553ced9239bf063b3b94d4614795ac52a6d47aa9).

The change is otherwise bounded to the five expected presenter/direct-test files. `git diff --check` passes. I found no source factory, config guess, pair/clip-shape heuristic, threshold change, private crop/statistics deletion, normal activation, public type/schema change, or semantic-motion change.

## Blocking preservation finding

The candidate conflates the legacy compatibility-input rule with the existing public `diagnostics.mouth` capability result:

- `motion.ts:42-44` returns `null` when raw `clip.params.mouth` is absent.
- `scene.ts:17-31` turns that `null` into `diagnostics.mouth.status = "unknown"`.
- `presenter_scene_capability.mjs:212` and `test_presenter_crop_equivalence.py:80-82,160-162` now assert that loss.

That contradicts the corrected KNOWN-preserving proposal and the approved four-still owner grant. Exact supported counterexample: a valid registered `clip.params = {}` / `clip()` at frame 0, with no mosaic or unsupported outer geometry. `mouthAnchor({})` still normalizes the component's actual drawing to `{x:151,y:104,w:19}` (`motion.ts:28-29`), and the existing parent/current source publishes the known padded footprint `{x:894,y:606,width:138,height:48}` at 1920x1080 (799 pixels at 640x360). The candidate instead publishes UNKNOWN. This is not merely a private legacy crop skip; it is a public capability loss.

The same broader loss affects the exact raw-invalid input `{mouth:{x:"bad",y:null,w:900}}`: the component safely renders with normalized `{x:151,y:104,w:40}` and the candidate itself proves `motionAt` equals the explicit-width-40 case at `presenter_scene_capability.mjs:214-216`, but it publishes UNKNOWN at line 213. The prior approved behavior kept this normalized public region KNOWN. The candidate also makes clamped/fractional normalized cases UNKNOWN in `test_presenter_crop_equivalence.py:88-93`; do not accept those losses based on the 799/697 headline counts.

The partial raw input `{x:151,y:104}` correctly demonstrates the legacy compatibility footprint of 697 pixels / logical width 16, while the semantic drawing remains width 19. That distinction must remain explicit: a legacy compatibility inspection eligibility rule is not permission to narrow the component's existing semantic capability result. Preserve the public KNOWN normalized facts and keep any raw legacy skip/unqualified-equivalence rule separate, without adding a public type/schema field.

The test edits currently rewrite passing known behavior to refusal/unknown behavior rather than preserving it. Restore the original KNOWN assertions; no xfail/skip is appropriate.

## Evidence run

All runs used a private extraction of `ee71010a0`, Node `v20.19.4` at `/home/user/work/node-v20.19.4-linux-x64/bin/node`, the read-only public `0.0.12` artifact, and the read-only private peer graph `/home/user/work/runtimes/agent-remotion-0012/node_modules`. No shared dependency was modified.

```text
pytest -q -o addopts= -p no:cacheprovider --tb=short \
  tests/packs/rendering/test_presenter_scene_capability.py::test_presenter_existing_registered_ssr_markup \
  tests/packs/rendering/test_presenter_scene_capability.py::test_presenter_public_scene_contract \
  --basetemp=/tmp/agt-review-mouth-focused
6 passed in 26.31s

pytest -q -o addopts= -p no:cacheprovider --tb=short \
  tests/packs/rendering/test_presenter_scene_capability.py \
  tests/packs/rendering/test_presenter_crop_equivalence.py \
  --basetemp=/tmp/agt-review-mouth-targeted2
17 passed in 46.94s

pytest -q -o addopts= -p no:cacheprovider --tb=short \
  tests/packs/astrid_motion/test_astrid_motion_pack.py \
  tests/packs/rendering/test_remotion_element_generation.py \
  tests/packs/rendering/test_timeline_visualize_motion_views.py \
  --basetemp=/tmp/agt-review-mouth-targeted3
38 passed, 2 skipped in 30.20s
```

The two skips are the existing esbuild-dependent neighbor cases. Aggregate direct evidence is **55 passed, 2 skipped**; no full suite, browser, socket, physical PNG capture, normal consumer activation, or private crop/statistics deletion was run.

Read-only checks:

```text
git diff --check ee71010a^ ee71010a                  PASS
python scripts/artifact_manifest.py --check          EXIT 1 (expected stale manifest)
```

The manifest check names exactly these changed source entries as stale:

```text
astrid/packs/astrid_motion/rendering/elements/effects/am-presenter/element.yaml
astrid/packs/astrid_motion/rendering/elements/effects/am-presenter/motion.ts
astrid/packs/astrid_motion/rendering/elements/effects/am-presenter/scene.ts
```

## Required next steps

1. Restore KNOWN-preserving public capability semantics for default, partial-normalized, raw-invalid-normalized, fractional, and clamped inputs; keep the partial 697 legacy inspection fact separate from semantic capability.
2. Restore the passing known-behavior assertions and rerun the same focused/targeted lanes.
3. After the corrected source is admitted, run the normal owner artifact refresh from the Agent root: `python scripts/artifact_manifest.py`, then `python scripts/artifact_manifest.py --check`, and include the resulting `artifacts.json` update. Do not hand-edit or mutate shared generated source during this review.
4. Keep physical default/partial equivalence and any production consumer activation unclaimed until their separately granted central qualification passes.

