# D09 label handoff commands

No central request, browser, socket, full suite, install, network, or fresh-PNG
run is authorized for this handoff. The source is already owner-integrated at
`d93b4ff6a99b0a421ecad47131467754deff3445`.

Run from:

```sh
cd /home/user/work/wt/vw-m3-labels-d93-owner-port-handoff
export PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD"
PY=/home/user/work/venv-agent/bin/python
```

Targeted non-native/metadata-safe neighbors:

```sh
$PY -B -m pytest -q -p no:cacheprovider -o addopts= \
  tests/packs/rendering/test_fast_lane.py \
  tests/packs/rendering/test_live_source_label_native.py \
  tests/packs/rendering/test_scene_source_carry.py -k 'not native' \
  tests/packs/rendering/test_timeline_filmstrip_cards.py \
  tests/packs/rendering/test_timeline_filmstrip_execution.py
# 118 passed, 37 deselected
```

Direct metadata assertions:

```sh
$PY -B -m pytest -q -p no:cacheprovider -o addopts= \
  'tests/packs/rendering/test_scene_source_carry.py::test_candidate_retains_real_compiled_candidate_and_uncertified_base_hint[transport]' \
  'tests/packs/rendering/test_scene_source_carry.py::test_metadata_only_historical_snapshots_remain_uncertified_with_revision_hint' \
  --disable-warnings
# 2 passed
```

Lint and whitespace:

```sh
$PY -B -m ruff check --no-cache --isolated \
  astrid/packs/rendering/actions/timeline_visualize/provenance.py \
  tests/packs/rendering/test_fast_lane.py \
  tests/packs/rendering/test_live_source_label_native.py \
  tests/packs/rendering/test_scene_source_carry.py \
  tests/packs/rendering/test_timeline_filmstrip_cards.py \
  tests/packs/rendering/test_timeline_filmstrip_execution.py
git diff --check 634867fed..HEAD
```

The prior central provenance positive is recorded as result
`1020142658-20591` (18 passed), alongside the recorded +127 metadata-control
checks. Reuse that result for the signed/admitted
positive; do not relabel it as fresh PNG certification. The native fixture is
not locally reproducible without the missing shared Remotion peer root, and no
dependency install or shared-node_modules mutation is allowed.

