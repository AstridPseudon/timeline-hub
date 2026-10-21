# Agent + Runtime handoff: normal imported Theme proof

## Result

**PASS — one central request, one test, one pass.** This is the actual 0913
normal proof result, not an inference from materialization.

- Source: Agent commit `966c7c6091ae7c1c2226ebb539c7408903c6a9cc`, with only
  the approved scoped fixture hunk; changed source SHA-256
  `8a360a49b270fa8762e9f238805455f52bafcd1fe29f9c22dbff8bc8c46cd7a8`;
  central snapshot tree `58d9ca46ee80316647c774f9e8a2c9025b9c62a9`.
- Runtime: `/home/user/work/wt/rt-pin-8f105c26`, commit
  `8f105c26e3b62f9c2683f717a9773a12bc775a8e`.
- C13: `@banodoco/timeline-composition@0.0.13`, 77 package members;
  `/home/user/work/runtimes/agent-remotion-viewing13-d0a5072b/artifacts/banodoco-timeline-composition-0.0.13.tgz`,
  SHA-256 `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`.
- Command:

  ```sh
  flock -x /tmp/timeline-viewing-browser.lock env -u NODE_OPTIONS -u NODE_PATH ASTRID_TEST_REMOTION_DEPENDENCY_ROOT=/home/user/work/runtimes/agent-remotion-viewing13-d0a5072b/node_modules ASTRID_REMOTION_PROJECT_DIR=/home/user/work/runtimes/agent-remotion-viewing13-d0a5072b ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-8f105c26 ASTRID_RUNTIME_PYTHON=/home/user/work/venv-runtime/bin/python ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node PATH=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin:/home/user/work/venv-agent/bin:/usr/local/bin:/usr/bin:/bin PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider -m integration --tb=short tests/integrations/test_generic_host_remotion_render.py::test_generic_host_normal_imported_theme_reaches_props_and_rejects_local_source
  ```

  The same command is retained in the central summary at
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/vw-m3-theme-reviewed-context-one-proof-0913-integration-viewing-theme-normal-props-reviewed-context-one-proof-0913-1021091621-2747/summary`.
- Test ID:
  `vw-m3-theme-reviewed-context-one-proof-0913-integration-viewing-theme-normal-props-reviewed-context-one-proof-0913-1021091621-2747`.
- Count/result: `1 passed in 110.30s (0:01:50)`, exit `0`.
- Raw log:
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/vw-m3-theme-reviewed-context-one-proof-0913-integration-viewing-theme-normal-props-reviewed-context-one-proof-0913-1021091621-2747/log.txt`,
  SHA-256 `43fc1408974cc1e66ad9575409bf26d86d90248ae1a571d18a9990a66a9d462a`.

## Stage reached and retained assertions

The existing normal Main path reached Runtime admission, the real imported
CAS object descriptors, managed named `theme.json` materialization, one theme
resolver, Root props, omitted-theme builtin/default separation, and forged
caller-local source refusal. The admission assertion retains the imported
input object IDs/digests and input order `timeline`, `assets_registry`,
`theme` (filename `theme.json`), then `selector`; materialization asserts the
named managed file and exact imported Theme contents. Root props assert the
explicit imported Theme identity/color; omission asserts the builtin differs;
the forged local path is refused with `requires a managed Runtime object`.

This is a pre-render props proof. It does not claim a final render, MP4,
browser, pixel/audio parity, raw-managed/file-mode authority, or a new source
authority. `privateThemeDocument`/preparation remains deferred. The proof
preserves the Main imported `theme.json` path and uses no product or validation
relaxation.

Supporting report: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/vw-m3-theme-reviewed-context-one-proof-0913-REPORT.md`.
