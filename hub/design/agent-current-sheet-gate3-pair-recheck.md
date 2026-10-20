# Current sheet and Gate3 integration qualification

Date: 2026-10-20 21:55 UTC

## Result

PASS. The combined Agent integration source `81873ccf270e1c099c9f76b86103ccf3c9275cf4` was qualified with one narrowly scoped central run. No product or assertion changes were made.

The named allow-list suite added for this check was `agent current-sheet-gate3-integration`. It used the normal public013/C13 socket-capable environment:

- Agent snapshot tree: `5164f267bb08eafc497ae19e081861eabec9bb67` (the tree of Agent commit `81873ccf270e1c099c9f76b86103ccf3c9275cf4`)
- Runtime: `5c32832baeb3018fb50da53be3ef2921ac2bae29`
- App: `0fa436c7847a2cdb1c2b565dbf7749e1d3ca605b`
- Composition: `4f325f1e14f03a3418f04bd81b3635c810a40cf2`
- Public renderer runtime: `/home/user/work/runtimes/agent-remotion-0013`
- C13 Python environment: `/home/user/work/venv-agent-child-c13-a8a40afd`

Central run: `agt-m2-current-sheet-gate3-pair-recheck-current-sheet-gate3-integration-1020215346-19046`.

## Exact test command and results

```text
env -i HOME=/root LANG=C.UTF-8 PATH=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin:/nix/var/nix/profiles/default/bin:/root/.local/bin:/root/.cargo/bin:/usr/local/go/bin:/opt/node22/bin:/opt/maven/bin:/opt/gradle/bin:/opt/rbenv/bin:/root/.bun/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/bin ASTRID_REMOTION_PROJECT_DIR=/home/user/work/runtimes/agent-remotion-0013 ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node ASTRID_TIMELINE_SCHEMA_PYTHONPATH=/home/user/work/venv-agent-child-c13-a8a40afd/lib/python3.13/site-packages ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime ASTRID_TEST_NODE_MODULES=/home/user/work/runtimes/agent-remotion-0013/node_modules PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent-child-c13-a8a40afd/bin/python -m pytest -q -o addopts= -p no:cacheprovider -m integration tests/editing_conformance/test_native_sheet_current_runtime.py::test_http_cut_owned_native_sheet_hold_reloads_and_undoes tests/editing_conformance/test_commit_runtime_native_checkout.py::test_authenticated_v1_commit_reload_undo_survives_stopped_renderer_and_preview_reports_unavailable
```

- PASS — `test_http_cut_owned_native_sheet_hold_reloads_and_undoes`
- PASS — `test_authenticated_v1_commit_reload_undo_survives_stopped_renderer_and_preview_reports_unavailable`
- Central output: `2 passed in 30.70s`, exit 0

No old parent-label control, full suite, or full* suite was run.

## Source checks

- Cut ownership preservation remains in `astrid/sdk/timeline/_clip_scalar_commands.py:28` (`key == 'cut'` is excluded from source-hold timing propagation).
- Connected CLI route remains in `astrid/packs/timeline/cli.py:3603` (`parsed.native or parsed.client is not None`).
- WC2 obsolete authoring promotion removal is present: `ecfa19c52` is an ancestor and `promote_approved_authoring_candidate` is absent from the affected source and test files.
- Both new nodes are present at the expected test locations.
- Opaque/clear fixture is present at `tests/editing_scenarios/look/look.clear.plate-asset-opaque.yaml`, SHA-256 `942dadc716df290c8865101172ce61fa9f33869d938ade2da473e96d06de1aa4`.
- Worktree status was clean and `git diff --check` passed.

Not run: any broader conformance, parent-label control, full suite, browser, or other live journey.

