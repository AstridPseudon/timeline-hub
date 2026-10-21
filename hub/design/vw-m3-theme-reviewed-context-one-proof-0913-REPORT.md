# Theme reviewed-context proof — result

- **PASS**, one central request only; result ID:
  `vw-m3-theme-reviewed-context-one-proof-0913-integration-viewing-theme-normal-props-reviewed-context-one-proof-0913-1021091621-2747`
- Result directory: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/vw-m3-theme-reviewed-context-one-proof-0913-integration-viewing-theme-normal-props-reviewed-context-one-proof-0913-1021091621-2747`
- Exact result/error stage: `1 passed in 110.30s`, exit `0`; no error stage.
- Log SHA-256: `43fc1408974cc1e66ad9575409bf26d86d90248ae1a571d18a9990a66a9d462a`.
- Summary SHA-256: `caf07c6cfa4a9e5dbeb39ddb1271279e9a67893a8a0e4c674481c1014eeee714`.
- Snapshot tree: `58d9ca46ee80316647c774f9e8a2c9025b9c62a9`; key `bb7ba26ba0ed51d5bc3a378b1ad70a5e`.

Applied only the approved 0912 test-fixture hunk: `ASTRID_PACKS_PATH` is
cleared inside `monkeypatch.context()` around `sdk.invoke` and restored for
the existing materialization, one-resolver, Root props, default, and refusal
assertions. Source SHA-256:
`8a360a49b270fa8762e9f238805455f52bafcd1fe29f9c22dbff8bc8c46cd7a8`.
Working-tree patch SHA-256:
`87ce86901a802368fe8949f62e458d1813181755bf41594c60a0e3cf39e23cb8`.

Registered unique suite in
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/suites.conf`
with exactly one suite-owned `flock -x /tmp/timeline-viewing-browser.lock`
around the exact existing command. The old command was lock-free. The
returned request path was normalized with `basename`; only that ID was waited.

Exact suite command:

```sh
flock -x /tmp/timeline-viewing-browser.lock env -u NODE_OPTIONS -u NODE_PATH ASTRID_TEST_REMOTION_DEPENDENCY_ROOT=/home/user/work/runtimes/agent-remotion-viewing13-d0a5072b/node_modules ASTRID_REMOTION_PROJECT_DIR=/home/user/work/runtimes/agent-remotion-viewing13-d0a5072b ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-8f105c26 ASTRID_RUNTIME_PYTHON=/home/user/work/venv-runtime/bin/python ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node PATH=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin:/home/user/work/venv-agent/bin:/usr/local/bin:/usr/bin:/bin PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider -m integration --tb=short tests/integrations/test_generic_host_remotion_render.py::test_generic_host_normal_imported_theme_reaches_props_and_rejects_local_source
```

Request and wait were exactly:

```sh
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test vw-m3-theme-reviewed-context-one-proof-0913 integration-viewing-theme-normal-props-reviewed-context-one-proof-0913
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test vw-m3-theme-reviewed-context-one-proof-0913-integration-viewing-theme-normal-props-reviewed-context-one-proof-0913-1021091621-2747
```

Preflight passed: Ruff, diff check, one collected node, pinned Node
`v20.19.4`, Runtime `8f105c26e3b62f9c2683f717a9773a12bc775a8e`, Remotion
`4.0.509`, realpath/graph guards, no active Gate6/theme request, and
`12080062464` free bytes against the `11253940118` floor. No browser, MP4,
full suite, alternate, retry, product change, or validation relaxation.

The central snapshot was removed and the shared browser lock is free. Worker
report and commit message are in the assigned worker directory.
