# Agent full5664 repaired six-node current check

Date: 2026-10-21 UTC

## Scope and source

This was one bounded changed-tree verification of exactly the six nodes that
failed in the classified `full-c13-5c5173dc-integration` run. No full suite,
neighbor, matrix, browser, live replay, Gate 1/3 repeat, source change, test
change, allowlist change, threshold change, or xfail was made.

The tested Agent snapshot was commit
`4467c1c1a9ed81fa7cd1b2d7687b8ada54dc216a`, tree
`5997f0162374dcfb56597b636caaad597c951b68`. This is the current worker
snapshot containing the five repaired changes. During/after this check the
mutable Agent integration tip advanced to commit
`88c9aac5042fa2caaa6278526a22e49da3593cd7`, tree
`91c279f86c1166eb04de11acdab881c8fc5a63f0`; the result below does not claim
qualification of that later tip.

The supported environment was the preflight tuple:

- Node `v20.19.4` at `/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node`;
- Remotion project `/home/user/work/runtimes/agent-remotion-0013`;
- installed child profile `/home/user/work/venv-agent-child-c13-5c5173dc`;
- immutable Runtime commit `9d1c43c647301da48a6e86ad82e466b501bd2418`, tree
  `50e74e3243c5da4cf77b6e6cc76605fae8aeb649`, at
  `/home/user/work/wt/rt-pin-9d1c43c6`.

## Exact central run

Named suite: `current-full5664-six-node-integration` (one light targeted run).

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test agt-m4-full5664-six-node-current-check current-full5664-six-node-integration --files "tests/core/rendering/test_production_callers.py::test_no_production_backend_imports_outside_allowlist tests/packs/test_composition_elements.py::CompositionElementTest::test_bundled_element_registries_generate_together tests/packs/timeline/test_cli_commit_move.py::test_ordinary_edit_occurrence_move_keeps_legacy_owner_resolution tests/test_artifact_manifest.py::test_committed_artifact_manifest_is_current tests/test_structure_contracts.py::test_giant_file_inventory_matches_rationale tests/timeline/test_timeline_kernel_kinds.py::DoctorV10ChecksTest::test_public_doctor_route_fails_closed_without_runtime"
```

The central service executed the preflight command with those six node IDs:

```text
env -i HOME=/root LANG=C.UTF-8 PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-9d1c43c6" PATH=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin:/nix/var/nix/profiles/default/bin:/root/.local/bin:/root/.cargo/bin:/usr/local/go/bin:/opt/node22/bin:/opt/maven/bin:/opt/gradle/bin:/opt/rbenv/bin:/root/.bun/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/bin ASTRID_REMOTION_PROJECT_DIR=/home/user/work/runtimes/agent-remotion-0013 ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node ASTRID_TIMELINE_SCHEMA_PYTHONPATH=/home/user/work/venv-agent-child-c13-5c5173dc/lib/python3.13/site-packages ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-9d1c43c6 ASTRID_TEST_NODE_MODULES=/home/user/work/runtimes/agent-remotion-0013/node_modules ASTRID_VIBECOMFY_CHECKOUT=/home/user/work/fixtures/vibecomfy PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent-child-c13-5c5173dc/bin/python -m pytest -q -o addopts= -p no:cacheprovider <the six node IDs above>
```

Result: **5 passed, 1 failed in 9.20s; exit 1.** Central result directory:
`orch/tests/agt-m4-full5664-six-node-current-check-current-full5664-six-node-integration-1021021033-8340/`.

## Exact result

Passed:

1. `tests/core/rendering/test_production_callers.py::test_no_production_backend_imports_outside_allowlist`
2. `tests/packs/test_composition_elements.py::CompositionElementTest::test_bundled_element_registries_generate_together`
3. `tests/packs/timeline/test_cli_commit_move.py::test_ordinary_edit_occurrence_move_keeps_legacy_owner_resolution`
4. `tests/test_artifact_manifest.py::test_committed_artifact_manifest_is_current`
5. `tests/timeline/test_timeline_kernel_kinds.py::DoctorV10ChecksTest::test_public_doctor_route_fails_closed_without_runtime`

Remaining failure:

- `tests/test_structure_contracts.py::test_giant_file_inventory_matches_rationale`
- Cause: `astrid/packs/rendering/actions/timeline_visualize/filmstrip_execution.py`
  is 2,072 lines while `docs/giant-file-rationale.md` records 2,015. The
  57-line difference exceeds the test's 50-line tolerance. This is the known
  Viewing-dependent inventory/rationale drift; it remains RED honestly.

## Next step

After the final Agent source tip is settled, refresh the giant-file rationale
entry as an owned documentation update and rerun only this exact remaining
node. Do not transfer this result to the later `88c9aac...` tip without a new
explicit check.
