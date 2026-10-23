# Farm P3 bench2 (STEP A, ap2-P3-gate5-h6-0348): provisioned, rebound, preflight RED, gate NOT run

Worker: tf-p3-bench2. Date: 2026-10-23, 18:28Z to 18:38Z. Tuple: App 2107e1870e51c650d59315f4cc1ab6af338f198c tree a3ff3584e9b559bbb3c3a82b77be7516ed8e761c; Agent 079580ca46af77e0292d49dc34386b25c8391f99; Runtime 2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d; frozen producer 34eac0041b0891e9011966b39bcbd26053fde5bc.

**Status: BLOCKED.** Provisioning is green. The P3 row is rebound. The preflight is red, so the single gate run was NOT requested. No test id for the gate exists. P2 was not touched.

## 1. Provisioning (all via dispatcher; no refusal from the approval gate)

| Request | Result |
|---|---|
| `bin/request-checkout agent 079580ca...` | `created /home/user/work/wt/agt-pin-079580ca (detached, KEEP)` |
| `bin/request-checkout runtime 2a9e347f...` | `created /home/user/work/wt/rt-pin-2a9e347f (detached, KEEP)` |
| `bin/request-checkout runtime 34eac004...` | `created /home/user/work/wt/rt-pin-34eac004 (detached, KEEP)` |
| `bin/request-child-venv venv-agent-child-ap2-current-079-2a9-1743 079580ca...` | `status passed`, `created /home/user/work/venv-agent-child-ap2-current-079-2a9-1743 (astrid 079580ca, runtime 2a9e347f, 92 pins, read-only)`, 18:28:54Z to 18:29:46Z |
| `bin/request-runtime agent-remotion-ap2-current-079-2a9-1743 079580ca... f4fc0a32... /home/user/work/wt/agt-pin-079580ca /home/user/work/wt/rt-pin-2a9e347f 2a9e347f...` | `created /home/user/work/runtimes/agent-remotion-ap2-current-079-2a9-1743 (lock f4fc0a32..., node v20.19.4 / npm 10.8.2)`, `suite agent-remotion-ap2-current-079-2a9-1743-nodes` |

Exit codes of the request scripts were not captured. Each printed `queued`, and each receipt above is in `queue/done`.

## 2. Rebind (identity tokens only; invocation tail byte-identical)

Source row: packet line 85 (`peer-app2-to-farm-20261023T1756-P3-P2-run-handoff.md`). Working copies are in my scratchpad `p3/`, namely `orig.cmd` and `rebound.cmd`.

| Item | Before | After | Count |
|---|---|---|---|
| Body (row bytes) sha256 | `4add5c804c48edfc2c9c4555f71f69b1ad2d08e755f64735c30ac15fdd79b17b` (23991 B) | `f9781f1d7e17b281f7cad15397cdb74d7e82b418ee1b0e94f4aa028962fb862f` (23976 B) | |
| `P3APP` and final HEAD guard | `58bf24ce6fc57c7477a7fa45d94b20dfb12c5e92` | `2107e1870e51c650d59315f4cc1ab6af338f198c` | 2 |
| `P3TREE` and final tree guard | `07f99905cb822656a2d3675a782b72e6c1fb5ecb` | `a3ff3584e9b559bbb3c3a82b77be7516ed8e761c` | 2 |
| `useTimelineSave.test.tsx` sha256 | `a6e27017...` | `bd6adf9ad6b2cd9fcde594a41120e10d4c5c249274186b89a004b41d5a37af82` (re-derived at 2107) | 2 |
| `three-products.p1-chain.spec.ts` sha256 | `a2188d7fc8c3a7228f7d46ffc54a6da30cf27aabdb2c65c73df86f97890231a4` | `074ecd9e6408218633bc6a997e509459f2034321a655d1555de38dc8f37cdca3` (re-derived at 2107) | 1 |
| Diagnostics folder | `ap2-P3-OPS-quoting-sol-1426` | `tf-p3-bench2` | 1 |

Notes:
- The `p1-chain.spec.ts` guard was not in the earlier draft. It changed between 58bf and 2107 because the collector (10390) touches P1 files. Its new hash was re-derived from my 2107 checkout.
- The earlier draft (`rebind.py`) is in a folder my sandbox cannot read, so I rebuilt the rebind from the packet row. The identity-token table above matches the earlier worker's table, plus the extra `p1-chain` guard.
- Unchanged, and re-verified at 2107: the Gate-5 body (git blob `37caf285...`, sha256 `0e69b561...`), `harness.ts` blob `3455a5eb...`, `astrid.ts` sha256 `02a42eb2...`, the composition archive `819acf6b...`, the ancestry checks, and the rest of the guard list. The app delta 58bf→2107 is four files: `useTimelineSave.test.tsx`, `p1-chain.spec.ts`, `p1-diagnostic-safety.ts`, `p1-diagnostic-safety.test.ts`. Only the first two are in the P3 guard list.
- `suites.conf` (`orch/tests/`): sha256 before `c756b0fe...`, after the row was appended `c894c165...`. Two more rows were appended afterwards (diag and diag2, below), so the current hash differs.

