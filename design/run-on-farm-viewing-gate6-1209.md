# Viewing Gate6 farm request 1209

Status: HOLD

This is a standing Gate6 farm request, not a local preparation retry. Do not
request a local test, issue a token, grant, or marker, or run a browser,
Runtime, socket, render, full suite, or physical test from this worktree.

The 1153 discovery-readiness contract fix and its assertion review are the
authorities for the packet. The 1054 complete owned Runtime stage is the
authority for the Runtime source graph. No unchanged source is under review
again here.

## Immutable tuple

Every checkout must be verified with both commands below before the controller
is allowed to proceed:

```sh
git -C "$APP" rev-parse HEAD
git -C "$APP" rev-parse HEAD^{tree}
```

The required source identities are:

| source | hub ref used to prepare the checkout | commit | tree |
| --- | --- | --- | --- |
| App | `hub/timeline/app/tl/vw-m3-gate6-admission-only-reviewed-source-0914` | `0d4323913b92c4e0e3830bf14ec7f35d981475ca` | `5a1e0e85d0f336f642426b91ccf3b3f1984ebd14` |
| Agent/sdk | `hub/timeline/agent/tl/vw-m3-immutable-d0a-runtime-graph-ready` | `d0a5072bbe7b7ce9489f43aa0a81027ec400343` | `6adb4a1190dfb2874e101565f37eccd392b1ae2f` |
| Runtime server | `hub/timeline/runtime/tl/vw-m3-runtime013-current-server-compatibility` | `8f105c26e3b62f9c2683f717a9773a12bc775a8e` | `b7f456d5135cba6049980ebc43a91c7a72ab8f7e` |
| Runtime producer/client artifacts | `hub/timeline/runtime/tl/app-m3-runtime013-producer-source` | `2c4ac180c2220bdad966bc01e95ad230e99ce26a` | `7ab412cc4bcbe517efcfa806e092336390312e18` |
| Composition | `hub/timeline/composition/tl/vw-m3-agent13-pin-source-final-gate` | `5a4e9b72f1916c4da01fa370ec5fe8d46b6da8e8` | `13e375534fffd704305eced5686699d2c8c9c948` |

These are the historical R4 refs, retained for provenance only and never to be
checked out over the run inputs:

| repo | frozen ref | commit | tree |
| --- | --- | --- | --- |
| Agent/sdk | `origin/codex/handover-timeline-r4-20261019-candidate-sdk` | `11caf1d9de291d76f491cf69f7942606b7471d7a` | `f6f4fad77ded050b1e9c2d802cc3da35b459e610` |
| Runtime | `origin/codex/handover-timeline-r4-20261019-candidate-runtime` | `31c7ac3a00f7a205f507bf5bd4d4625628d429bd` | `73e676f420ba0545b6eebe45870d532344a9e69b` |
| App | `origin/codex/handover-timeline-r4-20261019-candidate-app-qualified` | `8f0c2484463e9b666d184a744d52e252984e551a` | `26ad064632fac9ff123670aa7d6ed0e3d8f89178` |
| Composition | `origin/codex/handover-timeline-r4-20261019-candidate-composition` | `c82eb7c459d0a41263954bf007071a6a0e8e0a6a` | `49975e7a54fd594e1b7fc807681fe28611d57864` |

## Transported inputs and hashes

Transport the complete corrected packet directory, preserving all eleven
regular files and its mode bits:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-discovery-readiness-contract-fix-1153/packet/`

The packet manifest digest is
`0ee53582e55a4f9eb8464a2d7581924cf42bb5a56f3d75de362991f3e196299e`.
The packet `SHA256SUMS` entries are:

```text
91e047ef8c3083b8f1cdfd326005bd286cdcf3daa3ab4e39cf608473de217192  discovery-readiness.mjs
fb7632d2c69da10c65db04052f0b04ede1b6e72064817fdc600098135ea50dfd  dist-availability.mjs
f88b1885196984826cfb505ed7e1a12783f98b98e21f8ae131e2af6b0d8b8479  issue.mjs
8b7f352688edd511f5194f8fbec44abd8e295ffd02246a2e49252a65e3b7456d  packet-ready.mjs
43d35af7621732d31290a15e1cb872e9ad0a0432709111d836dd40cfd32b9c12  prepare-validation-diagnostic.py
ecd8182718707e76336ccf9913756b08b8cc011ae72cffba8a8dc204d8039cf7  prepare.mjs
26091f1ff5015c44a510e6629f62e593fd12088fad6281f122dd22ec21a3b418  preflight.sh
b51a2837810d951abfc7a696aff5a34f2a98da2299b442b77714e4a234063b4e  run.sh
654013afd77ca5baf793b4120c088b3985da3b30bbf2c90cda49cd85cafebcd3  short-player-temp-controls.py
70f2394e2fa174605f73f275d166bcb922955ff02004be115a744269b87c0a41  stage-audit.mjs
```

Retain the existing stage; do not restage it from a flat `remotion/` source:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-storage-cleared-complete-runtime-stage-1054/owned-stage/`

