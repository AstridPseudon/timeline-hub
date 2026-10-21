# Agent Main014 current-preserving forward

## Ancestry and merge parent

- Worker base: `6efc81500a0e0688c2bb41e736503f0fc3e04abb`, tree
  `2ed2b8a12b5b3391ca221ba6ff05390f71a73556`.
- Common merge base: `5c5173dcb57669a9d43e5add2674543333f1c6d2`, tree
  `8626f868a3869b23baaca9814adb930e8952e4c7`.
- Integration tip observed at worker start and again before finalization:
  `4467c1c1a9ed81fa7cd1b2d7687b8ada54dc216a`, tree
  `5997f0162374dcfb56597b636caaad597c951b68`; it did not advance.
- The harness merge-parent file contains the full integration SHA
  `4467c1c1a9ed81fa7cd1b2d7687b8ada54dc216a`. No git merge, checkout,
  rebase, or integration-branch mutation was performed.

## Resolved delta

Applied the integration-only scene/CLI/lifetime/registry repairs onto the
current-preserving worktree with `6efc81500` as the first parent. The resolved
worktree changes are limited to:

- extracted `scene_roles` metadata loading while retaining the `onscreen`
  compatibility patch points;
- neutral `prepared_scene_root` and `default_composition_id` renderer seams;
- Scene-only caller migration, native occurrence unsupported-map fallback,
  check/reflow role imports, and effect-registry typing;
- the corresponding scene-role, scene-lifetime, composition-registry, and
  existing CLI/scene tests.

The integration delta's `dispatch.py` additions were already present in the
current `6efc81500` tree, including final `ok`/`problem_code` handling, so
they were retained without a duplicate edit. The integration `artifacts.json`
was not copied: it was stale against the current source path set. Normal
`scripts/artifact_manifest.py` regeneration left the current 155-artifact
manifest current at version
`sha256:fe97bd9be011f3695a50dfc0017e2c0264c8cfa8a0b01b01e92abd3f927ec25e`.

No schema, raw/track/private15 source, runtime lock, generated Runtime client,
or unrelated current-main change was added or removed.

## Preservation checks

- `runtime.lock.json` remains byte-identical and hashes
  `920f4a3edf3d0e5ce9df5a0b2749f7b02bc2ea7db6fef2ec70db8d02b65be8e7`.
- `scripts/vendor_lock.py check runtime.lock.json --producer
  /home/user/work/wt/rt-pin-95bd3c5f` passed against Runtime
  `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`, tree
  `d3a290b407fa61e6ab2d476f50c068073f70df00`.
- `astrid/core/timeline/schema/edit-command.schema.json` remains exact hash
  `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`, with
  55 `$defs` and 29 `EditCommand.allOf` branches.
- No protected lock/schema/generated-client path appears in the worker diff.
- `python3 scripts/artifact_manifest.py --check` and `git diff --check` passed.

## Tests

Passed, with the approved read-only Runtime and Remotion profiles:

```text
ASTRID_REMOTION_PROJECT_DIR=/home/user/work/runtimes/agent-remotion-main95bd \
ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-95bd3c5f \
PYTHONDONTWRITEBYTECODE=1 \
PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-95bd3c5f" \
/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider \
  tests/core/timeline/test_scene_roles.py tests/core/timeline/test_onscreen.py \
  tests/core/timeline/test_onscreen_more.py tests/packs/rendering/test_scene_only_executor.py \
  tests/packs/timeline/test_cli_native.py tests/packs/timeline/test_cli_commit_move.py \
  tests/sdk/test_timeline_reflow_golden.py tests/sdk/test_timeline_reflow_keep.py \
  tests/packs/rendering/test_effect_registry_target.py tests/packs/test_composition_elements.py \
  tests/timeline/test_effects_catalog.py tests/core/gateway/test_doctor_bundle.py
# 102 passed in 39.04s
```

```text
... pytest tests/test_schema_contract.py
# 23 passed, 6 subtests passed in 10.63s
```

The public-boundary static portion was included in a broader run with 60
passes, but its four subprocess cases remain environment-unverified: that
test intentionally replaces `PYTHONPATH` with only the Agent root, so the
subprocess cannot import the Runtime checkout's `runtime_protocol`. No public
boundary or full/browser/live suite was rerun.

## Adoption hold

This is private staging only. The harness still needs to finalize the resolved
tree as a true two-parent commit with first parent `6efc81500` and merge parent
`4467c1c1a`; no public integration adoption, publication, activation, or
coordinated Runtime/App adoption is claimed here.
