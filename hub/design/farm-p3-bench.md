# Farm P3 bench provisioning and OPS validation (STEP A), tf-p3-bench

Status: **BLOCKED at provisioning.** No bench exists, the preflight has not run on the runner, and no P3 run was requested. No test id exists.

Date: 2026-10-23 (about 18:02-18:10Z). Packet: `peer-app2-to-farm-20261023T1756-P3-P2-run-handoff.md`.

## 1. Blocker: provisioning requests refused by the approval gate

Four dispatcher requests were refused. The harness returned `This command requires approval` for each. I did not retry, did not use a different wrapper, and did not write queue files by hand.

| # | Command | Result |
|---|---|---|
| 1 | `bin/request-checkout agent 079580ca46af77e0292d49dc34386b25c8391f99 "..."` | refused (approval gate) |
| 2 | `bin/request-checkout runtime 2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d "..."` | refused (approval gate) |
| 3 | `bin/request-checkout runtime 34eac0041b0891e9011966b39bcbd26053fde5bc "..."` (frozen producer, for the row's `vendor-lock check --producer .../rt-pin-34eac004` step; not in the brief's list) | refused (approval gate) |
| 4 | `bin/request-child-venv venv-agent-child-ap2-current-079-2a9-1743 079580ca46af77e0292d49dc34386b25c8391f99` | refused (approval gate) |

Not attempted, because they depend on the checkouts: `bin/request-runtime agent-remotion-ap2-current-079-2a9-1743 079580ca... f4fc0a32... /home/user/work/wt/agt-pin-079580ca /home/user/work/wt/rt-pin-2a9e347f 2a9e347f...` (6-argument exact-source form; the legacy 2-3 argument form fails the runtime identity check).

Dispatcher is alive (heartbeat 2026-10-23T18:02:46Z), so the gate is the cause, not the service.

Benches that the row needs, all absent (checked with `ls -d`): `/home/user/work/venv-agent-child-ap2-current-079-2a9-1743`, `/home/user/work/runtimes/agent-remotion-ap2-current-079-2a9-1743`, `/home/user/work/wt/agt-pin-079580ca`, `/home/user/work/wt/rt-pin-2a9e347f`, `/home/user/work/wt/rt-pin-34eac004`. No CHECKOUT, CHILDVENV or RUNTIME receipts exist in `queue/done`.

## 2. Verified read-only (passed)

| Check | Result |
|---|---|
| App integration `/home/user/work/app` HEAD | `3a0d76503a11451f91a5c9b18f9fcb74d009b247`, tree `7bb0c9171d85d5c14b4e5dd9cf8bfb708253b36b`, clean |
| Agent `/home/user/work/agent` HEAD | `079580ca46af77e0292d49dc34386b25c8391f99` (packet tree `2deab1a1...`) |
| Runtime `/home/user/work/runtime` HEAD | `2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d` (child venv takes its runtime from this HEAD, so it matches) |
| `079580ca:remotion/package-lock.json` sha256 | `f4fc0a32a8822e956dfa21ff35d19c0c83d147c754cdb3546f91c84e330be18d` (matches) |
| `079580ca:requirements/proof.lock` sha256 | `236d5be9894de96ce0483894630d54ee28f65107cd44ebe845940bc68c28c778` (matches) |
| Producer commit `34eac0041b08...` in runtime repo | present |
| `make-runtime` approved template `agent-remotion-0013-nodes` row sha256 / env sha256 | `9f7d51ce...` / `e03e1772...` (both match, so the registration gate will pass) |
| Free disk on `/home/user/work` | 20.7 GB (threshold 2 GiB) |
| Packet P3 command line sha256 (packet line 85, no trailing newline) | `4add5c804c48edfc2c9c4555f71f69b1ad2d08e755f64735c30ac15fdd79b17b`, 23991 bytes (matches the packet) |
| Gate-5 body `tests/e2e/local/three-products.spec.ts` | git blob `37caf28577d42fbe98afd2320dffa3c72e6e74b1`, sha256 `0e69b561a0c750669f45e54259021179b355bde41a52e265b7ea198be7318f14` (match) |
| `tests/e2e/local/support/harness.ts` | git blob `3455a5ebcff5666081745ba90723465d6b656e9f` (match) |
| `tests/e2e/local/support/astrid.ts` | sha256 `02a42eb29b122599301b04a26360ad9676f09dcf4e3fa81d21f898aeb379710e` (match) |
| App change 58bf24ce to 3a0d76503 | only `src/tools/video-editor/hooks/useTimelineSave.test.tsx`, +216 / -0 (pure addition). 58bf and 8770aa16 are ancestors of 3a0d. |

