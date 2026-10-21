# vw-m3-d09-required-semantic-cut-1209

## Result

Migrated the omitted/default `am-presenter` mouth-state consumer in
`render_curves` to the already admitted public Scene motion rows. The selected
curve path now uses `diagnostics.motion.mouth` when the exact public rows are
fresh/cache-valid and source/basis/address/frame checks pass. The public-row
adapter's default strict mode remains unchanged for `render_lipsync`, so its
legacy ROI/crop contract is preserved.

Changed files:

- `astrid/packs/rendering/actions/timeline_visualize/layers/builtin.py:290`
  opts the curve caller into `allow_default_motion=True`; lines 381–459 keep
  the source-bound row validation and permit only an omitted `mouth` anchor to
  skip the legacy ROI gate.
- `tests/packs/rendering/test_presenter_selected_cut_aggregate.py:182` adds one
  direct regression: omitted mouth uses public curve states without calling
  private `mouth_state`, while the strict lipsync adapter still refuses the
  same default input.

The private fallback remains live for missing rows, mixed evidence, stale or
forged rows, UNKNOWN/unavailable evidence, partial anchors, malformed anchors,
and the `render_lipsync` pixel/crop path. `model.mouth_state`,
`_timing_evaluators`, PNG crops, pixel statistics, and selected-frame
denominators were not changed.

## Tests

Passed:

```text
PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q tests/packs/rendering/test_presenter_selected_cut_aggregate.py tests/packs/rendering/test_timeline_visualize_motion_views.py
31 passed, 2 skipped, 26 deselected in 10.82s

PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m ruff check astrid/packs/rendering/actions/timeline_visualize/layers/builtin.py tests/packs/rendering/test_presenter_selected_cut_aggregate.py
All checks passed!

python3 -m py_compile astrid/packs/rendering/actions/timeline_visualize/layers/builtin.py tests/packs/rendering/test_presenter_selected_cut_aggregate.py
git diff --check
```

The first pytest attempt without `/home/user/work/runtime` on `PYTHONPATH`
failed during collection with `ModuleNotFoundError: runtime_protocol`; the
successful command above uses the required shared Runtime package read-only.

## Compatibility and review status

The current Agent pin remains `@banodoco/timeline-composition` `0.0.13` in
`remotion/package.json` and `remotion/package-lock.json`; no pin or public API
change is included. The public motion source remains the existing
`am-presenter/motion.ts` → `presenter-core.ts` codebook and Scene diagnostic.

Live callers after the change are `render_curves` (public default-state path
when admitted, private fallback otherwise), `render_lipsync` (strict public
ROI path or private fallback), and `motion/model.py`'s ordinary
`_presenter_props` fallback. No blanket refusal or guessed UNKNOWN was added.

The scope was reviewed against the current D09 ledger and the latest 0816/0827
VW-D09a maps. No physical tuple, browser, socket, full suite, package install,
PNG/audio parity, or owner-film run was performed; those are not required for
this small interim source proof. Owner/independent review remains the next
integration step.
