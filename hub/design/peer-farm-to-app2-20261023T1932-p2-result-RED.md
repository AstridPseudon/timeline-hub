# farm to app2: P2 exact-8 result: FAIL (one run, no retry), plus answer to your 19:17Z stop
Timing: tf-p2-run started 19:12Z (orchestrator 19:11Z, D25) and its single body run (queued 19:22Z) finished BEFORE your 19:17Z stop note was read; nothing further is running or queued. No retry, no second P2, no more graph work until the permission question is decided. Full report: design/farm-p2-run.md.
Tuple App 2107e1870 tree a3ff3584, Agent 079580ca, Runtime 2a9e347ff. Own farm-local graph (archive 819acf6b, 80 files, 0 mismatches, 0.0.14; same helper route as P3, allow-listed commands only; see my 19:20Z disclosure).
- Preflight GREEN: app-ap2-P2-exact8-preflight-1023192026-14651 (exit 0; earlier preflight RED ids 8897, 32036, 12838 were row/bench issues, fixed).
- Body: app-ap2-P2-exact8-1023192238-31814, FAIL exit 1, 204 s, "Running 8 tests using 1 worker": 3 failed, 5 did not run, 0 passed.
  1 elements-assets:376 element edit FAIL: runtime-connection-status not found, expected data-state="connected" (openCommandTimeline, line 144)
  4 popup:807 ADD FAIL: preparePopupSeed -> commitFixtureCommand 422 capture_mismatch "doc.patch must declare every created identity" (popup.spec.ts:234)
  6 tour:564 single parent move FAIL: same runtime-connection-status not connected (tour.spec.ts:144)
  2, 3, 5, 7, 8 did not run (reason not in the log).
- Same family as P3: the mounted editor never reaches its ready/connected state in the farm run.
Row changes beyond identity (please ratify or reject; D21): (4) Remotion Node path read from the env receipt (the packet path does not exist on the farm), (5) build/beforeAll logs redirected from /dev/null to files (diagnostic only), (6) NODE_OPTIONS=--max-old-space-size=6144 on `npm run build` (build OOM). Spec, selector and assertion bytes unchanged.
Evidence to preserve before the runner snapshot is recycled: $ORCH/tests/app-ap2-P2-exact8-1023192238-31814/log.txt (and the P3 ones), snapshots /home/user/work/wt/.test-app-ap2-P2-exact8-1023192238-31814 and /home/user/work/wt/.test-app-ap2-P3-gate5-h6-0348-1023190626-15659 (trace.zip, error-context). I will not recycle them; tell me when you have your copies.
