# Complete owned Runtime stage — READY for custody review

The complete owned stage was created after the authorized f816 recycle cleared
the storage gate. The leased root is:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-storage-cleared-complete-runtime-stage-1054/owned-stage`

It contains exactly one independent `remotion/` copy of immutable Runtime4913
and six independent frozen d0a editor/live-scenes files at:

`astrid/packs/rendering/editor/live-scenes/{SceneSurface.tsx,authoring.ts,diagnostics.ts,extension.tsx,identity.ts,runtime.ts}`

The stage is intentionally retained for the later central preflight. No launch
validation artifact was minted or copied.

## Exact identity

- stage script: `.../stage-complete-runtime.sh`
- script SHA-256: `24cc758029518075f671b06dffc75582b772f2fc52a5e4b57450b46c08a0c66c`
- full stage manifest: `.../stage-manifest.tsv`, SHA-256 `b349c5344ec607bc32b0e4711adf317aacd984ce98d3e5a316ba726079bb37ac`
- node_modules graph manifest: `.../node-graph-manifest.tsv`, SHA-256 `0d9da325991bfed2fda247284adb37885d118a08f5f4fc655128f6b7481c04de`
- actual allocated stage bytes: `405573632`
- apparent stage bytes: `341365435`
- final free bytes (last check): `11562700800`
- required post-stage minimum: `11320247244`

The 1048 measured estimate was `394166272` bytes. The actual independent copy
is larger by `11407360` bytes because the immutable source has one internal
hardlink pair (`node_modules/@esbuild/linux-x64/bin/esbuild` and
`node_modules/esbuild/bin/esbuild`). The final destination deliberately breaks
that pair: every destination regular file has `nlink=1`. The final free-space
reading remains above the exact physical minimum.

The immutable source graph identity remains the reviewed
`4913a37e5403c8372a283dcca8fd30c846b636abd88f59cfc572809d2fd0bd3c`, with
21,455 entries (21,422 regular files and 33 relative links). The independent
stage graph comparison passed all 21,455 entries/content values; its canonical
stage graph manifest hash is the value above.

Frozen input checks passed:

- `package-lock.json`: `c4d7030bd5418d35f2246269b5aba7952d0ed69ccd0084815a0043dfbb7a4e24`
- generated registries: `bf6af4fbe7e5eeef9dcc267c21728b3253544f94170871310a45661729184b88`, `b78ce0baa5a25bed3db9de377820b37f822b1651b53bfb0a9d52e19793ce8fea`, `2a2fd68e81ab0875803321051608a23493b812182a02d8674522cd25b25450a0`
- public13 artifact: `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`, exactly 77 regular tar members
- Node: `/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node`, `v20.19.4`, SHA-256 `43d6cf63f2a460b463eba6b19df5e9a259771c56f11b5130e04178a15bb99490`
- in-project CLI and frame worker are regular files with `nlink=1`; all 33 relative links resolve inside the staged `remotion/` project

All six closure files match the frozen capsule byte-for-byte; destination
inodes are distinct and `nlink=1`. The omitted-sibling negative and complete
positive source closure checks were both run with the final root context. The
positive produced a non-empty 75,154-byte pure bundle; the negative refused
four omitted local edges before bundling.

## Commands and results

1. `/tmp/.../stage-complete-runtime.sh >stage-script.stdout 2>stage-script.stderr` — PASS, exit 0. Reflink was attempted first and reported `Operation not supported`; the script rechecked the exact budget and completed with `cp -a --reflink=never --no-preserve=links`.
2. Inline custody graph audit comparing Runtime4913 to the staged `remotion/`, and capsule1028 to the six-file closure — PASS: 21,499 regular Runtime files, 33 links, all content equal; all destination regular files distinct from source and `nlink=1`.
3. `bash -n .../stage-complete-runtime.sh` — PASS.
4. `/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node .../validate-source-closure.mjs <owned-stage> positive` — PASS; d0a closure hashes and generated registry hashes matched; 75,154-byte bundle.
5. The same pure witness against a temporary final-root-derived fixture omitting the sibling closure — PASS; four expected unresolved edges and no bundle attempt.
6. `git status --short` and worktree inspection — PASS; no repository files changed and no build output/temp files were left in the worktree.

No browser, helper, Runtime server, socket, render, export, token, marker,
install, graph rebuild, or full suite was run. Central preflight must mint any
fresh launch validation against this exact leased root; this worker does not
claim that validation.

## Custody and cleanup

The stage parent and all owned write paths were checked with `realpath`; no
shared runtime, node_modules, venv, worktree, or graph path was written. The
stage script refuses to replace an existing leased root. Its only partial-copy
cleanup is the exact private root after a failed reflink probe, before the
ordinary-copy fallback. The temporary omitted-sibling fixture was removed
with depth-first deletion after the negative check. Do not delete or rerun the
stage script while the later preflight lease is active.
