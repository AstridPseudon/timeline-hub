# vw-m3-d09a-final-semantic-retirement-1250

## Result

Implemented the bounded D09a semantic consumer cut on Agent branch
`tl/vw-m3-d09a-final-semantic-retirement-1250`.

- Composed only the approved cumulative producer line `c9ac7c7b0..ef7f39af3`
  (query-only-fix1242), without merge/rebase/checkout. The six producer files
  are byte-for-byte equal to `ef7f39af3`.
- Motion views now request the exact padded motion frame clock through the
  existing prepared Root callback while retaining only sparse pixel frames.
  No new renderer, provider, public field, package, pin, or store was added.
- `render_lipsync` now explicitly consumes the complete admitted
  `diagnostics.motion.mouth` state map for the normal public-positive path.
  The existing `model.mouth_state` fallback remains for missing/mixed/stale/
  forged/invalid or otherwise refused public facts. Pixel crop, `mouth_box`,
  statistics, threshold, and qualified public crop behavior are unchanged.

## Tests and checks

- `PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q tests/packs/rendering/test_presenter_selected_cut_aggregate.py tests/packs/rendering/test_timeline_visualize_motion_views.py`
  — **31 passed, 2 skipped, 28 deselected** in 10.72s.
- `PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q tests/packs/rendering/test_scene_source_carry.py -k transport`
  — **21 passed, 40 deselected** in 5.22s.
- `PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q tests/packs/rendering/test_scene_source_carry.py::test_motion_scene_rows_join_exact_missing_frames_once[transport]`
  — **1 passed** in 3.20s.
- AST parse of all seven changed Python files — **passed**.
- `git diff --check` — **passed**.
- Producer equality check against `ef7f39af3` for its six approved files —
  **passed**.

The combined source-carry invocation reached **72 passed, 2 skipped, 28
deselected, 20 errors**. Every error was native Remotion fixture setup failing
because the shared environment lacks the provisioned `react` peer under the
temporary test host. No install or shared-dependency mutation was attempted.

Ruff was run on all seven changed files but is not a clean signal for this
tree: it reports pre-existing issues in `filmstrip_cards.py` and
`renderers/remotion/run.py` (E731, import ordering, unused imports, and an
existing undefined `render` export). No unrelated lint cleanup was made.

## Decisions and remaining capability

The public state is admitted only after exact source identity/address, basis,
frame, layer identity, and closed/half/open scalar validation. Default,
partial, null, and raw-invalid mouth inputs retain the existing refusal and
private fallback behavior; no `UNKNOWN` state was guessed. The private helper
was not deleted because the exact remaining fallback is still live at
`layers/builtin.py:498`, and the standalone no-public-override path remains at
`motion/model.py:603` through `props_at`. The model/hash/timing codebook is
therefore retained for those refusal paths and tests.

## Recommended next step

Run the native source-carry lane in the central test service with its
provisioned Remotion peer graph. A later D09a deletion may remove
`mouth_state` only after those remaining refusal/standalone callers have an
independent source-bound replacement and their original fallback behavior is
no longer required.