Transport its three sibling metadata files from the stage worker directory,
not from inside the source checkout:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-storage-cleared-complete-runtime-stage-1054/stage-complete-runtime.sh
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-storage-cleared-complete-runtime-stage-1054/stage-manifest.tsv
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-storage-cleared-complete-runtime-stage-1054/node-graph-manifest.tsv
```

Its transport files and hashes are:

```text
24cc758029518075f671b06dffc75582b772f2fc52a5e4b57450b46c08a0c66c  stage-complete-runtime.sh
b349c5344ec607bc32b0e4711adf317aacd984ce98d3e5a316ba726079bb37ac  stage-manifest.tsv
0d9da325991bfed2fda247284adb37885d118a08f5f4fc655128f6b7481c04de  node-graph-manifest.tsv
4913a37e5403c8372a283dcca8fd30c846b636abd88f59cfc572809d2fd0bd3c  remotion graph/content
c4d7030bd5418d35f2246269b5aba7952d0ed69ccd0084815a0043dfbb7a4e24  remotion/package-lock.json
bf6af4fbe7e5eeef9dcc267c21728b3253544f94170871310a45661729184b88  remotion/src/effects.generated.ts
b78ce0baa5a25bed3db9de377820b37f822b1651b53bfb0a9d52e19793ce8fea  remotion/src/animations.generated.ts
2a2fd68e81ab0875803321051608a23493b812182a02d8674522cd25b25450a0  remotion/src/transitions.generated.ts
```

The stage must contain the complete sibling closure: `remotion/` plus the six
independent d0a editor/live-scenes files under
`astrid/packs/rendering/editor/live-scenes/`. It has 21,455 graph entries
(21,422 regular files and 33 relative links). Every staged regular file must
have a distinct source inode and `nlink=1`; the six closure files must meet the
same rule. Relative links must remain inside staged `remotion/`. No flat
Remotion-only copy and no cross-source hardlink is acceptable.

The six closure paths are:

```text
astrid/packs/rendering/editor/live-scenes/SceneSurface.tsx
astrid/packs/rendering/editor/live-scenes/authoring.ts
astrid/packs/rendering/editor/live-scenes/diagnostics.ts
astrid/packs/rendering/editor/live-scenes/extension.tsx
astrid/packs/rendering/editor/live-scenes/identity.ts
astrid/packs/rendering/editor/live-scenes/runtime.ts
```

Other required immutable inputs:

```text
App private node_modules graph: 8bdc44e93ce6f712f2a26fc44f1f8e904215c1785f54ed97f826a98fe0145c5b (32393 entries)
App source manifest: 4fb1e53b2dce325f826b6b071d0782544e5ba2c7b27418b6170f8c947c450435 (5902 files)
Composition public13 archive: 9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738 (77 regular members)
Retained App dist: 339 regular files; index.html aeb5d83399b453b15a8cbc67b31260cf2820f8d65770ccd458986ddd551e257b
Reviewed pack-host helper: b70b9d569b2c80885d72734c61cd57e64c3715a8; tree 687f077c4771e3dbb66bfb7ff2b98f310ac054b6; blob bc75d73f21c6310efad7fc41e4a3d790bfe3a8975e0eb96c08c3dec63e62961b
Node: v20.19.4; executable SHA-256 43d6cf63f2a460b463eba6b19df5e9a259771c56f11b5130e04178a15bb99490
Player Chrome: 155.0.8059.84; executable SHA-256 cb19b59995072b86cc7f887b3b1c7ab1f63518a7f2ed9f0d33249e1a040e2c76; package tree SHA-256 5b9b48fad617dc414d4a18ccfe9c7933c7bc4a8efd78c70d4f7a9e853808de0e (255 files)
Remotion/peer versions: Remotion 4.0.509, React 18.3.1, React DOM 18.3.1
```

The public13 transport source is
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/artifacts/banodoco-timeline-composition-0.0.13.tgz`; the
stage copy is `remotion/artifacts/banodoco-timeline-composition-0.0.13.tgz`
and the App copy is `vendor/artifacts/banodoco-timeline-composition-0.0.13.tgz`.
All three must be regular files with the public13 hash above.

The App source files that the controller must see at the App pin include
`playwright.viewing-parity.normal-profile-native1920.config.ts`,
`playwright.viewing-parity.native-codec.config.ts`,
`tests/e2e/timeline/viewing-parity/cases.ts`,
`tests/e2e/timeline/viewing-parity/canvas.test.ts`,
`tests/e2e/timeline/viewing-parity/tab-audio.controller.mjs`,
`tests/e2e/timeline/viewing-parity/harness.ts`,
`tests/e2e/timeline/viewing-parity/bootstrap.ts`,
`tests/e2e/timeline/viewing-parity/browser-profile.ts`, and
`tests/e2e/timeline/viewing-parity/audio-join.ts`. They are source inputs, not
transport replacements; the App manifest and graph checks must cover them.

