# Gate6 farm transport 1210

Status: HOLD.

This is the normal-design-sync export of the already reviewed 1153
operational packet. The exported scripts are byte-for-byte copies of the
reviewed packet. They are source transport only: this worker did not execute
the runner, preflight, issuance path, browser, Runtime, socket, or physical
gate.

## Exported files

The flat files with this prefix are the complete small 1153 packet: the run,
preflight, readiness, validation, stage-audit, and supporting scripts, plus
the original reviewed checksum file. `handoff-vw-gate6-farm-1210-SHA256SUMS`
checks the flat design-sync names. The copied
`handoff-vw-gate6-farm-1210-reviewed-SHA256SUMS` retains the reviewed
manifest bytes and its original packet filenames.

The reviewed packet manifest digest is:

```text
0ee53582e55a4f9eb8464a2d7581924cf42bb5a56f3d75de362991f3e196299e
```

The issuance script is included only because the 1209 request requires the
complete eleven-file reviewed packet. It was not run. No generated
`preflight.json`, source tuple, grant, marker, or other operational JSON is
exported; none existed in this worker's output.

## Reviewed source identities carried by the 1209 request

These identities are historical inputs and must be checked with both commit
and tree before any farm execution:

| source | hub ref | commit | tree |
| --- | --- | --- | --- |
| App | `hub/timeline/app/tl/vw-m3-gate6-admission-only-reviewed-source-0914` | `0d4323913b92c4e0e3830bf14ec7f35d981475ca` | `5a1e0e85d0f336f642426b91ccf3b3f1984ebd14` |
| Agent/sdk | `hub/timeline/agent/tl/vw-m3-immutable-d0a-runtime-graph-ready` | `d0a5072bbe7b7ce9489f43aa0a81027ec400343` | `6adb4a1190dfb2874e101565f37eccd392b1ae2f` |
| Runtime server | `hub/timeline/runtime/tl/vw-m3-runtime013-current-server-compatibility` | `8f105c26e3b62f9c2683f717a9773a12bc775a8e` | `b7f456d5135cba6049980ebc43a91c7a72ab8f7e` |
| Runtime producer/client | `hub/timeline/runtime/tl/app-m3-runtime013-producer-source` | `2c4ac180c2220bdad966bc01e95ad230e99ce26a` | `7ab412cc4bcbe517efcfa806e092336390312e18` |
| Composition | `hub/timeline/composition/tl/vw-m3-agent13-pin-source-final-gate` | `5a4e9b72f1916c4da01fa370ec5fe8d46b6da8e8` | `13e375534fffd704305eced5686699d2c8c9c948` |

The exact package/browser/toolchain identities from the 1209 request remain
unchanged: Node `v20.19.4`, Remotion `4.0.509`, React and React DOM `18.3.1`,
and the named Chrome 155 executable/package hashes in that request. They are
not copied into this design export.

## External write-once transport required by the farm

Normal design sync cannot carry the following objects. The farm lead must
request them through the normal write-once transport, using the exact pins
above and preserving independent regular-file inodes:

- the complete 1054 Runtime stage: `remotion/` plus the six
  `astrid/packs/rendering/editor/live-scenes/` closure files;
- the 1054 stage metadata files: `stage-complete-runtime.sh`,
  `stage-manifest.tsv`, and `node-graph-manifest.tsv`;
- the complete Runtime `node_modules` graph and the separate reviewed b70
  pack-host helper carrier;
- the pinned App source checkout, its private dependency graph and retained
  `dist` tree;
- the public13 Composition archive and its required media/runtime inputs;
- the pinned Node, browser executable/package tree, Python environments, and
  the farm-local short temporary/socket roots.

Do not replace the complete Runtime sibling graph with a flat Remotion copy,
do not copy media or source trees into design, and do not use cross-source
hardlinks or a symlinked parent to hide shared dependencies. The stage graph
must retain the 21,455-entry closure and six independent d0 editor/live-scenes
files required by the 1209 request.

## Unexecuted path-relocation patch

The reviewed scripts retain their original machine-specific path literals.
They must not be silently edited in this export. Before any farm command, the
farm lead may apply one private, unexecuted path-binding patch to a materialized
copy only:

```text
PACKET_DIR       -> the farm's canonical real directory containing the ten
                    reviewed basenames and issue.mjs
APP              -> the exact App checkout at the reviewed commit/tree
AGENT            -> the exact Agent/sdk checkout at the reviewed commit/tree
RUNTIME          -> the exact Runtime server checkout at the reviewed commit/tree
HELPER           -> the separate b70 helper carrier
COMPOSITION      -> the exact Composition checkout at the reviewed commit/tree
STAGE_ROOT       -> the complete independently materialized 1054 stage
STAGE_METADATA   -> the directory containing the three 1054 metadata files
APP_DIST         -> the retained App dist tree
NODE/PYTHON      -> the farm's exact pinned toolchain and private environments
BROWSER          -> the pinned Chrome 155 executable
TMP/XDG_RUNTIME  -> one new mode-0700 short farm directory
```

The patch may change only those path bindings and the corresponding private
run/evidence directories. It must preserve the discovery helper, all refusal
controls, the exact five-case controller bodies, order, picture control,
audio comparison, half-gain negative, source identities, and all graph/hash
assertions. After applying it, the farm lead must write a new farm-local hash
manifest and must not claim the reviewed packet digest for rewritten files.
No path patch was applied here, and no central command is requested by this
export.

## Deferred run contract

Once the external inputs, fresh manager authorization, and farm-local path
patch are independently verified, the 1209 request permits exactly one
preflight followed by exactly one physical final-gate invocation. The
preflight must report `token-issued:false` and no marker, grant, Runtime,
helper, browser, socket, render, or case body. Only a passing preflight may
precede the physical invocation. This export does not authorize either
command.

The blockers remain: fresh manager grant note, complete independent 1054/b70
transport, and unverified central preflight and physical final gate. No
readiness, parity, or qualification claim is made here.
