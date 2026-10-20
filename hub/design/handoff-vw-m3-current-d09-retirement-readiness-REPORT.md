# D09 retirement readiness — current Agent integration

## Verdict

No qualified deletion is ready. I made no repository changes and did not apply
the earlier broad D09 proposal. The current integration is Agent HEAD
`43d567f9d972386dc4cf585fbacc3ad9afc56bdd` and pins Composition `0.0.12`; this
audit used that current tree, not the frozen R4 branch.

The smallest honest candidate remains a later deletion of
`astrid/core/timeline/onscreen.py` (452 lines), but it is blocked by the
ordinary/cache label path, the SDK check/reflow callers, and the fact that the
public adapter still imports its role declarations. `motion/model.py` is not a
qualified deletion candidate: production lipsync still calls `mouth_state` and
`mouth_box`, and the public mouth ROI proof is presently test-only.

## Current production caller map

### `astrid/core/timeline/onscreen.py`

| Caller | Current use | Retirement consequence |
|---|---|---|
| `astrid/core/timeline/scene_answers.py:98-114` | `host_frames_at()` obtains `element_coverage()` and `role_of()` before calling the public Composition scene query. The adapter validates Root shape but explicitly says shape does not certify revision, candidate, assets, or theme. | Move only role/address declarations to a retained public seam, and keep source-bound capture separate. A public scene query alone does not replace this dependency. |
| `astrid/packs/rendering/actions/timeline_visualize/overlays/labels.py:53-66` | `labels_for()` calls private `visible_at()`; `addresses_at()` filters those rows at the 5% threshold. | This is the known label-geometry fallback. It remains needed for cache hits and non-capture paths. |
| `astrid/sdk/timeline/check.py:46-53,82-106` | Per-process cached element declarations, `_on_screen()` coverage spans, and `check()` diagnostics. `_sprite_problems()` also calls `layout_bounds()` at `:223-261`. Current `check()` makes scene findings advisory but still computes the private spans. | Need a verified public source for the exact post-resolve candidate plus preservation of picture/EMPTY/DIP/address and sprite diagnostics. No UNKNOWN/UNAVAILABLE substitution is acceptable. |
| `astrid/sdk/timeline/reflow.py:1015-1027` | `_doomed_cuts()` uses `role_of()` to decide whether picture/background clips survive a reflow. This is role semantics, not a render query. | Relocate role declarations without requiring renderer access or importing scene evaluation into reflow. |

The exact current test consumers include `tests/core/timeline/test_onscreen.py`,
`tests/core/timeline/test_onscreen_more.py`,
`tests/packs/rendering/test_labels_overlay.py`,
`tests/packs/rendering/test_timeline_visualize_labels.py`,
`tests/packs/rendering/test_capture_scene_labels.py`,
`tests/packs/rendering/test_scene_host.py`,
`tests/packs/rendering/test_scene_source_carry.py`, and
`tests/sdk/test_intent_app_astrid.py` (`_address`). The original on-screen
tests must remain until each distinct user-visible behavior has a named public
equivalent.

### `astrid/packs/rendering/actions/timeline_visualize/motion/model.py`

| Caller | Current use | Retirement consequence |
|---|---|---|
| `.../layers/builtin.py:387-390` | `render_lipsync()` calls `model.mouth_state()` for every presenter/frame and draws the mouth-state strip. | A public motion scalar/label path must feed the same per-frame result before deleting the private state mirror. |
| `.../motion/model.py:600-603` | `_presenter_props()` calls `mouth_state()` for the element-motion fallback props. | The element's own motion path and fallback behavior must remain covered. |
| `.../layers/builtin.py:426-432` | `render_lipsync()` calls `model.mouth_box(presenter, 0)` for the pixel-change crop. | A retained public component-zero ROI must be delivered into the existing `LayerContext`; the current public ROI helper is not a production caller replacement. |

The direct behavior tests are
`tests/packs/rendering/test_timeline_visualize_motion_views.py:297-307`
(`mouth_state` cycle),
`tests/packs/rendering/test_presenter_crop_equivalence.py` (legacy/current
crop controls and source-bound unknowns), and
`tests/packs/rendering/test_presenter_selected_cut_aggregate.py:159-266`
(selected cut, adjacency, denominator, and strict 2% controls). The latter's
module comment still states that production lipsync uses `mouth_box`; its
public adapter is explicitly test-only.

## What current public capture supports

The current tree contains the staged sequence, not a blanket source claim:

