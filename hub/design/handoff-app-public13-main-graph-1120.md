# App public13 main dependency-graph transport

Status: READY for main-owned extraction after byte checks. This is transport only: no App source, package metadata, install, build, test, browser, or shared-install change was made.

## Source and existing qualification

- Read-only source graph: `/home/user/work/app-m3-private13-normal-lock-install-units-r6-owned/node_modules`
- Existing qualifier: `/home/user/work/app-m3-private13-normal-lock-install-units-r6-owned/READY` and the graph-builder report for `app-m3-private13-normal-lock-install-units-r6`.
- Source App commit/tree recorded by the qualifier: `808ef7ebf8b48d16cc0007a23b6877d62b90f63e` / `d6f1e417379f59c41747b61adab51de4c370f8e6`.
- Source `package.json` SHA-256: `a4dc9fcc02b1769ba8472f551349f7875774b07ad0830c7260eb88d2db8292fd`.
- Source `package-lock.json` SHA-256: `7f1bfcea48cef38d4c6f1163aa34190b8d5e71c9f08c7378e01a962d6696fc14`.
- Source `node_modules/.package-lock.json` SHA-256: `4a0b613e7dc615aadd6c6fcc6152ee9113f4f2450335c8ffabc1b272ca32dcaf`.
- Official Composition C13 artifact: `ORCH/artifacts/banodoco-timeline-composition-0.0.13.tgz`, SHA-256 `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`, exactly 77 regular members. The source installed C13 package and the transported package both match all 77 official members byte-for-byte.
- Existing qualifier identities: React/React DOM `18.3.1`; Vite `5.4.21`; Remotion, `@remotion/media`, `@remotion/player`, and `@remotion/web-renderer` `4.0.509`; Playwright, `@playwright/test`, and `playwright-core` `1.60.0`.
- Existing qualifier browser evidence: central environment-smoke result `app-m3-private13-normal-lock-install-units-r6-e2e-environment-smoke-private13-normal-r6-tree-d6f1e417-graph-r6-chrome141-e2e-integration-1021014246-28404`, exit 0; Chromium `141.0.7390.37`. This worker did not relaunch it.

The normal npm source install has 86 npm-owned symlinks (`.bin`, scope self-links, and the legitimate `vendor/` lockfile package links) and retains its `.vite` cache. It was not modified. The transport archive is the physical/symlink-free form: `.vite` is excluded as cache, scope self-link aliases are excluded because dereferencing them recursively aliases their containing scope, and all usable package contents are dereferenced into regular files. This is archive normalization, not a new install or graph repair.

## Transport artifact

- Archive: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/artifacts/app-public13-main-node-modules-r25.tgz`
- SHA-256 sidecar: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/artifacts/app-public13-main-node-modules-r25.tgz.sha256`
- Compressed size: `130648897` bytes.
- Unpacked payload: `466661105` regular-file bytes; 35,496 total archive members, 3,147 directories, 32,349 regular files, zero symlinks and zero hardlinks.
- Archive SHA-256: `a1ef11b292548c22caa36cc38c683a67b01d9244f8389aade9405e5a7dca581e`.
- Archive member root: `node_modules/`.
- Safety audit: all paths are relative and under `node_modules/`; no `..` or absolute paths; no `.vite`, `.cache`, `.npm`, `.aws`, `.config`, `realm`, `credentials`, or `credential` path components.
- The archive was created with deterministic tar metadata, symlink and hardlink dereferencing, `node_modules/.vite` exclusion, and `node_modules/@*/@*` scope-self-link exclusion. The first recursive attempt was quarantined in the worker-owned temp directory and is not a transport artifact.

## Safe extraction for main

Use a new main-owned directory, after verifying the sidecar and archive safety above; do not extract over a shared install:

```sh
archive=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/artifacts/app-public13-main-node-modules-r25.tgz
target=/home/user/work/app-public13-main-node_modules-r25
sha256sum -c "$archive.sha256"
test ! -e "$target"
mkdir "$target"
tar --extract --gzip --file="$archive" --directory="$target" --no-same-owner --no-same-permissions --no-overwrite-dir --keep-old-files
test -d "$target/node_modules"
test "$(find "$target/node_modules" -type l | wc -l)" -eq 0
```

The extracted package root is therefore `$target/node_modules`; main can attach or replace only its own install after independently checking package and peer bytes. No extraction was performed by this worker.

## Peer manifest identities

The following source manifests were read-only checked; the archive contains the same bytes for these package files:

| package | version | manifest SHA-256 |
|---|---:|---|
| `@banodoco/timeline-composition` | `0.0.13` | `7c806b078b00bba1593336c49a3d2953b3f8f7afc7fa9919f6d5d7ccc7c1aa61` |
| `react` | `18.3.1` | `d4e68a5c96babb20cad1daafea8b78822eae45b341552cf5418d06a5304fa64c` |
| `react-dom` | `18.3.1` | `d2f29e31bd48b833e48cd7bbf41f192e8ee4ff8da249fdbe10d4ac4114b8b12e` |
| `remotion` | `4.0.509` | `1260b76eb109b0ebfff6cfb57f0e2b9b5fc8c6511f18bd43b047bddca068bd01` |
| `@remotion/layout-utils` | `4.0.509` | `244521ec2c97085930463bd476366cdf7f6392793a57d787b6f0576dbdeaafda` |
| `@remotion/media` | `4.0.509` | `59e90c2e2d182faf420dd8b9461a74bedd21d6680a627ea6f2fb66c4efb9ee95` |
| `@remotion/player` | `4.0.509` | `89595cb2ec1e0231f576cf32408e81aa3dab522ebe0c2154dc4adb41746f7abf` |
| `@remotion/web-renderer` | `4.0.509` | `368fad52ef17b18579b53f76fb1fd5c60206425321b8fb7cdbd06bb7b3cedcd9` |
| `@remotion/three` | `4.0.509` | `a2805901e7cd3a1675e572c344f07c58837ed89701b21b796b35b7cb8aed2e3e` |
| `playwright` | `1.60.0` | `8be9edc5642a8c761b677e7af8b9937f36c0443a91e14765877716d70034e5bf` |
| `playwright-core` | `1.60.0` | `6f7b58cc55449321279f11ca97d4e451c391738b77db32cdbcedf02851e3f097` |
| `@playwright/test` | `1.60.0` | `cf92117ef1d8cbf1e4b2dffb63a0da552c0173bd6052f0f45711c0f00b79dc99` |

Composition C13 declares exact peers: `@remotion/layout-utils`, `@remotion/media`, and `remotion` `4.0.509`; `react` and `react-dom` `18.3.1`.

## Checks performed here

- Disk guard before final creation: `12000165888` bytes available; after final creation: `10898759680` bytes; final postflight: `11221245952` bytes.
- Read-only C13 comparison: official 77/77 and final archive embedded 77/77 equal.
- Final archive `sha256sum -c`: PASS.
- Final archive safety audit: PASS; zero links and no forbidden path components.
- Source postflight package/lock/Composition hashes: unchanged and match the qualified identities; source still has the expected 86 npm symlinks and `.vite` cache.
- No install, copy/extraction, build, test, browser, network, shared dependency mutation, protected deletion, or worktree product change.
