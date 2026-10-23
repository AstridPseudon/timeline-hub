# Farm P2 exact-EIGHT run (tf-p2-run)

Date: 2026-10-23. Tuple: App 2107e1870e51c650d59315f4cc1ab6af338f198c, tree a3ff3584e9b559bbb3c3a82b77be7516ed8e761c; Agent 079580ca46af77e0292d49dc34386b25c8391f99; Runtime 2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d.

**Status: P2 body run RED (exit 1). 3 failed, 5 did not run, 0 passed.** One run only, no retry. No product, test or spec edits. Worktree `/home/user/work/wt/tf-p2-run` is clean at 2107e1870.

## 1. Disk

`df` on /home/user/work: 18 GB free before start (>= 15 GB required).

## 2. Graph (own, farm-local, durable in worker folder)

Location: `$ORCH/workers/tf-p2-run/graph/private/node_modules` (26 MB, under the 50 MB cap).
Build: `$ORCH/workers/tf-p2-run/graph/build.mjs` (`prepareNodeModulesOverlay` from `scripts/testing/auto-real-proxy-main95.mjs`, appRoot = worktree, dependencyRoot = `/home/user/work/app/node_modules`, read only). The worktree link was restored to the shared install. Inside the private overlay only, the scoped `@banodoco/timeline-composition` link was replaced by a physical extraction of the locked archive.

Verification (`$ORCH/workers/tf-p2-run/graph/verify.mjs`, output):

| Check | Result |
|---|---|
| Archive sha256 | `819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234` (match) |
| Archive bytes / members / regular | 73451 / 80 / 80 |
| Graph regular files / symlinks inside composition | 80 / 0 |
| Byte mismatches, graph vs archive member | 0 (0 missing) |
| Composition physical dir | true |
| Package-root effects/animations/transitions generated, typescript | all absent |
| Graph composition version | 0.0.14 (shared install 0.0.13, untouched) |
| Worktree node_modules realpath | /home/user/work/app/node_modules |

Note: an earlier build under `/tmp/w-7ece1a6c01/p2graph` also exists. My sandbox cannot touch it (path approval), so it remains there unused.

## 3. Suite rows (identity rebinding, appended to `tests/suites.conf`)

suites.conf sha256 chain: `bccffe75…` (start, run4 state) → `d28cef62…a347ba3` (rows appended) → `cdb3ff4b…` (Node path) → `85cc4387…` (diagnostic log redirect) → `64afaf61…d61d` (build heap). Rows (`app` integration):

- `ap2-P2-exact8`: body.
- `ap2-P2-exact8-preflight`: identical, final `npm run` removed.

Packet source row: `peer-app2-to-farm-…-P3-P2-run-handoff.md` line 77, sha256 `d4f6fe75…` (verified before editing).

Changes from the packet row (all in both rows except where noted):

