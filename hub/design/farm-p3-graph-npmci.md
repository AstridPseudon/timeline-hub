# Farm P3 graph via Node 20 npm ci (tf-p3-graph-npmci): BLOCKED at npm ci; no graph, no row edit, no preflight, no gate

Date: 2026-10-23. Tuple: App 2107e1870e51c650d59315f4cc1ab6af338f198c, tree a3ff3584e9b559bbb3c3a82b77be7516ed8e761c. Worktree `/home/user/work/wt/tf-p3-graph-npmci` is clean at 2107e18 (no product, test or spec edits; no commit-msg written because there is nothing to commit).

**Status: BLOCKED.** The sandbox refused the authorized toolchain `npm ci` (`/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/npm`). Steps 2 to 4 were not run. The P3 gate body was not requested.

## 1. Why it is blocked

The orchestrator's 19:39Z item says `Bash(/home/user/work/toolchain/:*)` is allowed. The kit file `orch/bin/claude-perms.sh` (line 15) does contain that entry. My session does not have it. The orchestrator also wrote that it "arrives with the next hub sync; fresh workers get it". This worker started before that sync, so the permission is not active here. I did not try any alternate route (no plain `npm` on PATH, which would run under Node 22, no `sh -c` or interpreter wrapper, no symlink).

| # | Command | Result |
|---|---|---|
| 1 | `/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node --version` | `This command requires approval` (refused, did not run) |
| 2 | `/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/npm ci --version` | `This command requires approval` (refused, did not run) |
| 3 | `PATH=<toolchain bin>:$PATH <toolchain npm> ci --cache <scratch>` (in the staged folder) | Rejected before running: `A variable in this command can't be checked before it runs` |
| 4 | Same `npm ci` as a second attempt with the plain full path | Not run; the path itself is the refused prefix, so I stopped |

No `npm ci` ran, so there is no node_modules, no npm version and no Node 20 version output to record.

## 2. Inputs staged and hash-checked (step 1 partial)

Staged in the session scratchpad, not in the worker folder: `/tmp/w-b7b4d71d70/claude-0/-home-user-work-wt-tf-p3-graph-npmci/388ca6ba-dd93-49ba-b1cb-f46174da6963/scratchpad/p3graph/private/` (package.json, package-lock.json, `vendor/artifacts/<tgz>`, `scripts/patches/remotion-4.0.509-audio-resume.mjs`). The npm cache was not created. A `mkdir` under `/tmp/w-b7b4d71d70/tf-p3-graph-npmci` was refused as outside the session's directories, so I used the scratchpad path.

| Input (App worktree at 2107e18) | sha256 | Expected | Match |
|---|---|---|---|
| `package.json` | `7c4f3edad16efe09050311635c4ad036f9a4ecbf4d29fb3f216e3d79ac7f4320` | 7c4f3eda…4320 | yes |
| `package-lock.json` | `59cd66da9a223eb1ff3cf60fd06dfa5b4b376533786366bd94b74ae3d95140ba` | 59cd66da…5140ba | yes |
| `vendor/artifacts/banodoco-timeline-composition-635f4de06fda22a85fc2e4cfc764d0153a4c9f40.tgz` | `819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234` | 819acf6b…2040234 | yes |
| `scripts/patches/remotion-4.0.509-audio-resume.mjs` | `845317ae1229c741d50ce61d3fd745b22a83a78afa5d82368fa6c5d3dac82bb6` | (App postinstall) | recorded |

Commands run: `sha256sum` on the four worktree files (exit 0), `cp` of the four files into the staging folder (exit 0). Not yet verified: the 80 members, version 0.0.14, and 0 byte mismatches. They need the built graph.

Node/npm versions: not recorded (toolchain refused). The pinned target is Node 20.19.4 / npm 10.8.2.

## 3. Row state (step 2 not done)

Rows 154 (`ap2-P3-gate5-h6-0348`) and 155 (`…-preflight`) were not edited, because there is no toolchain graph to point at. Current state, read only:

| Item | Value |
|---|---|
| `suites.conf` sha256 now | `64afaf615665def79f3660d771f17e226c83fa58223417f5dd11d8cc6227d61d` (differs from run4's `bccffe75…`; I did not edit it, so someone changed it after run4) |
| Row 154 body hash (command bytes after `app <suite> `, no newline), before = after | `b40072a8b8c5b13dd71618b4e0efda6f33e33030269838b179a65829b5cdcf3b` |
| Row 155 body hash, before = after | `20a9702ae3d3fe9e94b7feb35183510b25399a7f93bf8845a67da9302141208f` |
| Row 154/155 GRAPH | `/tmp/w-79d31cf50f/tf-p3-run4/private/node_modules` (run4's helper-built graph, which the orchestrator says is NOT GO-eligible) |

Row 156 still points at the 0407 path, and rows 158 and 159 at tf-p2-run. These are diagnostic or P2 rows and were not touched.

## 4. Preflight and gate: NOT run

- Preflight `ap2-P3-gate5-h6-0348-preflight`: not requested. With the run4 helper graph it would give no GO-eligible evidence.
- Gate body `ap2-P3-gate5-h6-0348`: not requested (as instructed; the manager decides after the 15659 investigation).

## 5. What is needed to unblock

1. Activate `Bash(/home/user/work/toolchain/:*)` for this session (the hub sync, or a fresh worker), or have an operator run the build with the staged inputs.
2. Build recipe, once allowed: in the staging folder, `PATH=<toolchain bin>:$PATH <toolchain npm> ci --cache <scratch npm-cache>`, then record `node --version`, `npm --version`, the three hashes above, and the graph path. Then verify the 80 members, 0.0.14, no package-root generated/typescript files, and 0 byte mismatches against the archive (the run4 `verify-graph.mjs` checks are the reference).
3. Edit GRAPH in rows 154 and 155 to the new path (harness-only, keep the qualified guard form), record body hashes before and after, run the preflight once, then stop.

Observation for the orchestrator: the built graph will live in TMPDIR or the scratchpad, not the worker folder. At ~hundreds of MB it cannot meet the 50 MB worker-folder cap, so it is not durable across harness cleanup. Its path and hashes should go in the preflight record.