## Farm path binding and clean environment

The absolute paths embedded in the reviewed packet are machine-specific. The
farm lead may replace only those path bindings with farm-local real directories
and private short temporary directories. This replacement does not change any
source commit, source tree, graph digest, package/browser/toolchain hash, or
test body. Recompute and record the transported script hashes if a script is
rewritten for path binding; never claim the original packet digest for a
rewritten file. Do not use a symlinked parent to hide a shared install, and do
not use hardlinks between source graphs. Check `realpath` for every replacement.

The reviewed command shape is the following exact clean child invocation; use
the farm's real paths only in the named path values:

```sh
env -i \
  HOME=/root LANG=C.UTF-8 \
  PATH=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin:/home/user/work/venv-agent/bin:/usr/local/bin:/usr/bin:/bin \
  TMPDIR=/tmp/tf-g6-1209 \
  ASTRID_CHECKOUT=/home/user/work/wt/agt-pin-d0a5072b \
  ASTRID_PACK_HOST_HELPER_CHECKOUT=/home/user/work/wt/agt-pin-b70b9d56 \
  ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-8f105c26 \
  ASTRID_RUNTIME_PYTHON=/home/user/work/venv-runtime/bin/python \
  ASTRID_PYTHON=/home/user/work/venv-agent/bin/python \
  ASTRID_TIMELINE_SCHEMA_PYTHONPATH=/home/user/work/venv-agent/lib/python3.11/site-packages \
  ASTRID_APP_DIRECT_DIST=/home/user/work/wt/app-pin-d00a6613/dist \
  ASTRID_REMOTION_PROJECT_DIR=/tmp/owned-stage-1054/remotion \
  ASTRID_REMOTION_BROWSER_EXECUTABLE=/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell \
  ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node \
  TIMELINE_COMPOSITION_CHECKOUT=/home/user/work/wt/vw-pin-5a4e9b72 \
  TIMELINE_VIEWING_APP_SOURCE=0d4323913b92c4e0e3830bf14ec7f35d981475ca \
  TIMELINE_VIEWING_APP_TREE=5a1e0e85d0f336f642426b91ccf3b3f1984ebd14 \
  PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 TSX_DISABLE_CACHE=1 \
  /home/user/work/venv-agent/bin/python -I /path/to/transported-packet/prepare-validation-diagnostic.py
```

The controller's own `preflight.sh` must additionally unset `NODE_OPTIONS` and
`NODE_PATH` for every Remotion pack-host process, set `TMP`, `TEMP`, and
`XDG_RUNTIME_DIR` to a mode-0700 short farm directory, and keep the browser
socket path below 100 bytes. The farm lead applies these known environment and
socket fixes in the existing controller/preflight; do not rebuild the
controller or alter its assertions.

## Run contract

After all prerequisites below are present and verified, request exactly these
two central commands, in order, once each:

```sh
bash /path/to/transported-packet/run.sh --preflight
bash /path/to/transported-packet/run.sh
```

The preflight must finish PASS with `token-issued:false`, no marker/grant,
Runtime, helper, browser, socket, render, or case body. Only then may the
physical command run. The physical command is the sole final-gate execution;
do not retry it or submit an alternate request. The existing controller must
create the one-shot grant and marker only inside that physical invocation.

The physical run must execute the existing `native-codec-chrome155` project
with exactly five bodies, in this order:

1. normal App Render downloads a valid native-size MP4 without a parity claim;
2. fixture readiness seeks the actual managed Player and captures native frames
   without export;
3. native-size actual Player frames compare with the decoded real CPU Remotion
   task output;
4. actual Player page capture compares native-PTS VP8/Opus audio/video against
   the same normal export, then rejects the planted half-gain PCM mutation;
5. the picture-only one-host patch is reported as a mismatch after the full
   passing baseline.

Do not remove, reorder, weaken, or replace these bodies or their picture,
audio, and half-gain controls. Zero executed bodies is FAIL, even with exit 0.

## Single blocker list

- A fresh manager grant note is still required at
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/viewing/notes/grant-discovery-readiness-1153.md`; it must name the transported 1153 packet, the unchanged 1054 stage, and the fresh marker path. No prior marker or grant may be reused.
- The farm must materialize the complete 1054 sibling source graph and the
  separate b70 helper carrier with independent regular-file inodes before
  preflight. A flat Remotion directory, missing six-file closure, shared
  node_modules, or cross-source hardlink is a refusal.
- Central preflight and the physical final gate remain unverified after the
  corrected packet. The earlier physical attempt failed before a valid export
  because SceneSurface was absent from the source closure; 1054 supplies that
  closure, but only the one authorized farm run may establish the result.

Farm results must report all blockers in one list, exact commits and trees,
exact command and result paths, case counts, failure classification, and what
was not run. Do not report readiness, parity, or qualification from this HOLD
request alone.
