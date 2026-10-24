## Report

Updated [tools/run-discovery-original-0603.py](/home/user/work/wt/agt-F-discovery-harness-return-0626/tools/run-discovery-original-0603.py).

- Corrected package-lock digest: `f4fc0a32…be18d`; Composition archive remains separately pinned to `819acf6b…40234`.
- Preflight now exits before body execution.
- `run` requires matching reviewed harness SHA and approved manager gate.
- Dirty Agent/Runtime source trees are rejected.
- Parent setup failures retain durable `after.json`.
- Added literal source, body, lock, and canonical origin hashes.
- Preserved 9 assertions, 10 support calls, transition invocation 6, exact selector, production caller, and `--timeout=45`.

Exact future suite row:

```text
tests/packs/rendering/test_threejs_backend.py::test_threejs_support_rejects_unsupported_timelines_with_clip_reasons
```

Hashes:

- Runner: `03be7e7b6d3844365dd5094c91b57dbe7c28ace7a7cf732d6b7cd34a9ef0aada`
- Agent: `bb50a43c915ec00c05c5ee34569a040bab8e817c`
- Runtime: `f3208b26b53c4d7053e5464eaa7c5e15b1505812`
- Discovery source: `40ae7c5945529bb65dbeb3853a80b1b03650e7dcc5f4a60ddaa04c4dc9f37999`
- Target file: `9efe493cb2f8339177e07616b976afe6f9813ae4d415923ff25701b471e991c7`
- Function AST: `ca54f2d5059bb3b5cca1e8ee43156df6762d3a86739caa2aa18ffcb83f3ded82`
- Assertions AST: `087c80d0211e714a7c073d12adb2e260d5de299ba3d251ac31b853562eb6de1e`
- Canonical origins: Agent `a8374cb5…da33`, Runtime `9349a548…ef3b`

Checks passed:

```text
python3 -m py_compile tools/run-discovery-original-0603.py
ruff check --no-cache tools/run-discovery-original-0603.py
ruff format --check --no-cache tools/run-discovery-original-0603.py
git diff --check
```

No provisioning, preflight, body, Node, browser, or original test execution was run. Completion marker and commit message are present.