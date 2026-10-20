# D09 fresh mouth context carry

## Result

Migrated the owned visualize/filmstrip fresh path to carry retained public
presenter facts into the existing private `LayerContext` through `shared`.
`CaptureSceneLabels._frame_facts()` exposes only facts already source-checked
against the exact prepared Root props and retained after all fresh PNGs exist.
The context adapter reads only fresh frames from the provider; cache-only,
mixed, missing, stale, or malformed facts leave the legacy private path active.

`render_lipsync` now uses the actual public row's component-owned compatibility
mouth footprint and declared canvas-to-PNG scale adapter when the entire
selected series qualifies. Public motion mouth levels are used for sampled
natural state rows; unsupplied frames still use the existing model fallback.
The private `mouth_box`, comparator, selected-frame denominator, missing-image
adjacency behavior, and all unsupported/legacy fallback behavior remain.

The selected-cut direct test now runs the registered Node/public query fixture
for a positive fresh handoff and planted stale-clip, forged-ROI, and missing-row
negative controls. The public query fixture returns the exact existing rows;
no fake public diagnostics are used for the positive case.

## Verification

- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m py_compile ...`: PASS.
- `git diff --check`: PASS.
- Pure targeted lane:
  `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --tb=short tests/packs/rendering/test_timeline_visualize_motion_views.py tests/packs/rendering/test_timeline_visualize_labels.py -k 'not integration'`
  -> **40 passed, 2 skipped**.
- Central targeted lane on the broader neighbours -> **71 passed, 2 skipped,
  19 errors**. Errors are pre-existing environment setup failures for missing
  Node 20/shared Remotion peers in `test_scene_source_carry.py`.
- Central dedicated public-query attempt -> blocked before test execution:
  its configured artifact path
  `/home/user/work/wt/vw-m3-mouth-public-query-real-lane/remotion/artifacts/banodoco-timeline-composition-0.0.12.tgz`
  does not exist.
- No full suite, browser, render, local server, socket, install, or network
  run was performed.

## Decisions and limits

- Kept the private fallback because cached or partially fresh series do not
  have the required retained public rows.
- Did not delete `mouth_box` or alter SDK/check/save/core-provider/timing code.
- Did not normalize default/partial/raw-invalid compatibility denominators or
  change the strict `>2%` comparator.
- Artifact/Node qualification of the new registered-host test remains
  unverified in this worker because the central lane's artifact path is absent.

