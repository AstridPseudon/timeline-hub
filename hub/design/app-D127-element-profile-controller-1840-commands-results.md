# D127 commands and results

## Dispatch

The exact expanded command and path-only derivative were emitted before execution. The only mechanical changes from the reviewed recipe were private output paths and `WORKER`:

```text
cd /home/user/work/app
D66_OUTPUT_DIR=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-D127-element-profile-controller-1840/submission/p2-element
D66_SUBMIT_PLAN_PATH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-D127-element-profile-controller-1840/submission/p2-element/p2-element-submit-plan.json
/home/user/work/runtimes/agent-remotion-app-p1-787-2a9-1830/.toolchain/node-v20.19.4-linux-x64/bin/node --max-old-space-size=6144 --import tsx scripts/testing/d66-plain-stack.mjs p2-element --submit
```

No product source, test, generated file, pin, dependency, or shared install was changed.

## Controller results

- Controller: one `p2-element --submit` invocation; no retry or resubmission.
- Preflight ID: `app-pin-d5a1d1ab-d73-p2-element-d5a1d1ab-submit-preflight-1025183946-29958`; exit 0, `PASS`.
- Normal ID: `app-pin-d5a1d1ab-d73-p2-element-d5a1d1ab-submit-1025184016-32016`; exit 1, `FAIL`.
- Plan SHA256: `21c1e9471c61d3e7925062f3e0a0bf3b943d988dad200d789dcb4018bd1b403c`.
- Normal counts: 1 readiness test passed; 1 element test failed.
- Readiness: `D28 mounted readiness` passed, exit 0.
- First failed predicate: `tests/e2e/local/three-products.p2-elements-assets.spec.ts:1052`, unchanged `toContainText('applied')` with the original 5000 ms timeout; status locator was not found. The following page-close/waitForResponse error is secondary teardown evidence.
- Exact JUnit/log/trace/diagnostic and private capture remain in the normal result directory recorded in `submission.json` and `source-custody.json`.
- Final custody verification found that the current App and Runtime receipt-file hashes differ from the hashes recorded by the earlier source review; the current receipt contents still name the exact pinned heads, and no source checkout or product tuple changed. Current hashes are recorded in `source-custody.json`; this is an observed custody discrepancy for manager review, not a reason to retry or substitute.

## Test evidence

The prescribed central wait command was run for the same normal ID and completed with exit 1 after 286 seconds. No full suite, alternate route, retry, browser rerun, or local test command was run.
