# Gate6 private graph copy — graph READY, preflight HELD

## Result

The authorized byte-identical private graph copy completed successfully. The
source graph remained read-only, the destination is a real regular directory,
and the existing physical-directory/isolation guard was not changed. Graph
readiness is **READY**. Overall Gate6 preflight remains **HELD** solely for the
independent App HOME ancestry condition for `0d432391`; that condition was not
relaxed or relabeled.

No source change, consumer pin/release action, install, network, central
preflight, browser/helper, Runtime, socket, render, physical, or full-suite run
was made.

## Absolute paths and frozen identities

- App pin: `/home/user/work/wt/app-pin-0d432391`
- App HEAD/tree: `0d4323913b92c4e0e3830bf14ec7f35d981475ca` /
  `5a1e0e85d0f336f642426b91ccf3b3f1984ebd14`; tracked files clean.
- Read-only graph source: `/home/user/work/wt/app-pin-d00a6613/node_modules`
- Private graph destination: `/home/user/work/wt/app-pin-0d432391/node_modules`
- Existing manager lease:
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/viewing/notes/gate6-app-pin-0d432391.lease`
- Prior readiness report:
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-gate6-physical-graph-clone-readiness-0934/REPORT.md`
- Prior safe-recycle report:
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m4-finished-partial-environment-release-0949/REPORT.md`

## Storage and copy

- Exact required free before copy: `11,876,144,076` bytes.
- Measured immediately before copy: `11,958,218,752` bytes; margin
  `82,074,676` bytes.
- Source allocated bytes: `555,896,832`.
- Destination allocated bytes after copy: `555,896,832`.
- Final post-copy free measurement: `11,401,834,496` bytes.
- Copy command: `cp -a --reflink=never "$SOURCE"/. "$DEST"/`, after realpath
  checks and `mkdir "$DEST"` under the real App pin parent.
- No hardlinks, install, network, write-through symlink, or shared-install
  mutation was used.

## Static graph proof

- Controller `assertPhysicalPrivateGraph` passed for both roots.
- Source and destination both equal graph hash
  `8bdc44e93ce6f712f2a26fc44f1f8e904215c1785f54ed97f826a98fe0145c5b` and
  `32,393` entries.
- Both graphs contain `32,357` regular files; every regular file has
  `nlink=1`; source and destination regular-file inode sets are disjoint.
- Internal symlinks are contained in their respective graph and resolve to
  regular files; no external graph link was accepted.
- React/React DOM: `18.3.1`; Remotion, Player, Media, Layout Utils:
  `4.0.509`; tsx: `4.21.0`.
- Contained loader/tool paths passed for both graphs: `tsx/dist/loader.mjs`,
  `tsx/dist/cli.mjs`, `@playwright/test/cli.js`, Playwright package metadata,
  TypeScript `bin/tsc` and `bin/tsserver`, esbuild `bin/esbuild`, and
  `.bin/{tsx,playwright,tsc,esbuild}`.
- Node: `v20.19.4`, executable path
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-current-root-cap-three-stills-prep/node`,
  SHA-256 `43d6cf63f2a460b463eba6b19df5e9a259771c56f11b5130e04178a15bb99490`.
- Runtime graph remains `4913a37e5403c8372a283dcca8fd30c846b636abd88f59cfc572809d2fd0bd3c` /
  `21,455`; public13 remains `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738` /
  `77` regular members.

## Retained dist and ancestry

The previously proven d00 dist/build-input equality evidence was reused. The
retained dist still exists at
`/home/user/work/wt/app-pin-d00a6613/dist`; a static check found `339` regular
files and `dist/index.html` SHA-256
`aeb5d83399b453b15a8cbc67b31260cf2820f8d65770ccd458986ddd551e257b`.

The independent App HOME ancestry requirement for `0d432391` remains pending
manager/central resolution. It is not converted into graph readiness and no
guard was bypassed. The next authorized step is the existing packet's central
preflight only after that ancestry condition is resolved; physical comparison
remains downstream of preflight PASS.

## Commands and results

- `sed` of `PLAN.md`, the 0934 report/manifest/command, and the 0949 recycle
  report: PASS.
- Realpath/absence/clean-pin checks before copy: PASS.
- Exact free-space gate before copy: PASS.
- `cp -a --reflink=never` private copy: PASS.
- Node static hash/isolation/version/path probe: PASS.
- Retained dist existence/count/index hash check: PASS.
- `git -C /home/user/work/wt/app-pin-0d432391 status --short --branch`: clean;
  HEAD/tree match the frozen identities.
- No product tests were applicable because the Composition worktree was not
  changed. Central preflight, physical, browser, helper, Runtime, socket,
  render, and full suites were not run by task instruction.