* `ae6c3ebc8` provides `scene_answers.host_frames_at()` and the public
  `prepareCompositionScene`/scene-query transport. Its current tests cover
  public transition boundaries, rational/half-open frames, painter order,
  opaque compiled IDs, unknown/unavailable answers, and public12 transition
  forwarding. The adapter's own docstring and tests preserve the limit that
  input shape is not source authority.
* `630c9d0a9` provides `CaptureSceneLabels`; it observes final serialized Root
  props and the exact sorted frame request, queries the public adapter once,
  and retains rows only after the complete fresh PNG batch succeeds.
* `de62afbbb` carries the retained revision/candidate/closure, projected clip
  IDs and address/occurrence mapping into `RemotionFrameProvider`. The current
  callback checks the frozen source bytes, resolved theme, serialized timeline,
  materialized asset digests, canonical canvas/fps basis, and staged element
  assets before the public query.
* Current `remotion/package.json` and lockfile pin the Agent consumer to the
  checked-in Composition `0.0.12` artifact. The recorded public12 direct lane
  was `79 passed`; neighboring rendering/filmstrip tests were `125 passed,
  3 deselected`, with targeted Ruff clean. That evidence used a private
  artifact overlay and synthetic PNG capture; it did not qualify host runtime
  admission, browser/render pixels, audio, or cross-product owner adoption.

These facts support fresh, source-bound capture labels for the composed-frame
path. They do not support deleting the private model from ordinary checks,
reflow, or fallback labels. They also do not authorize replacing the cache
fallback with refusal or UNKNOWN.

## Cache fallback that must stay

At `composed_frame.py:780-812`, cache hits copy PNGs directly and do not invoke
the scene callback. Scene rows are retained only for fresh frames after
`CaptureSceneLabels.retain()` succeeds. The two current consumers are:

* `filmstrip_cards.py:1684-1694`: `scene_for_frame()` absent ->
  `overlays.labels.addresses_at(config, frame, fps, canvas)`;
* `filmstrip_cards.py:1718-1724` -> `overlays.labels.overlay_labels_frame()`;
  when capture is absent, `labels.py:109-114` falls back to `labels_for()`,
  which calls private `onscreen.visible_at()`.

This is the 07:58 cache-fallback boundary. It must remain until a qualified
replacement covers cache cards and ordinary/non-capture labels with exact
source facts. Pixel-verification, statistics, and `_timing_evaluators.py` are
not deletion candidates.

## Exact blockers and minimum next proof

1. Agent owner must provide the existing verified source/capture join to the
   SDK check path for the exact post-resolve candidate, while retaining the
   renderer-free save path. It must preserve known GAP/EMPTY/DIP, cut/address
   wording, sprite OFFCANVAS/source diagnostics, and distinguish real UNKNOWN,
   UNAVAILABLE, and known empty answers.
2. The label path needs a current-tuple proof for fresh and cached cards,
   including selected projected IDs, occurrence identity, theme/assets, and
   frame membership. A callback test or metadata-only admission is not enough.
3. Mouth retirement needs the public component-zero ROI in the real
   `render_lipsync` caller, then positive and planted-mismatch selected-cut
   proofs against the current public12 consumer. Existing crop/statistics
   behavior remains until that production join exists.
4. Any landing gate must run the original on-screen/check/reflow/label tests
   alongside the named public query, source-carry, capture-label, and
   selected-cut tests on one exact Agent/Runtime/App/Composition tuple. The
   old proposal's historical PASS counts are not a current-tuple qualification.

## Potential delta, if and only if the proofs land

* `onscreen.py`: delete 452 lines; relocate only role/address declarations;
  replace the four production dependency sites above and retain all distinct
  public behavior tests. The earlier 18-file proposal was `+1060/-573` and
  product `+642/-562` (net `+80`), so it was not a net size cut by itself.
* `motion/model.py`: no count is proposed now. Do not delete its private
  mouth state/box or tests until the real lipsync caller consumes the public
  facts. The selected-cut public test delta is not production deletion proof.

## Verification run

From `/home/user/work/wt/vw-m3-current-d09-retirement-readiness`:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" \
  /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider -o addopts= \
  tests/core/timeline/test_onscreen.py \
  tests/core/timeline/test_onscreen_more.py \
  tests/packs/rendering/test_labels_overlay.py \
  tests/packs/rendering/test_timeline_visualize_labels.py \
  tests/packs/rendering/test_timeline_visualize_motion_views.py::test_mouth_state_matches_presenter_core_cycle
# 32 passed in 0.75s
```

No full suite, browser, socket, render, install, network, shared dependency
write, merge, checkout, commit, or push was run. Worktree remains clean.
