# Final staged Runtime attachment custody review

## Verdict

**APPROVED for the single subsequent central preflight only.** This is a
process-custody approval of the retained stage, not a physical, launch,
browser, render, marker, or qualification grant. The central preflight must
mint fresh normal validation bound to the exact root below; no foreign or
copied validation artifact was accepted.

## Exact retained identity

- Root: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-storage-cleared-complete-runtime-stage-1054/owned-stage`
- Stage script SHA-256: `24cc758029518075f671b06dffc75582b772f2fc52a5e4b57450b46c08a0c66c`
- Root manifest SHA-256: `b349c5344ec607bc32b0e4711adf317aacd984ce98d3e5a316ba726079bb37ac`
- Final node graph manifest SHA-256: `0d9da325991bfed2fda247284adb37885d118a08f5f4fc655128f6b7481c04de`
- Immutable source graph SHA-256: `4913a37e5403c8372a283dcca8fd30c846b636abd88f59cfc572809d2fd0bd3c`
- Graph: 21,455 entries, 21,422 regular files, 33 relative links
- Public13 artifact: `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`, 77 regular tar members
- Package lock: `c4d7030bd5418d35f2246269b5aba7952d0ed69ccd0084815a0043dfbb7a4e24`
- Generated sources: `effects.generated.ts` `bf6af4fbe7e5eeef9dcc267c21728b3253544f94170871310a45661729184b88`; `animations.generated.ts` `b78ce0baa5a25bed3db9de377820b37f822b1651b53bfb0a9d52e19793ce8fea`; `transitions.generated.ts` `2a2fd68e81ab0875803321051608a23493b812182a02d8674522cd25b25450a0`
- Node: `/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node`, v20.19.4, SHA-256 `43d6cf63f2a460b463eba6b19df5e9a259771c56f11b5130e04178a15bb99490`

## Independent controls

Passed independently:

- Current root and all write-target ancestors are real directories with
  `realpath` identity; stage and source ownership are uniformly `root:root`.
- Current stage manifest still matches modes, sizes, inodes, link counts,
  symlink targets, and content hashes: 21,499 Runtime regular files, 33
  Runtime links, 1,569 Runtime directories, and six closure files.
- Every staged regular destination has an inode distinct from its source and
  `nlink=1`; all six frozen closure files also have distinct inodes and
  `nlink=1`. The 33 relative links, including legitimate `.bin` links, resolve
  strictly inside the staged `remotion/` project.
- The in-project Remotion CLI and `src/astrid-frame-worker.mjs` are regular
  files with `nlink=1` and remain inside the staged project.
- Package lock, all three generated registry inputs, public13/77, stage
  script, root manifest, graph manifest, and source graph hashes match the
  published identities above.
- Positive final-root source closure passed with a non-empty 75,154-byte pure
  bundle. A final-root-derived fixture with the six sibling closure omitted
  refused before bundling with exactly four unresolved local edges.
- `bash -n` passed for the stage script. Its `set -euo pipefail`, exact
  storage guards, realpath checks, reflink fallback, no-preserve-links copy,
  and private-root-only cleanup were present. No partial omitted-sibling
  fixture or review temporary remained.

The immutable source contains one expected internal hardlink pair:
`node_modules/@esbuild/linux-x64/bin/esbuild` and
`node_modules/esbuild/bin/esbuild` have source `nlink=2`. The staged copies
break that pair and are both `nlink=1`; no staged destination shares an inode
with the source. This is the only source-side link-count exception.

## Exact commands and results

```text
python3 <inline custody audit>                         PASS
bash -n <stage>/stage-complete-runtime.sh              PASS
node-v20.19.4 validate-source-closure.mjs <root> positive PASS (75154 bytes)
node-v20.19.4 validate-source-closure.mjs <derived fixture> negative PASS (4 unresolved)
git diff --check                                        PASS
git status --short --branch                             clean
```

No repository test suite was relevant or run. No helper, Runtime server,
browser, socket, render, export, install, graph copy, full suite, or local
launch validation was run. The later central preflight is the required fresh
normal validation and must bind this exact root, script, source graph, and
node graph identity.
