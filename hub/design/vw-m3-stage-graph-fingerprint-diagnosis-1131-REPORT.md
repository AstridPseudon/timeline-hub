# Stage graph fingerprint diagnosis: f06d7fe9 vs original4913

## Verdict

The mismatch is an algorithm/serialization mismatch in the stage-audit packet, not graph drift.

The existing controller implementation produces `4913a37e5403c8372a283dcca8fd30c846b636abd88f59cfc572809d2fd0bd3c` for both immutable source runtime4913 and reviewed stage1054. The duplicate packet stage-audit implementation produces `f06d7fe955f936e7a6370cee1900bd4d32a5676d65a8f9a7f46f8b4ce8ec352a` for both roots because it serializes the same records in recursive `readdirSync(...).sort()` traversal order but omits the controller's final lexical sort of the complete record list.

No content, mode, symlink-target, key, or timestamp drift was found. The stage's independent copy identity is different as expected: every record has a different inode, and the known esbuild hardlink pair has `nlink=2` in source and `nlink=1` in stage. That is the reviewed intentional copy identity, not a content or link-target mismatch.

## Exact implementations and inputs

- Source root: `/home/user/work/runtimes/agent-remotion-viewing13-d0a5072b/node_modules`
- Reviewed stage root: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-storage-cleared-complete-runtime-stage-1054/owned-stage/remotion/node_modules`
- Existing controller: `/home/user/work/app/tests/e2e/timeline/viewing-parity/tab-audio.controller.mjs`, SHA-256 `f536eff2773cd1ffd87678d647b99facd01c7cfa6d649d98ae7a0b7387038c27`, `hashTree()` at lines 174-190.
- Packet stage audit: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-final-stage-metadata-path-correction-1120/packet/stage-audit.mjs`, SHA-256 `9d3b661a592f656189f5db2818a3edf64060be11428376f0b23ac14a9b2919f8`, `tree()` at lines 23-37.
- Both implementations emit `[relativePath, kind/mode, digest]` records and count 21,455 records (21,422 regular files and 33 symlinks). Only the controller sorts the complete `entries` array by relative path before JSON serialization.

## Exact result

| Root / implementation | SHA-256 | Records |
| --- | --- | ---: |
| source / packet stage-audit traversal | `f06d7fe955f936e7a6370cee1900bd4d32a5676d65a8f9a7f46f8b4ce8ec352a` | 21,455 |
| stage / packet stage-audit traversal | `f06d7fe955f936e7a6370cee1900bd4d32a5676d65a8f9a7f46f8b4ce8ec352a` | 21,455 |
| source / existing controller `hashTree` | `4913a37e5403c8372a283dcca8fd30c846b636abd88f59cfc572809d2fd0bd3c` | 21,455 |
| stage / existing controller `hashTree` | `4913a37e5403c8372a283dcca8fd30c846b636abd88f59cfc572809d2fd0bd3c` | 21,455 |

The packet's central preflight failure at `stage-audit.mjs:122` therefore compared different algorithms. The packet's actual stage result was `f06d7fe9...`; the original READY controller value was `4913a37e...`.

## Proposed correction (not applied)

Align the packet's duplicate audit with the existing controller by inserting this existing behavior after `walk(root)` and before JSON serialization:

```js
entries.sort(([left], [right]) => left < right ? -1 : left > right ? 1 : 0);
```

This is a minimal unapplied packet hunk. It does not change the controller hasher, expected value, DTO/API, stage contents, or any guard. The operational binding should continue to carry source graph `4913a37e...` separately from actual stage identity, using the already reviewed root manifest `b349c5344ec607bc32b0e4711adf317aacd984ce98d3e5a316ba726079bb37ac` and node graph manifest `0d9da325991bfed2fda247284adb37885d118a08f5f4fc655128f6b7481c04de`. Those manifest hashes must remain distinct from the controller graph hash.

## Controls

The child-spawn-free local diagnostic reproduced both algorithms, compared all records and metadata, and used a tiny worker-owned fixture for negative controls. It did not copy or modify either graph. The fixture was removed in `finally`.

- Baseline fixture controller fingerprint: `f08626c7ce18e0cd1edffd4d535996cffd346207072a2cc6fbdb1d261f75c863/2`.
- Planted changed byte: refused with `772c09ed78450079e8342565f8609cf4ee52d0a4a526e38943323d121e5c079c/2 != f08626c7.../2`.
- Planted missing file: refused with `74a2f5a488767af93e2bb4ce0fbec537cd47b25602ff33227fbb7a3498d7b051/1 != f08626c7.../2`.

The first attempt to invoke the packet's `readlink` child process locally was denied by the sandbox (`spawnSync readlink EPERM`), so the local reproduction used Node's direct `readlinkSync`; the central exact packet run independently returned the same `f06d7fe9...` result. No child-spawn-dependent local proof is claimed.

## Later validation prerequisites

1. Apply only the final-sort hunk to the packet duplicate and record its new source hash.
2. Re-run the exact stage audit against the leased stage and confirm source and stage both produce controller hash `4913a37e...` with 21,455 records.
3. Reconfirm stage root identity separately: root manifest `b349...`, node manifest `0d9...`, package lock `c4d7030bd5418d35f2246269b5aba7952d0ed69ccd0084815a0043dfbb7a4e24`, public13 hash `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738` with 77 regular tar members, and the reviewed 75,154-byte positive closure.
4. Reconfirm Node20 hash `43d6cf63f2a460b463eba6b19df5e9a259771c56f11b5130e04178a15bb99490`, source/authority/77+75 guards, and the expected source/stage root paths.
5. Only after those checks pass should a later authorized preflight be considered. No retry, integration, physical authorization, helper, browser, Runtime, server, socket, token, marker, render, or export was run here.

## Commands and results

1. `CONTROLLER=/home/user/work/app/tests/e2e/timeline/viewing-parity/tab-audio.controller.mjs /home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-stage-graph-fingerprint-diagnosis-1131/diagnose.mjs` — passed; output records the four fingerprints above, zero record-set differences, 6,831 order-position differences, the metadata counts, and both refused negative controls.
2. Central prior preflight: `bash /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-final-stage-metadata-path-correction-1120/packet/run.sh --preflight` — failed only at stage graph hash (`f06d7fe9...` actual vs `4913a37e...` expected); no helper/browser/Runtime/token/marker/physical/export activity.
3. `sha256sum /home/user/work/app/tests/e2e/timeline/viewing-parity/tab-audio.controller.mjs /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-final-stage-metadata-path-correction-1120/packet/stage-audit.mjs` — passed with the source hashes recorded above.
4. `git status --short` in the assigned composition worktree — clean; no repository files were changed.

