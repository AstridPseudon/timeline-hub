# Farm P3 run3 (tf-p3-run3): BLOCKED at the private graph; guard fixed; no preflight, no gate run

Date: 2026-10-23. Tuple: App 2107e1870e51c650d59315f4cc1ab6af338f198c, tree a3ff3584e9b559bbb3c3a82b77be7516ed8e761c. Worktree `/home/user/work/wt/tf-p3-run3` is clean at 2107e18 (no product, test or spec edits; nothing for the harness to commit).

**Status: BLOCKED.** Decision 1 (identity guard) is applied. Decision 2 (private graph rebuild) could not be executed: the sandbox gates `npm` and the Node 20 toolchain binary, and the queue has no app-graph builder. Decision 3 (preflight, then ONE gate run) was therefore not run. No test id exists for the gate. P2 was not touched.

## 1. Identity guard (decision 1): applied

Edit: `suites.conf` rows `ap2-P3-gate5-h6-0348` (line 154) and its derived `ap2-P3-gate5-h6-0348-preflight` (line 155). `replace_all` changed exactly the one guard literal in each row:

- before: `test "$(git rev-parse HEAD)" = 2107e1870e51c650d59315f4cc1ab6af338f198c && test "$(git rev-parse HEAD^{tree})" = a3ff3584e9b559bbb3c3a82b77be7516ed8e761c`
- after: `test "$(git rev-parse HEAD^)" = 2107e1870e51c650d59315f4cc1ab6af338f198c && test "$(git rev-parse HEAD^{tree})" = a3ff3584e9b559bbb3c3a82b77be7516ed8e761c`

Diff against the pre-edit backup changes only lines 154 and 155. No other byte moved.

| Item | Value |
|---|---|
| Gate row body, command bytes (after `app <suite> `, no newline), before | `f9781f1d7e17b281f7cad15397cdb74d7e82b418ee1b0e94f4aa028962fb862f` (matches packet rebound value) |
| Gate row body, after | `5ca8c17202c98c29da273f3c353402f66a2a3f72d72a85b06049b9b03b601b0a` |
| `suites.conf` sha256, before | `5ea50e65d73c5cb4cd70ffd86b2125a2c2e6fa8df5761485028e7545cb4d273a` |
| `suites.conf` sha256, after | `bfe6694db0a659b752448193e677d91aa4c8f631ead8312b3c38a32a6ec250d1` |
| Backup of pre-edit file | `.../scratchpad/p3run3/suites.conf.before` (session scratchpad) |

Earlier evidence (packet section 3, run 2) already showed `HEAD^` plus the tree check passes on the runner. The one remaining red item in that run was the private graph.

## 2. Private graph (decision 2): NOT built

Target that the row requires: `/tmp/claude-0/…/orch/workers/ap2-P3-env-final-0407/record/private/node_modules`. It does not exist on this host (checked).

Why it could not be built:

| Attempt | Result |
|---|---|
| `npm --version` (default npm), twice, plain | `This command requires approval` (sandbox gate) |
| `/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node --version` (App `.nvmrc` = 20.19.4) | `This command requires approval` |
| Default `node --version` | v22.22.0 (not the required Node 20.19.4) |
| Queue for an app graph | None. `request-*` covers checkouts, child venvs, Remotion runtimes and test runs only |

Packet option (a), the farm Remotion `node_modules`, is NOT the recipe. `/home/user/work/runtimes/agent-remotion-ap2-current-079-2a9-1743/node_modules` has `@banodoco/timeline-composition` 0.0.14 but no `@playwright` and no `tsx`. The row symlinks the whole app graph, so a full App install is required.

Recorded inputs for the rebuild, checked on the app worktree at 2107e18 (for the orchestrator or a permitted operator to run):

| Input | sha256 / size |
|---|---|
| `vendor/artifacts/banodoco-timeline-composition-635f4de06fda22a85fc2e4cfc764d0153a4c9f40.tgz` | `819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234`, 73,451 B (row guard already checks this) |
| `package.json` | `7c4f3edad16efe09050311635c4ad036f9a4ecbf4d29fb3f216e3d79ac7f4320` |
| `package-lock.json` (App lock; carries composition 0.0.14, `integrity sha512-Ajl7lyCb…`) | `59cd66da9a223eb1ff3cf60fd06dfa5b4b376533786366bd94b74ae3d95140ba` |
| `scripts/patches/remotion-4.0.509-audio-resume.mjs` (App `postinstall`) | `845317ae1229c741d50ce61d3fd745b22a83a78afa5d82368fa6c5d3dac82bb6` |

Proposed recipe (not run): stage `package.json`, `package-lock.json`, `vendor/artifacts/<tgz>` and `scripts/patches/` from 2107e18 into the `record/private/` folder, then `npm ci` there with Node 20.19.4 / npm 10.8.2 and the npm cache in the worker tmpdir. Verify with the row's own 80-member and 0.0.14 guards.

Open question for the orchestrator: packet line 25 names Remotion lock `f4fc0a32…` and `proof.lock` `236d5be9…`. Neither is the App graph lock. I used the App `package-lock.json` (`59cd66da…`) as the "recorded lock", since it is the lock that pins composition 0.0.14 by integrity. Please confirm.

## 3. Preflight and gate: NOT run

- Preflight (`ap2-P3-gate5-h6-0348-preflight`): not requested. Without the graph it would reproduce run 2 (HEAD^ passes, GRAPH guard fails), so it gives no new information.
- Gate (`integration:app ap2-P3-gate5-h6-0348 --no-cache`): not requested. Brief says ONE run only when preflight is fully green. No test id.

## 4. Diagnostic rows

Rows `ap2-P3-gate5-h6-0348-preflight-diag` (156) and `-preflight-diag2` (157) are still in `suites.conf`. I did not remove them: the removal would need a ~24 KB exact-match edit per row, and the brief allowed listing when a plain edit was not practical. Recommend deleting both once the gate is decided.

## 5. Next steps (need the orchestrator)

1. Authorize one of: (a) an operator or queue step that runs the App `npm ci` into the `record/private/` folder above (Node 20.19.4, from the staged inputs), or (b) an approved request type for an app private graph. The sandbox gate on `npm`/Node 20 is what stopped this worker.
2. Confirm the "recorded lock" (App `package-lock.json` vs the packet's Remotion/proof locks).
3. After the graph exists: run the preflight row once; if fully green, run `bin/request-test integration:app ap2-P3-gate5-h6-0348 --no-cache` once.
4. Delete the two diagnostic rows.

Note: the gate row still checks only the archive hash and the 80-member, 0.0.14 graph. The lock hash is recorded here but not checked by the row. Adding it would change the row beyond the authorized guard, so I did not.
