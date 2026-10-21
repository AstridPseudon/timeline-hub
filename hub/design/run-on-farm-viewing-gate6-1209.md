# Viewing Gate6 farm request — executable publication

Status: HOLD.

This is one farm request for the already reviewed native-codec Gate6 packet.
Do not run it, request a local test, create a token/grant/marker, start a
browser/Runtime/socket/helper, or change product, test, or controller source
until the viewing manager authorizes the farm phase.

## Frozen execution tuple: historical 0d43/C13

The packet and controller are frozen to this historical tuple. The current
integration checkpoint below is intentionally not a substitute for it.

| input | commit | tree | required checkout |
| --- | --- | --- | --- |
| App | `0d4323913b92c4e0e3830bf14ec7f35d981475ca` | `5a1e0e85d0f336f642426b91ccf3b3f1984ebd14` | `/home/user/work/wt/app-pin-0d432391` |
| Agent/sdk | `d0a5072bbe7b7ce9489f43aa0a81027ec400343b` | `6adb4a1190dfb2874e101565f37eccd392b1ae2f` | `/home/user/work/wt/agt-pin-d0a5072b` |
| Runtime server | `8f105c26e3b62f9c2683f717a9773a12bc775a8e` | `b7f456d5135cba6049980ebc43a91c7a72ab8f7e` | `/home/user/work/wt/rt-pin-8f105c26` |
| Runtime producer/client | `2c4ac180c2220bdad966bc01e95ad230e99ce26a` | `7ab412cc4bcbe517efcfa806e092336390312e18` | the pinned Runtime source/artifact carrier |
| Composition C13 | `5a4e9b72f1916c4da01fa370ec5fe8d46b6da8e8` | `13e375534fffd704305eced5686699d2c8c9c948` | `/home/user/work/wt/vw-pin-5a4e9b72` |

Before execution, verify each checkout with both `git rev-parse HEAD` and
`git rev-parse HEAD^{tree}`. The Agent commit is the complete 40-hex object
`d0a5072bbe7b7ce9489f43aa0a81027ec400343b`; the earlier 39-hex spelling is
invalid and must not be used.

## Current checkpoint (reference only)

Observed on 2026-10-21 from the clean `/home/user/work/{agent,runtime,app,composition}`
integration worktrees; this table is not an authorization to substitute these
heads into the frozen Gate6 packet:

| repo | commit | tree |
| --- | --- | --- |
| Agent | `c9ac7c7b0e862ad32a919db33859c5fcbf58ad99` | `cab0a2aa34ba6dae880657eb484979039e206049` |
| Runtime | `0906f729d8c0f323cb29384ea032c38de640f96e` | `f96fbf48c298a1ede56eda05a34aa87bcb70d7e3` |
| App | `5f513665a6961e3552cf47bf70303fe41f370ba3` | `1c28244f9de4399070bc31772aef2d1a6cfca128` |
| Composition | `df7b86308902fae90eda1dc3080d17d8fc30ea78` | `71d8e95edb1bb2d187c3193ef3462d4cfde277fa` |

## Exact packet and reviewed identities

The executable packet directory is this absolute directory:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/`

Use the ten bare script names and `SHA256SUMS` there. They are byte-for-byte
copies of the committed `tl/vw-m3-gate6-farm-transport-1210` export at
`9361d5002339adaaf2bcc80322a4695fbeaae984`; the prefixed
`handoff-vw-gate6-farm-1210-*` files are the exact archival copies. The
reviewed packet manifest digest is
`0ee53582e55a4f9eb8464a2d7581924cf42bb5a56f3d75de362991f3e196299e`.

The source packet contains exactly eleven regular files: the ten files listed
in `SHA256SUMS` plus `issue.mjs` as the unexecuted issuance source. No token,
grant, marker, generated operational JSON, source graph, node_modules, media,
archive, or build output is published here.

Required external immutable inputs:

- 1054 complete stage at
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-storage-cleared-complete-runtime-stage-1054/owned-stage`,
  with its three sibling metadata files in that worker directory; stage graph
  `4913a37e5403c8372a283dcca8fd30c846b636abd88f59cfc572809d2fd0bd3c` and
  21,455 entries (21,422 regular files, 33 relative links);
- stage metadata hashes: script
  `24cc758029518075f671b06dffc75582b772f2fc52a5e4b57450b46c08a0c66c`, root
  manifest `b349c5344ec607bc32b0e4711adf317aacd984ce98d3e5a316ba726079bb37ac`,
  graph manifest `0d9da325991bfed2fda247284adb37885d118a08f5f4fc655128f6b7481c04de`;
- separate b70 helper carrier at `/home/user/work/wt/agt-pin-b70b9d56`, commit
  `b70b9d569b2c80885d72734c61cd57e64c3715a8`, tree
  `687f077c4771e3dbb66bfb7ff2b98f310ac054b6`, blob
  `bc75d73f21c6310efad7fc41e4a3d790bfe3a8975e0eb96c08c3dec63e62961b`;
- private App dependency graph `8bdc44e93ce6f712f2a26fc44f1f8e904215c1785f54ed97f826a98fe0145c5b`
  (32,393 entries), App source manifest
  `4fb1e53b2dce325f826b6b071d0782544e5ba2c7b27418b6170f8c947c450435`
  (5,902 files), and retained App dist at
  `/home/user/work/wt/app-pin-d00a6613/dist` (339 files; `index.html`
  `aeb5d83399b453b15a8cbc67b31260cf2820f8d65770ccd458986ddd551e257b`);
