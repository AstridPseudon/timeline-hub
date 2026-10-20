## Report: agt-public10-adoption

The source is composed and the targeted tests pass, but the task is not complete. I wrote `BLOCKED` instead of `DONE`, for the three gaps listed below.

**What I did**
- I applied Bundle1 (`tl/agt-m2-bundle1-pin` at `3bf9e536`, based on `fc324e83`) onto `4a75f68f`. The patch applied cleanly across 17 files and includes the Runtime 0.2.2 lock. The pin is Runtime `6be97063`, client 0.2.2, schema `89a396`, artifact `3b805d`. This matches `design/m2-writer-bundle-1.md`, which names nothing newer.
- I pinned Composition 0.0.10 in the same places as the 0.0.8 adoption (`cbd91c3b`):
  - the new tarball under `remotion/artifacts/`;
  - `remotion/package.json` and `remotion/package-lock.json`, with integrity `sha512-SmJAoem9…Ycg==`;
  - `_COMPOSITION_PACKAGE_VERSION` in `astrid/core/rendering/remotion_runtime.py`;
  - the pin tests.
- The tarball's sha256 is `cd83b77f…ddea7`, as specified. No `0.0.8` reference remains outside the old tarball.
- I wrote `design/m2-public10-adoption.md` and the commit message at `workers/agt-public10-adoption/commit-msg`.

**Tests** (all run with `/home/user/work/venv-agent/bin/python`)
- **Pin, editing_conformance and neighbours:** `580 passed, 4 skipped, 33 deselected`. This ran `-m pytest -q -p no:warnings` over `test_composition_package.py`, `test_render_export_task_adapter.py`, `test_clip_fields.py`, `test_journey_plumbing.py`, `test_remotion_locking.py` and `tests/editing_conformance`.
- **Rendering pack plus native/label tests:** `1061 passed, 10 skipped, 33 deselected, 1 failed`.
  - The failure is `test_remotion_render_contract.py::TextCardVisibleMarkupTest::test_text_card_renders_visible_markup`: "SSR contract must resolve the Node version pinned by remotion/package.json". It is an environment failure, since no pinned Node was on PATH.
  - I did not rerun it with Node, because that command was rejected. The central suite `consumer-regressions-integration` lists this node with the Node 20.19.4 environment.
- **Import fence:** `scripts.reshape.import_cycles` reports no new cycles.

**Blocked or unverified**
1. **Exact-pair Runtime integration:** the `bundle1-runtime6be9706-integration` suite fails in 1s. It needs `/home/user/work/wt/rt-m2-track-public-export`, which no longer exists. Runtime's `tl/integration` is 11 commits past `6be97063`, so I did not substitute it. `vendor_lock.py check` fails for the same reason. It needs a Runtime checkout at exactly `6be97063`, or a suite pointed at one.
2. **Remotion gate:** I did not run `scripts/reshape/remotion_gate.py`, which needs `npm ci` and Node. `/home/user/work/runtimes/agent-remotion` would also need reinstalling with the 0.0.10 tarball before `consumer-regressions-integration` or `remotion-env-nodes` can run.
3. **Old tarball:** `remotion/artifacts/banodoco-timeline-composition-0.0.8.tgz` is still in the tree, unreferenced, because `rm` was denied. Whoever adopts this should `git rm` it.

I never requested a full suite. The scratchpad holds a stray `rt.tar` and an empty `rt/` directory from the abandoned Runtime extract; nothing stray is in the worktree.

**Next steps:** restore a Runtime checkout at `6be97063` and run the Bundle1 pair suite. Run the gate and Node-env suites with `/home/user/work/runtimes/agent-remotion` rebuilt on 0.0.10. Remove the 0.0.8 tarball.
