Implemented harness: [tools/run-render-wire-0124.sh](/home/user/work/wt/agt-F-render-wire-env-0124/tools/run-render-wire-0124.sh:1)

Preflight passed without running original tests:

- `bash -n tools/run-render-wire-0124.sh`
- `git diff --check`
- `tools/run-render-wire-0124.sh preflight`
- Exact collection: 6 selectors
- 19 relevant source/fixture files equal installed Agent c36
- Installed child/runtime/profile/origin/read-only checks passed

Script SHA256: `e983362cb8d2c4a1f6f91365c236788a8f4062705694a9d623254846995a4daf`

Exact suite row:

```text
agent render-wire-0124 test "$(sha256sum tools/run-render-wire-0124.sh | awk '{print $1}')" = e983362cb8d2c4a1f6f91365c236788a8f4062705694a9d623254846995a4daf && env -i HOME=/root LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-8ea0766f" PATH=/home/user/work/bench-store/entries/child-c886d448c07fe72421bfbc708db0dc9399c2833a66b7dadc67625a3df0d4da0e/bin:/usr/bin:/bin ASTRID_HOST_EXECUTION_PROFILE=installed ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-8ea0766f ASTRID_RUNTIME_SOURCE_ROOT=/home/user/work/wt/rt-pin-8ea0766f ASTRID_REMOTION_PROJECT_DIR=/home/user/work/runtimes/agent-remotion-v3-819acf-1110 ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node ASTRID_TEST_NODE_MODULES=/home/user/work/runtimes/agent-remotion-v3-819acf-1110/node_modules ASTRID_TIMELINE_SCHEMA_PYTHONPATH=/home/user/work/venv-agent/lib/python3.13/site-packages bash tools/run-render-wire-0124.sh
```

Scope is only the six original conformance cases; the static-surface seventh case and all other suites are excluded. Actual body execution remains pending the central test service. No product, profile, dependency, or source changes were made.