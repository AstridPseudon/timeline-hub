# Run-on-main result: App original parent split, current paired-seek source

Status: **REFUSED-PREFLIGHT**

No collection or actual was run. The packet requires refusal when the exact
source/private fixture prerequisites are unavailable; no substitute source,
graph, credential, or dependency was used.

## Exact identities verified

| item | commit | tree | result |
|---|---|---|---|
| Packet App source object | `435e76eb3f2dcaa0324ed69d4c019ab9c32bfbef` | `daf4e71ba71ebaf6a2bc8b6cd6e66fc13d762273` | verified in `/home/user/work/app` |
| r44 paired-seek fix | `e1c0d8d52bd37c792368523ce8a6bfc7a55ad40a` | `51534291177131094cc8da49a02792be21b59c5a` | verified |
| r45 independent review | `e1c0d8d52bd37c792368523ce8a6bfc7a55ad40a` | `51534291177131094cc8da49a02792be21b59c5a` | verified |
| integration merge | `2b85341ef724a15f34179e270a7acf323ac7b878` | `5ea64a704797fd034fb5fd184832448ae6b12ce0` | verified |
| Agent execution | `6efc81500a0e0688c2bb41e736503f0fc3e04abb` | `2ed2b8a12b5b3391ca221ba6ff05390f71a73556` | verified |
| Agent vendor | `091aa23ec83ea05ffd3b0115a640230d51c8c429` | `e3ae90fe482ba6cad6c3f94069127faf76ebceb6` | verified as object |
| Runtime producer | `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c` | `d3a290b407fa61e6ab2d476f50c068073f70df00` | verified |

The fetched `hub/timeline/app/tl/integration` resolves to
`0cc2583aaf07e89190b9344b5ac82849d6279586` / tree
`320e74a93676c781e83885b86ec237b4a1465d80`, not the packet source. The exact
source keeper ref `hub/timeline/app/tl/app-m2-split-reviewed-main-packet-r46`
does resolve to the packet App commit/tree, but no private App source keeper
was available in the prescribed main layout.

The four packet-file SHA-256 values matched. The approved Composition archive
matched `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`
with 77 safe regular entries and no duplicate/traversal entries. The exact
Runtime manifest contained 76 artifacts and the expected producer digest
`sha256:54205b3ecb55038e416b31af936c9af26afa30dc1b05da16157ee4d861fe05ac`.

## Missing prerequisites (single list)

- The prescribed private main layout `/home/user/work/tl-split-main-435e`
  and its private App, Agent-vendor, Runtime, graph, credential, READY,
  LEASE, evidence, temp, profile, and socket paths were absent.
- The existing private public13 graph was absent. The only App
  `node_modules` found was the physical shared install at
  `/home/user/work/app/node_modules`, which the packet explicitly forbids
  using as `PRIVATE13_NODE_MODULES`.
- No mode-0600 Runtime product credential was available; therefore the
  credential guard could not pass.
- No private Agent-vendor-091 keeper was available. Clean exact Agent-6ef and
  Runtime-95 pin worktrees were present, but that did not supply the missing
  vendor/graph/credential setup.
- The packet's concrete `$MAIN/node-v20.19.4-linux-x64/bin/node` path was
  absent because the private main layout was absent. The shared toolchain
  prerequisite itself passed separately: `/home/user/work/toolchain/.../node`
  reported `v20.19.4`.

Chromium `/opt/pw-browsers/chromium-1194/chrome-linux/chrome` was executable,
port 17340 was free, and `/home/user/work` had approximately 9.8 GB free
(above the 5 GB minimum). Ambient `NODE_OPTIONS` and `NODE_PATH` were present
in this shell, but the packet's required `env -i` would unset them; no process
was started.

## Requested command (not run)

```bash
cd "$APP"
env -i \
  HOME="$MAIN/h" LANG=C.UTF-8 PATH="$MAIN/node-v20.19.4-linux-x64/bin:/usr/bin:/bin" \
  ASTRID_CHECKOUT="$AGENT" ASTRID_RUNTIME_CHECKOUT="$RUNTIME" \
  ASTRID_PYTHON=/home/user/work/venv-agent/bin/python \
  ASTRID_RUNTIME_PYTHON=/home/user/work/venv-runtime/bin/python \
  TIMELINE_CURRENT013_APP_SHA=435e76eb3f2dcaa0324ed69d4c019ab9c32bfbef \
  TIMELINE_CURRENT013_APP_TREE=daf4e71ba71ebaf6a2bc8b6cd6e66fc13d762273 \
  TIMELINE_CURRENT013_AGENT_SHA=6efc81500a0e0688c2bb41e736503f0fc3e04abb \
  TIMELINE_CURRENT013_RUNTIME_SHA=95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c \
  TIMELINE_CURRENT013_AGENT_VENDOR_CHECKOUT="$AGENT_VENDOR" \
  TIMELINE_CURRENT013_RUNTIME_PRODUCER_CHECKOUT="$RUNTIME" \
  PRIVATE13_NODE_MODULES="$GRAPH/node_modules" \
  TIMELINE_CURRENT013_PRIVATE13_READY="$PRIVATE/READY" \
  TIMELINE_CURRENT013_PRIVATE13_LEASE="$PRIVATE/LEASE" \
  TIMELINE_CURRENT013_SHORT_TMPDIR="$SHORT" \
  TIMELINE_CURRENT013_CONFIG_PATH="$CONFIG" \
  WORKSPACE_RUNTIME_TOKEN_FILE="$PRIVATE/product-credential.json" \
  TIMELINE_BUNDLE_AGENT_HEAD=6efc81500a0e0688c2bb41e736503f0fc3e04abb \
  TIMELINE_BUNDLE_RUNTIME_HEAD=95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c \
  PLAYWRIGHT_CHROMIUM_EXECUTABLE="$CHROME" PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers \
  ASTRID_APP_DIRECT_DOOR_PORT=17340 \
  TMPDIR="$TMP" XDG_RUNTIME_DIR="$SOCKET" \
  npm_config_cache="$MAIN/n" npm_config_offline=true PWTEST_CACHE_DIR="$MAIN/w" \
  VITE_CACHE_DIR="$MAIN/v" XDG_CACHE_HOME="$MAIN/c" \
  PLAYWRIGHT_OUTPUT_DIR="$EVIDENCE" \
  npm exec -- playwright test \
    --config "$CONFIG" tests/e2e/local/parent-split-command.spec.ts
```

## Counts and evidence

- Collection: 0 tests in 0 files; the mandatory `--list` was not run because
  the private graph/source/credential preflight failed.
- Actual: 0 passed, 0 failed, 0 skipped, 0 unexpected; not run.
- Expected log path: `/home/user/work/tl-split-main-435e/evidence/split-current/playwright.log`.
- Trace/failure-context path: none; no evidence directory was created and no
  browser, Runtime, Vite, socket, build, install, or localhost process ran.

Failure classification: **missing prerequisite / exact source publication
mismatch**, not a product or harness failure. The run was not retried.
