# D118 terminal metadata correction

Status: corrected by bounded read-only accounting; no new run and no source retagging.

For service `agent-agent-core-full-1025102421-30693`, `service-30693.summary` and `service-30693.snap` name Agent tree `f43dd198e915c3319983d406773f3d6683833d28` at `/home/user/work/agent`. That tree is the ambient service-worktree snapshot (commit `0277f46d5578a8d87a58b2ba8f570ee914303be3`), not the test source.

The actual test source is the controller manifest tuple: Agent commit `120d71202a9ebafa99011aec417cfca6d67fafc2`, tree `9a65a32e4462464825df6cfe4d913408694ad4c5`, checkout `/home/user/work/wt/agt-pin-120d7120`. The parsed launcher command asserts that exact HEAD/tree and the corresponding Runtime/App/Composition heads and trees, then invokes the pinned D73 launcher with `PYTHONPATH=/home/user/work/wt/agt-pin-120d7120:/home/user/work/wt/rt-pin-1daca2a3`. The launcher checks its own pinned path, exact checkout trees, clean state and parent guards. Its preflight imports `astrid`, `astrid_runtime_client`, Agent schema, Runtime `runtime_protocol`, and shared schema, asserting the pinned `__file__` paths; run mode invokes the pinned Python. Preflight exit was `0`; body exit was `1`.

Correction: `f43dd198…` is an ambient mutable service snapshot label; `9a65a32e…` is the actual pinned Agent test source. The original source tuple is retained exactly, with no classification/source retagging.

The first `coverage.txt` block is stale intermediate metadata. Its immediately following `CORRECTED_COVERAGE_CHECK` has all 22 roots, no missing roots, and complete coverage; the root argv includes `tests/packs/rendering/test_live_scene_composition.py`. The terminal/accounting result remains 9,273 XML cases, 8,823 PASS, 159 FAIL, 291 ERROR, 173 subtests, 0 skips, 450 bad, core-open 425, REG 14.

Original preimage/reference hashes are preserved in the JSON companion and worker evidence. No original file was scribbled and no new proof was created.
