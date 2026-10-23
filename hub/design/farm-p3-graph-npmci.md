# tf-p3-graph-npmci: GO-eligible App graph via Node 20.19.4 npm ci (BLOCKED before the build)

Date: 2026-10-23. Tuple: App 2107e1870e51c650d59315f4cc1ab6af338f198c, tree a3ff3584e9b559bbb3c3a82b77be7516ed8e761c.

**Status: BLOCKED. No graph was built, no row was edited, no preflight was run, and no gate body was requested.**

The toolchain Node binary is not executable in this worker's session. Every call to it returns `This command requires approval`. The 19:39Z orchestrator allowlist (`Bash(/home/user/work/toolchain/:*)`) has not reached this sandbox yet. I did not use the system Node (v22.22.0) or any other route as a substitute.

## 1. Inputs staged from App 2107e18 (verified)

Staged with `git show 2107e1870e51c650d59315f4cc1ab6af338f198c:<path>` into the worker folder (the designated `$TMPDIR` `/tmp/w-0a07a732f9` is outside the sandbox's writable set, so the write was refused).

| File (staged path) | sha256 | Match |
|---|---|---|
| `p3graph/app/package.json` | `7c4f3edad16efe09050311635c4ad036f9a4ecbf4d29fb3f216e3d79ac7f4320` | recorded |
| `p3graph/app/package-lock.json` | `59cd66da9a223eb1ff3cf60fd06dfa5b4b376533786366bd94b74ae3d95140ba` | recorded |
| `p3graph/app/vendor/artifacts/banodoco-timeline-composition-635f4de06fda22a85fc2e4cfc764d0153a4c9f40.tgz` | `819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234` | recorded |
| `p3graph/app/scripts/patches/remotion-4.0.509-audio-resume.mjs` | `845317ae1229c741d50ce61d3fd745b22a83a78afa5d82368fa6c5d3dac82bb6` | App `postinstall` |

Staging folder: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/tf-p3-graph-npmci2/p3graph/app`. No `npm ci` was run in it.

## 2. Commands and exits

| Step | Command | Result |
|---|---|---|
| Stage inputs | `git show 2107e18:<path> > …/p3graph/app/<path>` (4 files) | exit 0 each |
| Hash inputs | `sha256sum package.json package-lock.json vendor/artifacts/*.tgz scripts/patches/*.mjs` | matches table above |
| Toolchain node version | `/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node --version` | `This command requires approval` (not run) |
| Toolchain npm version | `/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/npm --version` | `This command requires approval` (not run) |
| Private `mkdir` in `$TMPDIR` (`/tmp/w-0a07a732f9`) | `mkdir -p …` | `needs approval`, path outside working directories (not run) |

Not done, because they depend on the blocked Node 20 / npm step: the `npm ci`, the 80-member / 0.0.14 / byte-mismatch graph verification, the GRAPH edit, the preflight and wait-test.

## 3. Row body hashes (command bytes after `app <suite> `, no newline)

Measured on `$ORCH/tests/suites.conf` before any edit. The suites file was not changed.

| Row | Body hash now |
|---|---|
| 154 `ap2-P3-gate5-h6-0348` | `b40072a8b8c5b13dd71618b4e0efda6f33e33030269838b179a65829b5cdcf3b` |
| 155 `ap2-P3-gate5-h6-0348-preflight` | `20a9702ae3d3fe9e94b7feb35183510b25399a7f93bf8845a67da9302141208f` |

These equal the run4 "after" hashes. So both rows still point GRAPH at the run4 helper-built overlay `/tmp/w-79d31cf50f/tf-p3-run4/private/node_modules`, which is harness-cleaned. That graph is NOT the qualified `npm ci` graph and must not be used for GO-eligible runs.

## 4. Items for the orchestrator

1. The toolchain allowlist (`Bash(/home/user/work/toolchain/:*)`) must reach this worker's sandbox. Once it does, the remaining steps are: `npm ci` in the staging folder with `PATH=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin:$PATH` and `--cache` under the worker folder; verify node v20.19.4 and npm 10.8.2; check 80 members, version 0.0.14, no package-root generated/typescript files, and 0 byte mismatches against the archive; then edit GRAPH in rows 154 and 155 only.
2. Disk and cap: a full App `node_modules` is about 510 MB (`/home/user/work/app/node_modules`), far over the 50 MB worker-folder cap. The graph and npm cache therefore cannot live in the worker folder. The 18:45Z rule puts them in `$TMPDIR`, which this sandbox cannot write. The orchestrator must choose a location.
3. The rows still reference the run4 graph path. Re-point them only after a verified npm ci graph exists.
4. The worker's `tmpdir` marker points to `/tmp/w-0a07a732f9`, which the sandbox treats as outside its writable set. This is the same permission gap.
5. No product, test or spec file was edited. The worker worktree `/home/user/work/wt/tf-p3-graph-npmci2` (HEAD `be890a1f`) has no changes. No commit-msg was written because there is nothing to commit.