- public13 archive
  `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`,
  package lock `c4d7030bd5418d35f2246269b5aba7952d0ed69ccd0084815a0043dfbb7a4e24`,
  and the named immutable media/runtime inputs; binaries and graphs over 50 MB
  remain external and are not packed into design;
- Node `/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node`, version
  20.19.4, SHA-256
  `43d6cf63f2a460b463eba6b19df5e9a259771c56f11b5130e04178a15bb99490`;
  Chrome `/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell`,
  version 155.0.8059.84, executable SHA-256
  `cb19b59995072b86cc7f887b3b1c7ab1f63518a7f2ed9f0d33249e1a040e2c76` and
  package-tree SHA-256 `5b9b48fad617dc414d4a18ccfe9c7933c7bc4a8efd78c70d4f7a9e853808de0e`;
  Remotion 4.0.509, React 18.3.1, React DOM 18.3.1.

Materialize every external input as an independent regular-file graph with
`nlink=1`; preserve relative links only inside the staged Remotion project.
Do not use a flat Remotion copy, cross-source hardlinks, or a symlinked parent.

## Farm path binding and guard ownership

The reviewed scripts already use the exact absolute paths above. The farm may
either materialize those paths or make one private copy of the scripts and
rebind only these constants: packet directory, App, Agent, Runtime, helper,
Composition, stage and metadata roots, App dist, Node/Python, Chrome, and
private run/evidence/temp roots. A rebind must preserve all source/test/hash
assertions and must emit a new local script hash manifest; it must not claim
the reviewed packet digest. No new path framework is permitted.

The farm lead owns the required environment/socket fixes in the existing
controller/preflight: unset `NODE_OPTIONS` and `NODE_PATH` for every Remotion
pack-host process; set `TMP`, `TEMP`, and `XDG_RUNTIME_DIR` to a fresh
mode-0700 private directory; keep the browser socket path under 100 bytes.
Do not expand or rewrite the controller, test bodies, or assertions.

## Exact commands and five bodies

After all inputs and a fresh manager note exist, run these commands once, in
this order, from the packet directory:

```sh
cd /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design
bash /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/run.sh --preflight
bash /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/run.sh
```

The runner's clean child validation is exactly:

```sh
env -i HOME=/root LANG=C.UTF-8 PATH=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin:/home/user/work/venv-agent/bin:/usr/local/bin:/usr/bin:/bin TMPDIR=/tmp/tf-g6-1209 ASTRID_CHECKOUT=/home/user/work/wt/agt-pin-d0a5072b ASTRID_PACK_HOST_HELPER_CHECKOUT=/home/user/work/wt/agt-pin-b70b9d56 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-8f105c26 ASTRID_RUNTIME_PYTHON=/home/user/work/venv-runtime/bin/python ASTRID_PYTHON=/home/user/work/venv-agent/bin/python ASTRID_TIMELINE_SCHEMA_PYTHONPATH=/home/user/work/venv-agent/lib/python3.11/site-packages ASTRID_APP_DIRECT_DIST=/home/user/work/wt/app-pin-d00a6613/dist ASTRID_REMOTION_PROJECT_DIR=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-storage-cleared-complete-runtime-stage-1054/owned-stage/remotion ASTRID_REMOTION_BROWSER_EXECUTABLE=/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node TIMELINE_COMPOSITION_CHECKOUT=/home/user/work/wt/vw-pin-5a4e9b72 TIMELINE_VIEWING_APP_SOURCE=0d4323913b92c4e0e3830bf14ec7f35d981475ca TIMELINE_VIEWING_APP_TREE=5a1e0e85d0f336f642426b91ccf3b3f1984ebd14 PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 TSX_DISABLE_CACHE=1 /home/user/work/venv-agent/bin/python -I /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/prepare-validation-diagnostic.py
```

Preflight must PASS with `token-issued:false`, no marker/grant/Runtime/helper/
browser/socket/render/case body, and no physical run directory. The physical
run is the sole final-gate invocation and must execute exactly five bodies in
this order:

1. normal App Render downloads a valid native-size MP4, without a parity claim;
2. fixture readiness seeks the actual managed Player and captures native frames;
3. native-size actual Player frames compare with decoded real CPU Remotion output;
4. actual Player capture compares native-PTS VP8/Opus audio/video with the same
   normal export, then rejects the planted half-gain PCM mutation;
5. the picture-only one-host patch is reported as a mismatch after the passing
   baseline.

All picture/audio negatives and the five-case order are mandatory. Zero bodies
is FAIL. The farm result belongs at
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/run-on-farm-result-viewing-gate6-1209.md`.

## ALL missing inputs / blockers

1. Fresh manager authorization at
   `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/viewing/notes/grant-discovery-readiness-1153.md`,
   naming the exact packet directory, unchanged 1054 stage, and fresh marker
   path; no prior grant or marker may be reused.
2. Independent materialization of the complete 1054 stage and six-file editor
   closure, its three metadata files, the b70 helper, App graph/source/dist,
   public13 archive/media/runtime inputs, pinned toolchains, and short private
   temp/socket roots.
3. Central preflight and the one authorized physical five-case run are
   unverified. This HOLD request makes no readiness, parity, qualification, or
   M4 claim.
