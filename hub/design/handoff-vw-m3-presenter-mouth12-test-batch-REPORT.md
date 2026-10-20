# ORCHREPORT — presenter mouth/series 0.0.12 test batch

## Result

Prepared one unapplied combined test delta from clean presenter `8a78c25ac`:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-presenter-mouth12-test-batch-combined.patch`

The worker worktree is based on `47a3be2a7` and contains the series helper,
its direct tests, the presenter 0.0.12 pin/test adaptation, explicit historical
theme selection, the navy `DEFAULT_THEME` assertion, and the retained selected-
cut original-PNG test proposal.

Changed paths are limited to `tests/` (including the retained PNG fixture).
No product source, root `package.json`/lock, runtime pin, artifact pin, or
repository documentation was changed. The selected-cut fixture remains
explicitly bounded to public10 retained evidence; its 0.0.12 query compares
timeline/assets and pins the inspection hash while preserving the historical
explicit theme. The presenter implementation is unchanged from the clean
source; no source-admission, activation, private-crop deletion, or Gate 6
claim is made.

## Overlay and evidence

The disposable ORCH overlay is:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-presenter-mouth12-test-batch-overlay`

It used the exact f29 Composition 0.0.12 artifact, SHA-256
`0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`, f29
package/lock/runtime metadata in the overlay, and the unchanged presenter
source from this worker.

Commands and results:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD \
ASTRID_NODE_EXECUTABLE=/tmp/vw-m3-agent-gate-node20.19.4/bin/node \
ASTRID_COMPOSITION_TEST_NODE_MODULES=/home/user/work/wt/vw-m3-scene-host-plumbing/remotion/node_modules \
/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --tb=short \
tests/packs/rendering/test_presenter_scene_capability.py \
tests/packs/rendering/test_presenter_crop_equivalence.py \
tests/packs/rendering/test_presenter_series_inspection.py \
tests/packs/rendering/test_presenter_selected_cut_aggregate.py
33 passed in 12.13s

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD \
/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --tb=short -m 'not integration' \
tests/packs/rendering/test_composition_package.py
5 passed, 1 deselected in 0.28s

/home/user/work/venv-agent/bin/python -m ruff check --no-cache --isolated --select E4,E7,E9,F,I,BLE \
tests/packs/rendering/test_presenter_scene_capability.py \
tests/packs/rendering/test_presenter_crop_equivalence.py \
tests/packs/rendering/test_presenter_series_inspection.py \
tests/packs/rendering/test_presenter_selected_cut_aggregate.py \
tests/packs/rendering/test_composition_package.py
All checks passed!

/tmp/vw-m3-agent-gate-node20.19.4/bin/node --check \
tests/packs/rendering/presenter_scene_capability.mjs
/tmp/vw-m3-agent-gate-node20.19.4/bin/node --check \
tests/packs/rendering/presenter_crop_geometry.mjs
/tmp/vw-m3-agent-gate-node20.19.4/bin/node --check \
tests/packs/rendering/presenter_series_inspection.mjs
/tmp/vw-m3-agent-gate-node20.19.4/bin/node --check \
tests/packs/rendering/presenter_selected_cut_query.mjs
all passed

git -C <clean-8a78-applycheck> apply --check --whitespace=error-all <combined.patch>
combined patch applies cleanly to 8a78c25ac

git diff --check
passed
```

The presenter lane retained all 286 historical SSR hashes. The selected-cut
lane exercised the original PNGs, one component-zero public ROI query, actual
cut selection, missing/duplicate/order controls, missing-image adjacency,
half-open windows, absent-file refusal, and strict 15/799 <= 2% < 16/799
controls. No browser, socket, full suite, install, network, or central test
request was run.

## Decision / limits

The selected-cut proposal is included because its owned fixture qualification
remains honest: the fixture README identifies the exact retained public10
source and the test does not present it as current Runtime custody or a
production source contract. The public12 adaptation keeps its explicit
historical theme instead of substituting the new navy default.

No blocker remains for review. The delta is intentionally not applied to any
integration worktree.