Registered rows in `suites.conf` for `app`:
- `ap2-P3-gate5-h6-0348`: the rebound row. **Not requested. Gate not run.**
- `ap2-P3-gate5-h6-0348-preflight`: the row with the final `npm run` removed. Used for run 1 below.
- `ap2-P3-gate5-h6-0348-preflight-diag`: run 2 below. Only the final HEAD guard is changed, to `HEAD^`.
- `ap2-P3-gate5-h6-0348-preflight-diag2`: run 3 below. Additionally skips the private GRAPH mount and the 80-file guard.

The two `diag` rows are not the gate row and are not evidence of green. I suggest removing them after the decision in section 5.

## 3. Preflight on the runner (report-all `P3_ENV` block plus fail-fast chain)

| Run | Suite | Test id | Exit | Result |
|---|---|---|---|---|
| 1 | `ap2-P3-gate5-h6-0348-preflight` | `app-ap2-P3-gate5-h6-0348-preflight-1023183150-3794` | 1 | `P3_ENV` report-all: no `P3FAIL`. global-setup, actual beforeAll, and the full native seed (trivialboot) all GREEN. The chain then failed at the first post-`P3_ENV` guard, `test "$(git rev-parse HEAD)" = 2107e187...`. |
| 2 | `ap2-P3-gate5-h6-0348-preflight-diag` | `app-ap2-P3-gate5-h6-0348-preflight-diag-1023183451-29449` | 1 | Same as run 1 up to the chain. The `HEAD^` guard passed. Then `realpath: .../node_modules: No such file or directory` after `ln -s <GRAPH>`, so the private graph is absent. |
| 3 | `ap2-P3-gate5-h6-0348-preflight-diag2` | `app-ap2-P3-gate5-h6-0348-preflight-diag2-1023183732-30416` | 0 | Diagnostic only: `DIAG ONLY: private GRAPH mount and 80-file guard skipped`. Then `vendor-lock check runtime.lock.json` (matches pinned producer), the import provenance check, the `runtimePython` / harness check, and the `astrid` / `astrid.sdk` import all passed. `P3 D21 PREFLIGHT GREEN; body not run`. |

### Failure list (every failure found)

1. **Snapshot HEAD guard (structural).** `test-run` builds a synthetic snapshot commit (`git commit-tree <tree> -p HEAD`) and runs the row inside it. So `git rev-parse HEAD` in the row is never `2107e187`; the parent is. The row's final HEAD guard can never pass on the runner. `P3_ENV` already handles this with the parent form, which is why it passed.
2. **Private graph absent.** `GRAPH=/tmp/claude-0/.../workers/ap2-P3-env-final-0407/record/private/node_modules` does not exist on Farm (verified by Glob). The 80-file guard and `ln -s` mount fail. This is open item 4.1 in the packet.
3. **Not reached.** The fail-fast chain stopped at item 1 in run 1 and item 2 in run 2. Items after the GRAPH segment were checked only in run 3, where they passed.

## 4. Gate run

Not requested. The preflight is not green, and the brief says to run only when it is fully green. No retry. No `integration:app ap2-P3-gate5-h6-0348` test id exists.

## 5. Decisions needed from the orchestrator

1. **Final HEAD guard in the P3 row.** Under the farm snapshot the row must use the parent form, e.g. `test "$(git rev-parse HEAD^)" = 2107e187...`, which `P3_ENV` already enforces with the tree check. The current row's `HEAD` check cannot pass on the runner. This changes a protected row beyond identity tokens, so I did not change it.
2. **Private graph (packet 4.1).** Choose (a) point `GRAPH` at the Farm Remotion runtime `node_modules` (`/home/user/work/runtimes/agent-remotion-ap2-current-079-2a9-1743/node_modules`) and let the row's 80-file guard judge, or (b) name a Farm-local graph source. I did not hand-build a graph or change the path.
3. **Diagnostic rows.** Keep or remove `...-preflight`, `...-preflight-diag`, `...-preflight-diag2`.

Once 1 and 2 are decided, a fresh preflight is needed, then the ONE gate run. Per the brief, I stop here and do not request it.

## 6. Other observations

- `test-run` logged `tests/cache/<key>: No such file or directory` after each run. The cache dir seems missing. This did not change any result here, but it may matter for cache writes.
- The fail-fast chain makes "report-all" true only inside `P3_ENV`. The trailing chain reports only its first failure.
- Diagnostic folders were created under `workers/tf-p3-bench2/p3-preflight.*`. Nothing was written into the worktree. `/home/user/work/wt/tf-p3-bench2` is clean at 2107e187.
