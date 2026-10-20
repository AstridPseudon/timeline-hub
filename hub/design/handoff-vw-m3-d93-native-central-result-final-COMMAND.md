# D09 terminal evidence commands

The following commands were executed before this terminal handoff; do not
rerun the central lane.

```sh
/home/user/work/venv-agent/bin/python -B \
  /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-d93-central-env-runtime-fix/run-integration-clean.py \
  --preflight
# PASS; exact origins copied to *-preflight.json

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" \
  /home/user/work/venv-agent/bin/python -B -m pytest -q -p no:cacheprovider -o addopts= \
  tests/packs/rendering/test_scene_source_carry.py::test_candidate_retains_real_compiled_candidate_and_uncertified_base_hint[transport] \
  tests/packs/rendering/test_scene_source_carry.py::test_metadata_only_historical_snapshots_remain_uncertified_with_revision_hint \
  tests/packs/rendering/test_scene_source_carry.py::test_execute_handoff_uses_actual_provider_and_public_labels_in_exported_pack[transport]
# 3 passed in 3.57s

R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test \
  vw-m3-d93-central-env-runtime-fix integration-viewing-live-source-label-native-clean)
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
# 1020160329-27058: 18 passed in 95.40s
```

Read-only final checks recorded: `git merge-base --is-ancestor d93b4ff6a
tl/integration` exit 1; current Agent worktree clean; shared f816 worktree
clean; public12 archive SHA256
`0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`.
