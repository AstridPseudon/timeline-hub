# VW-D09a — one default fallback map: presenter mouth state

## Result

Chosen fallback: `astrid/packs/rendering/actions/timeline_visualize/motion/model.py:451-463`, `mouth_state`.

No product patch is proposed. The existing public13 Scene source is semantically equivalent for the bounded **normal** presenter input, but it is not an equivalent replacement for the live fallback boundary as a whole. The remaining independent caller has no source-bound public-row input.

## Exact normal contract

The source pair is:

- Private caller: `layers/builtin.py:472-473` (`render_lipsync`) uses `model.mouth_state` only when the source-bound public facts do not qualify. The independent curve caller is `motion/model.py:600-603` (`_presenter_props`), reached through `props_at:627-636` and sampled by `layers/builtin.py:285-289` (`render_curves`).
- Public source: `astrid/packs/astrid_motion/rendering/elements/effects/am-presenter/motion.ts:95-117,132-141`, backed by `presenter-core.ts:72-103`; `scene.ts:24-26` publishes the result as `layer.diagnostics.motion.mouth`.
- Normal input: admitted `am-presenter`, exact retained compiled clip/source, valid finite word spans with `end > start`, an in-range integral seed, and an exact clip-local frame. Under this bounded contract, both paths use the same sorted word schedule, `Math.round(seconds * fps)` frame edges, three-state cycle (`closed=0`, `half=.5`, `open=1`), `hashUnit(seed, wordIndex)` offset, and `0.12s` short-gap hold.
- Output mapping: public numeric `mouth` `{0,.5,1}` maps to private `{closed,half,open}`. `props_at` returns the numeric form plus the existing zoom/visible fields; `render_lipsync` consumes the string form for its unchanged state strip.

Clock/binding requirements are part of the equivalence: query the retained prepared Root through `scene_answers._prepared_host_frames_at`/`host_frames_at`, use the public row for the exact compiled clip ID and source-derived address, and use the row's actual content/own frame rather than a guessed timeline frame under speed/remap. The existing public clock controls cover 30 and rational 24000/1001 fps, speed `.5/1/2`, preroll, and half-open end boundaries.

## Refusal and UNKNOWN contract

- Missing, mixed, stale, or forged source-bound rows are a miss; `_public_mouth_facts` returns `None` and the caller retains `model.mouth_state`.
- Default/partial/raw-invalid `params.mouth` remain unqualified because the current adapter deliberately couples state rows to the legacy crop/ROI contract. Their public normalized motion may still be known, but it must not authorize the legacy crop or pixel statistic.
- Public Scene `coverage == UNKNOWN` or missing media does not mean `mouth == closed`: presenter motion diagnostics may remain numerically known while presence/coverage is unknown. Conversely, an absent/invalid `diagnostics.motion.mouth`, missing layer, wrong clip/address/basis, unknown owner, unavailable Scene, or stale/forged cache is not converted to a state; it refuses/unqualifies and keeps the private fallback.
- Pixel crops, strict `>2%` comparison, selected-frame denominator, and all PNG statistics remain untouched.

## Existing evidence

Positive controls already present:

- `tests/packs/rendering/test_timeline_visualize_motion_views.py::test_mouth_state_matches_presenter_core_cycle` — private codebook/hash control; targeted rerun here passed.
- `tests/packs/rendering/presenter_scene_capability.mjs`, `states` mode — public codebook, rational-fps word edges, short-gap hold and all three states.
- The same file's `clock` mode — content/own-frame mapping, speed/remap, preroll and half-open boundary.
- The same file's `registration` mode — normal owner dispatch and diagnostics equality.
- `tests/packs/rendering/test_presenter_selected_cut_aggregate.py::test_single_mode_public_mouth_facts_drive_existing_consumer` — existing normal public-first selected caller; the prior qualified lane reports 40 selected/crop/capability controls and 97 source/cache controls passing.

Negative/preservation controls already present:

- `presenter_scene_capability.mjs`, `unknowns` and `registration` modes — missing media/unknown coverage, mosaic/outer unknown diagnostics, and unknown owner refusal.
- `test_presenter_selected_cut_aggregate.py` — mixed public evidence, default/partial raw mouth, stale clip, forged ROI, and missing-row fallback.
- `test_scene_source_carry.py` — source, basis, retained-input, and incomplete-answer refusals.
- `test_scene_cache_payload.py` — stale/forged/other-frame cache misses and no mint on failed batches.
- `test_scene_only_executor.py` — unavailable, stale/incomplete, malformed compiled input, and missing-source advisory-unavailable behavior.

## Why no caller migration is proposed

Public13 and the exact retained source already support the normal `render_lipsync` selected path, which is the already-landed caller migration. They do not support `render_curves`/`_presenter_props`: that path receives only an `Element` and frame, not a source-bound public Scene row or the prepared Root lifetime. Adding a new carrier, query/API, source factory, or geometry/state split would exceed this bounded task.

The precise containing dependency is therefore `motion/model.py:_presenter_props` through `props_at`, with the direct `render_lipsync` fallback still required for the refusal cases above. The cut can qualify only after one source-bound normal presenter curve test compares `props_at(...)['mouth']` against the public `diagnostics.motion.mouth` at the same clip-local frame, and retains missing/mixed/stale/forged/UNKNOWN refusal assertions. No such curve-consumer join exists in the current tree; this is a qualification requirement, not evidence of a passing cut.

## Limits

The Python mirror has broader coercive behavior than the TS source for malformed/fractional inputs (for example Python `round`/seed handling versus JS `Math.round`/`Math.trunc`). Those are outside the normal equivalence and remain private fallback behavior. No physical run, renderer/helper launch, browser/socket, central, full suite, install, public pin, deletion, or test weakening was performed.