## 3. Rebinding draft (not applied to suites.conf)

The draft is in `/tmp/w-2511b51c19/claude-0/-home-user-work-wt-tf-p3-bench/82430bfd-ae47-4c5f-8782-3354aa2524ec/scratchpad/`: `ap2-P3-gate5-h6-0348.orig.cmd` and `ap2-P3-gate5-h6-0348.rebound.cmd`. The script is `rebind.py` in the same folder. `workers/tf-p3-bench/tmpdir` is a pointer file to that scratch folder, not a directory.

| Change | Count | Why |
|---|---|---|
| `P3APP` 58bf24ce to 3a0d76503a11 | 1 | App identity |
| `P3TREE` 07f99905 to 7bb0c9171d85 | 1 | App tree identity |
| final `git rev-parse HEAD` / `HEAD^{tree}` guards | 1 each | App identity |
| `useTimelineSave.test.tsx` sha256 a6e27017 to bd6adf9a | 2 | required exact source guard; the only App file changed |
| diagnostics `ap2-P3-OPS-quoting-sol-1426` to `tf-p3-bench` | 1 | the Proof worker folder does not exist on Farm |

- Body hash, before: `4add5c804c48edfc2c9c4555f71f69b1ad2d08e755f64735c30ac15fdd79b17b` (23991 bytes).
- Body hash, after: `0904e4c2ec2ad054ffcee708e5fc8548e73a3be4135256dce6e9fe5374053c99` (23975 bytes). The bytes differ only in identity tokens. The invocation tail (`npm run test:e2e:three-products -- --grep ...`) is byte-identical. The protected test body is unchanged: spec blob `37caf285...`, sha256 `0e69b561...`.
- `suites.conf` has no `ap2-P3-gate5-h6-0348` row yet. Only `app full-e2e-three-products` exists. I did not append the row, because the rebind has an open item (section 4).

## 4. Open items needing an orchestrator decision

1. **Private graph path.** The row's final chain requires `GRAPH=/tmp/.../workers/ap2-P3-env-final-0407/record/private/node_modules` (80 files in `@banodoco/timeline-composition`, version 0.0.14, no generated or typescript files). This path does not exist on Farm (3 occurrences in the row). I did not hand-build it. Options: (a) point it at the Farm Remotion runtime `node_modules` once `request-runtime` builds it, and let the row's own 80-file guard judge; or (b) name a Farm-local graph source.
2. **Preflight-only row.** The `P3_ENV` block is the report-all preflight. Running the whole row would spend the single gate run even on a red preflight. I planned a preflight-only suite that uses the same `P3_ENV` bytes with no body. This adds a suite row, so it needs approval.
3. **Permission for the four queue requests** (section 1).

## 5. Preflight list

Not run on the runner (blocked before any runner work). No failures can be listed yet. The P3 preflight list will be the `P3FAIL` string from the `P3_ENV` block.

## 6. Next steps once unblocked

1. Queue the four requests (section 1). Wait for the checkout receipts in `queue/done`.
2. Queue `request-runtime` in the 6-argument form.
3. Decide item 4.1 and item 4.2.
4. Append the rebound row to `suites.conf`, plus the preflight-only row if approved.
5. Run the preflight on the runner once. Record every `P3FAIL` entry. Request the single `integration:app ap2-P3-gate5-h6-0348 --no-cache` run only if the preflight is fully green.

## 7. Not touched

No product, test or spec file was edited. P2 was not touched. No commit (no changes in the worktree). `/home/user/work/wt/tf-p3-bench` is clean at 3a0d76503a11.
