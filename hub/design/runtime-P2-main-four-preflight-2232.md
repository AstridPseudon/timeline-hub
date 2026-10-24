## Report

- Read PLAN and exact App peer handoffs.
- Captured fixed tuple and genuine detached checkout receipts:
  - App `bceb…` / tree `46ad…`
  - Agent `039ff…` / tree `4e40…`
  - Runtime `732c…` / tree `7ed0…`
  - Composition `635f…` / tree `5ab5…`
- Source-only preflight: **PASS**.
- Submitted `p2-parent-move` through D66 persistent plan.
- Service preflight ID: `app-pin-bceb0350-d73-p2-parent-move-mainfour-2232-bceb0350-preflight-1024223544-27231`
- Result: **FAIL, exit 127**. The generated recipe invokes an absent runtime Node path. No normal gesture request was submitted; the other three cases were not started.
- Worktree remains clean; no product/test changes.
- Blocker recorded in `BLOCKED`; commit message recorded as requested.

Next step: repair the existing D66 recipe’s Node path to `/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node` through the owning workflow, then rerun the four cases under the original one-request rule.