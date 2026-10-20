# D09 / VW-LABEL final gate commands

All commands were read-only against the Agent repository or used a disposable private `/tmp` extraction. No shared dependency, node_modules, runtime, venv, cache, browser, socket, render, install, or network mutation was performed.

## Source and scope checks

```sh
AG=/home/user/peteromallet/astrid-agent
git -C "$AG" show -s --format='target=%H parent=%P tree=%T subject=%s' \
  815714e8bdb75a8ce1bb422c18466bcb3edb7fc2
# target=815714e8bdb75a8ce1bb422c18466bcb3edb7fc2
# parent=634867fed71b4ae53acaa3c3162315527c2bdb23
# tree=1e6fc112e17e8b811e7aaf206a556ebfa63551f3

git -C "$AG" show -s --format='current-integration=%H parent=%P tree=%T subject=%s' tl/integration
# current-integration=04c24768cbfa758d1a2c41c107140a051cda8773

git -C "$AG" diff --name-only \
  634867fed71b4ae53acaa3c3162315527c2bdb23 \
  815714e8bdb75a8ce1bb422c18466bcb3edb7fc2
# provenance.py
# test_fast_lane.py
# test_live_source_label_native.py
# test_timeline_filmstrip_cards.py
# test_timeline_filmstrip_execution.py
```

The target helper's `source` path imports the existing `astrid.core.rendering.verified_source.VerifiedTimelineSource` lazily, checks exact encoded snapshot equality, and returns committed/candidate only for a host-minted revision/working-copy ref. The metadata-only path is explicitly uncertified.

## Narrow controls replayed on exact target

Private target extraction, no cache/bytecode:

```sh
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -B -m pytest -q \
  -p no:cacheprovider -o addopts= tests/packs/rendering/test_fast_lane.py
# 13 passed in 0.18s
```

Preserved metadata expectations:

```sh
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -B -m pytest -q \
  -p no:cacheprovider -o addopts= \
  tests/packs/rendering/test_scene_source_carry.py::test_candidate_retains_real_compiled_candidate_and_base_label \
  tests/packs/rendering/test_scene_source_carry.py::test_historical_capture_and_managed_labels_name_their_consumed_revision
# 2 failed, 1 error
# transport candidate failed: old candidate label vs new UNCERTIFIED candidate label
# historical failed: old committed label vs new UNCERTIFIED preview label
# native parameter errored only because the private extracted environment lacked
# provisioned React/Remotion Node peers; no product conclusion is drawn from it.
```

## Adjacent worker evidence (not rerun here)

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -B -m pytest -q -p no:cacheprovider -o addopts= \
  tests/packs/rendering/test_fast_lane.py \
  tests/packs/rendering/test_timeline_filmstrip_cards.py \
  tests/packs/rendering/test_timeline_filmstrip_execution.py \
  tests/packs/rendering/test_timeline_offline_inspection.py \
  tests/sdk/test_timeline_commit_provider.py::test_move_reload_and_inverse_import_no_renderer \
  tests/sdk/test_timeline_capture_projection.py::test_capture_method_imports_and_runs_without_renderer_or_runtime \
  tests/editing_conformance/test_recipe_scalar_commands.py::test_scalar_capture_and_save_import_no_renderer_or_runtime \
  tests/editing_conformance/test_recipe_shot_set.py::test_shot_set_capture_and_save_import_no_renderer_or_runtime
# 100 passed in 17.38s

R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test \
  vw-m3-live-source-label-native-join integration-viewing-live-source-label-native --no-cache) && \
  /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
# 18 passed in 96.60s; tree 1e6fc112e17e8b811e7aaf206a556ebfa63551f3
```
