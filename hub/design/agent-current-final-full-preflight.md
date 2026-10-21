# Agent current final full preflight

Date: 2026-10-21

Verdict: **not ready for the later batched full**. I did not request a full suite, provision a child environment, or modify shared dependencies.

Current Agent source is commit `bc191ba1f61bfbf90ee23662c02acd3d75606f9`, tree `bfe5ab8a6cd488578b21d98ce375ed8a185264f4`.

## Changed batch

Against prior5a `5a625dd4c`, the current batch is:

```text
A astrid/sdk/_timeline_filmstrip_scene.py
M astrid/sdk/timeline/_recording.py
M astrid/sdk/timeline/inverse.py
M astrid/sdk/timeline_filmstrip.py
M docs/giant-file-rationale.md
A tests/editing_conformance/test_commit_runtime_parent_track_batch_inverse.py
M tests/editing_conformance/test_native_sheet_current_runtime.py
```

`git diff --check 5a625dd4c..HEAD` passed.

## Prerequisite failures

1. The current giant-file inventory is still stale for `remotion_runtime.py`.

Exact command:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider -o addopts= tests/test_structure_contracts.py::test_giant_file_inventory_matches_rationale
```

Result: failed. `astrid/core/rendering/remotion_runtime.py` is recorded as 1265 lines but is 1387 lines (`+122`, outside the allowed 50-line tolerance). The exact inventory scan found 36 large files, 36 rationale entries, no missing entries, no orphan entries, and no other out-of-tolerance entry.

2. The Viewing-owned Remotion helper source binding remains held and is not repaired here.

The exact handoff is `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m4-readiness-helper-source-binding-review-0416.md`. It records request-changes for candidate `d65c50d4...`: the extracted `_remotion_package.py` is executable validation authority, but `remotion_runtime._runtime_inputs()` currently binds `Path(__file__)` and the schema probe source, without binding the helper source. The current checkout still has no `_remotion_package.py`; its `_runtime_inputs()` path list at `astrid/core/rendering/remotion_runtime.py:385` likewise has no helper path. The required repair is owned by Viewing: include the helper in the existing file bindings and add the stale-helper negative test. I made no self-fix.

3. No existing installed Agent child is built from the final current source.

The existing source markers are:

```text
venv-agent-child-c13-5c5173dc: 5c5173dcb57669a9d43e5add2674543333f1c6d2
venv-agent-child-c13-a8a40afd: a8a40afd37e5560a14fa5e1a09ace6018596793e
venv-agent-child-s2:           d8749a9ce12a699672faf3ad96b4e4cbea9245c2
```

None matches `bc191ba1...`. The later full's Rendering/Composition tests consume the installed `banodoco_timeline_schema` through `ASTRID_TIMELINE_SCHEMA_PYTHONPATH`, and the full profile also needs a final-source identity. The closest existing profile, `full-c13-a8a40afd-integration`, is therefore deficient for final qualification because its child is tied to `a8a40afd...`. I did not provision a replacement. If the manager requires an installed child at final SHA, the exact consuming tests are the full suite's Rendering/Composition paths and the integration tests that use the isolated schema path; the existing profile does not provide that final-child guarantee.

## Source, artifact, and environment checks

- Agent artifact manifest: `scripts/artifact_manifest.py --check` passed (`artifacts.json is current`).
- `tests/test_vendor_lock.py tests/test_artifact_manifest.py`: `24 passed in 5.36s`.
- Current Agent Remotion package, lockfile, and `0.0.13` composition artifact byte-compare equal to both `/home/user/work/runtimes/agent-remotion-0013` and `/home/user/work/runtimes/agent-remotion-published14-091aa23e`.
- The Agent vendor lock intentionally pins Runtime producer `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3`; checking against the pinned producer checkout passed. Checking against current Runtime `/home/user/work/runtime` (`b92d3e7a05eec65c142294ef4873edd059e9b31`, tree `6abc2f117391de8e7e35c0283f575a002199894d`) fails with the expected producer-commit mismatch. This is an intentional source split, not a request to refresh the lock: execute the later full against current Runtime as directed.
- Import-origin checks with all three existing child profiles passed: `astrid` and `astrid_runtime_client` came from this current Agent worktree, `runtime_protocol` from current Runtime, and `banodoco_timeline_schema` from the selected child site-packages.
- Declared pack traversal found `115` paths and `missing=[]`. Required Runtime, schema, Remotion, Composition, and VibeComfy fixture paths exist.
- Disk check: `/dev/vda` has `14,415,160` KiB available (65% used), above the 5 GiB preflight floor.
- Shared worktrees `/home/user/work/agent`, `/home/user/work/runtime`, `/home/user/work/app`, and `/home/user/work/composition` had no file changes. Shared dependency paths resolved to themselves; no symlink mutation was found.

## Test-runner and targeted evidence

- `pytest --markers` exposes the expected `integration` and `live` markers.
- Changed integration tests collected successfully with the configured argv and paths: `17 tests collected`, exit 0. This was collect-only; they were not executed because they require a long-lived subprocess/second checkout and the task disallows live proof here.
- Non-integration SDK/conformance tests with `ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime`: `68 passed in 33.86s`.
- Pack resource and timeline admission tests: `10 passed in 12.40s`.
- No full, browser, render, live-socket, or real-provider suite was run or requested.

## Recommendation

Use the existing `full-c13-a8a40afd-integration` profile as the single later batched-full profile shape, after the prerequisites above are resolved: update the stale inventory, obtain Viewing's reviewed helper-binding source, and—if final installed-child identity is required—build a fresh child from Agent `bc191ba1...` without changing shared dependencies. Run it with current Runtime `/home/user/work/runtime`, the existing Remotion `agent-remotion-published14-091aa23e` fixture, and the declared VibeComfy fixture. Do not reuse the old child as final-SHA evidence.

