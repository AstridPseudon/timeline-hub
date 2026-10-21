# Run-on-main result: App public Trim

Status: **REFUSED-PREFLIGHT**

Selected source: integrated App commit `0cc2583aaf07e89190b9344b5ac82849d6279586`, tree `320e74a93676c781e83885b86ec237b4a1465d80`.

## Exact commits and trees verified

- App integration ancestor: `1490fbfe90f83c7c7c380d5cb16ccfcc0e9dcfcf` / `8e242d1497841f391b6152ecd8d204143fa03b52`; selected source descends from it.
- r40 source: `eb51ff381660a90e847c70371fcb64b8eca4d113` / `525ce6d726ab36d743e4504fa2e1b274bfa21b41`; reachable from the exact hub r40 ref.
- r41 review: `eb51ff381660a90e847c70371fcb64b8eca4d113` / `525ce6d726ab36d743e4504fa2e1b274bfa21b41`.
- Integrated source: `0cc2583aaf07e89190b9344b5ac82849d6279586` / `320e74a93676c781e83885b86ec237b4a1465d80`.
- r43 fallback: `76d1397d80b4f409c1062814b09d452e881d1748` / `9ac48c4d7a5152be3469781178fb9987ca95909f` (verified, not selected).
- All seven packet-listed integrated r43 support blobs matched.
- Agent: `6efc81500a0e0688c2bb41e736503f0fc3e04abb` / `2ed2b8a12b5b3391ca221ba6ff05390f71a73556`, clean.
- Runtime: `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c` / `d3a290b407fa61e6ab2d476f50c068073f70df00`, clean.
- Runtime manifest: 76 artifacts; producer version `sha256:54205b3ecb55038e416b31af936c9af26afa30dc1b05da16157ee4d861fe05ac`.
- Composition C13 archive: SHA-256 `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`, 77 regular members.
- Vendor provenance: `091aa23ec83ea05ffd3b0115a640230d51c8c429` / `e3ae90fe482ba6cad6c3f94069127faf76ebceb6`.

The required `git fetch hub` was attempted from `/home/user/work/app`, but failed to write `/home/user/banodoco/reigh-app/.git/worktrees/om-app-public-trim-current/FETCH_HEAD` because shared worktree metadata is read-only. Existing exact refs/objects matched; no substitute was used.

## Missing preflight items

1. Main root `/home/user/work/tl-app-public-trim-current-r43`, its private source checkout, graph, run/cache/home/private directories, and evidence directory were absent.
2. `$MAIN/node-v20.19.4-linux-x64/bin/node` was absent. Exact Node `v20.19.4` exists at `/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node`, but was not substituted.
3. The required private symlink-free `$MAIN/graph/c13/node_modules` was absent. The only C13 candidate was shared/linked `/home/user/work/runtimes/agent-remotion-0013/node_modules`, which cannot be used.
4. The private13 install unit is absent in this worker environment; no install, extraction, build, or copy was attempted.
5. `git fetch hub` could not update `FETCH_HEAD` due the read-only shared metadata.

Chromium, exact pins, vendor identity, Runtime manifest, C13 archive, free port `17340`, clean App source, and the 5 GB disk floor passed. Available disk was 9.9 GB.

## Exact command, counts, paths, and non-runs

The exact packet commands below were authorized but not run:

```bash
cd "$APP"
env -i HOME="$MAIN/home" LANG=C.UTF-8 PATH="$MAIN/node-v20.19.4-linux-x64/bin:/usr/bin:/bin" ASTRID_CHECKOUT="$AGENT" ASTRID_RUNTIME_CHECKOUT="$RUNTIME" ASTRID_PYTHON=/home/user/work/venv-agent/bin/python ASTRID_RUNTIME_PYTHON=/home/user/work/venv-runtime/bin/python TIMELINE_BUNDLE_AGENT_HEAD=6efc81500a0e0688c2bb41e736503f0fc3e04abb TIMELINE_BUNDLE_RUNTIME_HEAD=95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c PRIVATE13_NODE_MODULES="$GRAPH/node_modules" VITE_TIMELINE_COMPOSITION_ROOT="$GRAPH/node_modules/@banodoco/timeline-composition" PLAYWRIGHT_CHROMIUM_EXECUTABLE=/opt/pw-browsers/chromium-1194/chrome-linux/chrome PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers ASTRID_APP_DIRECT_DOOR_PORT=17340 TMPDIR="$MAIN/run/t" XDG_RUNTIME_DIR="$MAIN/run" PWTEST_CACHE_DIR="$MAIN/cache/pw" VITE_CACHE_DIR="$MAIN/cache/vite" XDG_CACHE_HOME="$MAIN/cache/xdg" npm_config_cache="$MAIN/cache/npm" npm_config_offline=true npm exec -- playwright test --config playwright.public-trim.config.ts --list
```

```bash
cd "$APP"
env -i HOME="$MAIN/home" LANG=C.UTF-8 PATH="$MAIN/node-v20.19.4-linux-x64/bin:/usr/bin:/bin" ASTRID_CHECKOUT="$AGENT" ASTRID_RUNTIME_CHECKOUT="$RUNTIME" ASTRID_PYTHON=/home/user/work/venv-agent/bin/python ASTRID_RUNTIME_PYTHON=/home/user/work/venv-runtime/bin/python TIMELINE_BUNDLE_AGENT_HEAD=6efc81500a0e0688c2bb41e736503f0fc3e04abb TIMELINE_BUNDLE_RUNTIME_HEAD=95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c PRIVATE13_NODE_MODULES="$GRAPH/node_modules" VITE_TIMELINE_COMPOSITION_ROOT="$GRAPH/node_modules/@banodoco/timeline-composition" PLAYWRIGHT_CHROMIUM_EXECUTABLE=/opt/pw-browsers/chromium-1194/chrome-linux/chrome PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers ASTRID_APP_DIRECT_DOOR_PORT=17340 TMPDIR="$MAIN/run/t" XDG_RUNTIME_DIR="$MAIN/run" PWTEST_CACHE_DIR="$MAIN/cache/pw" VITE_CACHE_DIR="$MAIN/cache/vite" XDG_CACHE_HOME="$MAIN/cache/xdg" npm_config_cache="$MAIN/cache/npm" npm_config_offline=true PLAYWRIGHT_OUTPUT_DIR="$EVIDENCE/browser-artifacts" npm exec -- playwright test --config playwright.public-trim.config.ts tests/e2e/local/public-trim-mounted-fixture.spec.ts > "$EVIDENCE/playwright.log" 2>&1
```

Counts: 0 collected, 0 executed, 0 passed, 0 failed. No browser, Runtime, discovery proxy, Vite, or daemon started.

Expected log path (not created): `/home/user/work/tl-app-public-trim-current-r43/evidence/public-trim-current/playwright.log`.

Expected trace/artifact path (not created): `/home/user/work/tl-app-public-trim-current-r43/evidence/public-trim-current/browser-artifacts`.

Classification: **missing prerequisite / environment**. The actual is not a product or harness failure. Recommended next step: materialize the private symlink-free C13 graph and specified main run root, then rerun after a successful `git fetch hub`.
