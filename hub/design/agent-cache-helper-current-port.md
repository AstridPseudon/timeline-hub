# Agent cache-helper current port

## Result

Ported the two requested units onto current Agent `4095a349`:

- `dfa2fbb28`: extracted the existing `attach_frame_addresses` and
  `_contact_overlay_for_layers` implementations into private
  `astrid/packs/rendering/actions/timeline_visualize/_filmstrip_cache.py`,
  retained the old public imports through `filmstrip_cards.py`, and declared
  the helper in the existing `timeline_visualize` pack resource closure.
- `929bed011`: applied only the native fixture environment resolution change
  in `tests/packs/rendering/test_capture_scene_labels.py`.

No cache key, source identity, PNG hash, fresh-only row minting, fallback,
default-off, rendering, public graph, API, DTO, or policy behavior changed.

## Counts and preservation

- `filmstrip_cards.py`: 1,968 lines before (`f711cbd2`) -> 1,917 after.
- New `_filmstrip_cache.py`: 63 lines.
- Diff against `f711cbd2`: helper +63; cards +9/-60; pack resource +2; native
  fixture +9/-5. No other files changed.
- Exact file comparisons against source units passed for the extracted helper,
  cards source, `pack.yaml`, and native fixture.
- AST dumps for both moved functions match their original definitions.
- Public compatibility import smoke passed: both functions resolve to the
  extracted helper objects.

## Tests

- `ruff check --select I,F401 astrid/packs/rendering/actions/timeline_visualize/filmstrip_cards.py astrid/packs/rendering/actions/timeline_visualize/_filmstrip_cache.py` — PASS.
- `pytest ... tests/reshape/test_compare_baselines.py::test_the_tree_has_exactly_the_baselined_structure_violations` — **1 passed**.
- Cache/card/source neighbors, excluding native: `test_scene_cache_payload.py test_timeline_visualize_labels.py test_labels_overlay.py test_timeline_filmstrip_cards.py test_scene_source_carry.py -k 'not native'` — **133 passed, 19 deselected in 15.03s**.
- Pack resource closure/discoverability: first-party pack validation plus
  `tests/core/rendering/test_package_data.py` — **3 passed in 8.83s**.
- Exact affected native selection (`test_scene_source_carry.py -k native`) on
  public13 immutable graph `/home/user/work/runtimes/agent-remotion-0013`,
  Node `v20.19.4` — **19 passed, 40 deselected in 17.31s**.
- Additional direct neighbor check `test_capture_scene_labels.py` on the same
  graph — **20 passed in 10.33s**.

No full suite, browser journey, live socket suite, or renderer-wide run was
requested or performed. Shared dependency graphs were read-only.

## Decisions / blockers

No new decisions were required. The current source retains the existing
`f711cbd2` D10 and other current integration content; only the bounded helper,
pack resource declaration, and the requested native fixture setup were ported.
No blockers.

Recommended next step: owner merges this qualified unit, then the orchestrator
runs the single current full suite after the batch.
