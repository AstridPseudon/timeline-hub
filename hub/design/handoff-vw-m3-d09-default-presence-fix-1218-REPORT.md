# vw-m3-d09-default-presence-fix-1218

## Result

Fixed the D09a default-input regression on top of
`tl/vw-m3-d09-required-semantic-cut-1209`.

- `_public_mouth_facts(..., allow_default_motion=True)` now distinguishes a
  missing `mouth` key from a present invalid value. Only omission admits public
  motion rows; explicit `None`, partial mappings, and malformed/raw-invalid
  mappings return `None` and keep the private fallback.
- The default-motion regression now queries public rows from the actually
  mutated case through the registered Composition host. Its provider asserts
  exact current props, basis, and requested frames before publishing rows, so
  retained pre-mutation rows cannot satisfy the test.
- The strict `render_lipsync` ROI path, `closed` 0.0 mapping, pixel threshold,
  selected-frame denominator, and mixed/partial/stale/forged/UNKNOWN fallback
  behavior are unchanged.

Changed files:

- `astrid/packs/rendering/actions/timeline_visualize/layers/builtin.py`
- `tests/packs/rendering/test_presenter_selected_cut_aggregate.py`

## Tests

Passed:

```text
PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q tests/packs/rendering/test_presenter_selected_cut_aggregate.py tests/packs/rendering/test_timeline_visualize_motion_views.py
31 passed, 2 skipped, 28 deselected in 10.72s

ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node ASTRID_COMPOSITION_TEST_NODE_MODULES=/home/user/work/runtimes/agent-remotion-viewing13-d0a5072b/node_modules ASTRID_REMOTION_PROJECT_DIR=/home/user/work/runtimes/agent-remotion-viewing13-d0a5072b PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q -m integration tests/packs/rendering/test_presenter_selected_cut_aggregate.py -k 'default_presenter_curve or explicit_invalid_presenter_mouth'
3 passed, 25 deselected in 5.27s

ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node ASTRID_COMPOSITION_TEST_NODE_MODULES=/home/user/work/runtimes/agent-remotion-viewing13-d0a5072b/node_modules ASTRID_REMOTION_PROJECT_DIR=/home/user/work/runtimes/agent-remotion-viewing13-d0a5072b PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q -m integration tests/packs/rendering/test_presenter_selected_cut_aggregate.py tests/packs/rendering/test_timeline_visualize_motion_views.py
28 passed, 33 deselected in 6.45s

PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m ruff check astrid/packs/rendering/actions/timeline_visualize/layers/builtin.py tests/packs/rendering/test_presenter_selected_cut_aggregate.py
All checks passed!

PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m py_compile astrid/packs/rendering/actions/timeline_visualize/layers/builtin.py tests/packs/rendering/test_presenter_selected_cut_aggregate.py
git diff --check
```

The two skips are the existing motion-view markers for unavailable element
maths when Node 20.19.4 is not on PATH; no new skip was added. The first
integration attempt hit the same environment issue and was rerun with the
provisioned Node 20.19.4 binary and read-only shared runtime modules.

No full suite, browser, socket, physical, package, pin, API, or owner-film
run was requested or performed.

## Decisions and follow-up

The settled plan and D09a review brief were followed. The named
`handoff-vw-m3-d09-default-motion-review-1212-REPORT.md` was not present in the
shared scratchpad; the manager brief and required semantic-cut report were
used as the available handoff evidence. Independent changed-hunk review is
still the next step.