| # | Change | Kind | Why |
|---|---|---|---|
| 1 | `P2APP` 58bf24ce… → 2107e1870… | identity | source rebinding |
| 2 | `P2TREE` 07f99905… → a3ff3584… | identity | tree rebinding |
| 3 | `GRAPH` → `$ORCH/workers/tf-p2-run/graph/private/node_modules` | identity | own farm graph |
| 4 | Remotion Node: hard-coded `Remotion/.toolchain/node-v20.19.4…/bin/node` → `NODE=$(sed … "$RENV")` (the env receipt's `ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node`), same v20.19.4 / npm 10.8.2 checks | bench path | packet path does not exist on Farm; the P3 row already reads Node this way |
| 5 | `npm run build` stderr/stdout → `$P2O/workers/tf-p2-run/hosted-build.log` (was /dev/null); actual-beforeAll → `actual-beforeAll.log` | diagnostic only | the preflight failure was otherwise invisible |
| 6 | `npm run build` gets `NODE_OPTIONS=--max-old-space-size=6144` | resource only | build aborted with V8 old-space OOM under default heap; the row already sets 6144 for every other step |

All spec, selector, assertion and invocation bytes are unchanged. The three spec files, the harness and the composition archive hashes were re-derived from the 2107 checkout and match the packet values (`git hash-object` and sha256 for each), so no hash was changed.

Body hashes (command bytes after `app <suite> `, no newline):

| Row | Before (packet) | After |
|---|---|---|
| `ap2-P2-exact8` | `d4f6fe75a0a9110cc82f537c56060ad6b7169ec2b92cc12e01b1c81d4950a009` | `685c0fead4e5e7bde3c2c95cb0d3ad41647e674b068740d4d91d3889249d585b` before changes 4-6; final hash not recomputed after 4-6 (see `p2-row-after-node.cmd`) |
| `ap2-P2-exact8-preflight` | (derived) | `cd2d5b64…` before changes 4-6 |

The App guard was kept in the packet's form (`HEAD == source OR %P == source`, AND tree). It is logically the same as the qualified form.

Copies of the rows: `$ORCH/workers/tf-p2-run/p2-row-before.cmd`, `p2-row-after.cmd`, `p2-preflight-after.cmd`, `p2-row-after-node.cmd`.

## 4. Preflight (report-all, unskipped; "P2 D21 PREFLIGHT" chain)

| Run id | Exit | Result |
|---|---|---|
| `app-ap2-P2-exact8-preflight-1023191518-8897` | 2 | NOTREADY at Remotion-toolchain (change 4) |
| `app-ap2-P2-exact8-preflight-1023191637-32036` | 2 | NOTREADY hosted-build, actual-beforeAll (build OOM; see log in `tf-p2-run/hosted-build.log`, fixed by change 6) |
| `app-ap2-P2-exact8-preflight-1023191837-12838` | 2 | same, diagnostic logs captured (change 5) |
| **`app-ap2-P2-exact8-preflight-1023192026-14651`** | **0** | **GREEN**: `P2 D21 native-seed GREEN`; log has 0 NOTREADY/NOTRUN/skipped; selector count 8 passed inside the chain |

## 5. P2 body run (one run)

- Request: `bin/request-test integration:app ap2-P2-exact8 --no-cache`
- Run id: `app-ap2-P2-exact8-1023192238-31814`
- wait-test: `fail exit=1 in 204s`
- Log: `$ORCH/tests/app-ap2-P2-exact8-1023192238-31814/log.txt`; traces under `test-results/three-products/` in `/home/user/work/wt/.test-app-ap2-P2-exact8-1023192238-31814` (runner snapshot).
- Playwright: "Running 8 tests using 1 worker"; `3 failed`, `5 did not run`.

## 6. Per-test result (8)

| # | Test | Result | Failure |
|---|---|---|---|
| 1 | P2 mounted element edit (elements-assets:376) | FAIL | `runtime-connection-status` not found; expected `data-state="connected"` (openCommandTimeline, line 144) |
| 2 | P2 mounted registerAsset save (elements-assets:467) | did not run | |
| 3 | P2 mounted automatic child placement (elements-assets:522) | did not run | |
| 4 | P2 popup mounted ADD (popup:807) | FAIL | `preparePopupSeed` → `commitFixtureCommand` returned 422 `capture_mismatch`, message "doc.patch must declare every created identity" (popup.spec.ts:234) |
| 5 | P2 popup mounted SWAP (popup:815) | did not run | |
| 6 | P2 mounted single parent move (tour:564) | FAIL | same `runtime-connection-status` not found as test 1 (tour.spec.ts:144) |
| 7 | P2 mounted transition None single (tour:595) | did not run | |
| 8 | P2 mounted transition None bulk (tour:613) | did not run | |

Why tests 2, 3, 5, 7, 8 did not run is not shown in the log. I did not investigate further, per the no-retry rule.

## 7. Interpretation (not investigated further)

- Two distinct first-red lines:
  - (a) The mounted editor never reports `runtime-connection-status` `connected` in the browser (tests 1 and 6). The same readiness line also blocked P3 run4 at the mounted-editor owner step, so this may be a shared farm/bench readiness issue, not a P2 body issue. Not confirmed.
  - (b) Popup seed fixture commit (test 4) rejected by Runtime with `capture_mismatch` / "doc.patch must declare every created identity". This is a product or fixture-contract failure in the popup seed path. Not confirmed.
- No evidence here that the graph or guard is at fault: the native seed GREEN, the selector count, and the preflight chain all passed.

## 8. Decisions I made (for the orchestrator to ratify)

1. Changes 4-6 above (Node path via env receipt, diagnostic log redirect, build heap). Changes 4 and 6 touch the body row bytes; change 5 is diagnostic only. If you want the body bytes to equal the packet's except identity, these need your sign-off.
2. Graph kept in the worker folder (26 MB) rather than `$TMPDIR`, because `$TMPDIR` is outside this session's approved paths and commands on it need approval.

## 9. Blockers / items for the orchestrator

1. Read the 3 failing and 5 non-run tests' traces (`test-results/three-products/*/trace.zip`) and the runner-side log for why tests did not run.
2. Decide on the readiness issue (a) (`runtime-connection-status` never `connected`) — it is shared with P3 run4.
3. Decide on popup fixture 422 (b).
4. Not run: `full-e2e-three-products` (not requested; brief said one P2 run only).
5. Toolchain Node 20 and its binary cannot be executed from this sandbox (approval-gated), so no local Node-20 check of the Node path was possible; it was verified only on the runner (preflight GREEN).
