# D141 future receiving commands

These are bound, supported commands for the next heavy controller. They were not executed by this worker. Run them from `/home/user/work/app` only after the controller has taken the existing one-body heavy slot. Each `--submit` call is the existing D66/D73 route: it captures the four clean normal homes, requests detached exact checkouts, waits for the four receipts, registers the paired rows atomically, submits pure preflight, waits for PASS, then submits the normal row.

The environment-clearing prefix is required by the retained recipe. `D66_SUBMIT_TARGET` is the supported stable target; `D66_SUBMIT_SUITE` is the supported unique-row override. No manual `tests/suites.conf` edit is part of this route. The source homes and target are the exact final tuple in `binding.json`.

## Serial order

Run exactly one command at a time, in this order:

1. `p1`
2. `p2-automatic-child-placement`
3. `p2-popup-add`
4. `p2-parent-move`
5. `p2-transition-none-single`
6. `p2-transition-none-bulk`
7. `p2-register-asset`
8. `p3`

## Exact D66 `--submit` argv

```sh
cd /home/user/work/app
env -u NODE_PATH -u ASTRID_PUBLIC_CHECKOUT -u ASTRID_APP_DIRECT_DIST -u APP_DIRECT_DIST D66_SUBMIT_TARGET='app-pin-867cb273' D66_SUBMIT_SUITE='d141-p1-867cb273-submit' '/home/user/work/runtimes/agent-remotion-app-p1-787-2a9-1830/.toolchain/node-v20.19.4-linux-x64/bin/node' --max-old-space-size=6144 --import tsx scripts/testing/d66-plain-stack.mjs 'p1' --submit

env -u NODE_PATH -u ASTRID_PUBLIC_CHECKOUT -u ASTRID_APP_DIRECT_DIST -u APP_DIRECT_DIST D66_SUBMIT_TARGET='app-pin-867cb273' D66_SUBMIT_SUITE='d141-p2-automatic-child-placement-867cb273-submit' '/home/user/work/runtimes/agent-remotion-app-p1-787-2a9-1830/.toolchain/node-v20.19.4-linux-x64/bin/node' --max-old-space-size=6144 --import tsx scripts/testing/d66-plain-stack.mjs 'p2-automatic-child-placement' --submit

env -u NODE_PATH -u ASTRID_PUBLIC_CHECKOUT -u ASTRID_APP_DIRECT_DIST -u APP_DIRECT_DIST D66_SUBMIT_TARGET='app-pin-867cb273' D66_SUBMIT_SUITE='d141-p2-popup-add-867cb273-submit' '/home/user/work/runtimes/agent-remotion-app-p1-787-2a9-1830/.toolchain/node-v20.19.4-linux-x64/bin/node' --max-old-space-size=6144 --import tsx scripts/testing/d66-plain-stack.mjs 'p2-popup-add' --submit

env -u NODE_PATH -u ASTRID_PUBLIC_CHECKOUT -u ASTRID_APP_DIRECT_DIST -u APP_DIRECT_DIST D66_SUBMIT_TARGET='app-pin-867cb273' D66_SUBMIT_SUITE='d141-p2-parent-move-867cb273-submit' '/home/user/work/runtimes/agent-remotion-app-p1-787-2a9-1830/.toolchain/node-v20.19.4-linux-x64/bin/node' --max-old-space-size=6144 --import tsx scripts/testing/d66-plain-stack.mjs 'p2-parent-move' --submit

env -u NODE_PATH -u ASTRID_PUBLIC_CHECKOUT -u ASTRID_APP_DIRECT_DIST -u APP_DIRECT_DIST D66_SUBMIT_TARGET='app-pin-867cb273' D66_SUBMIT_SUITE='d141-p2-transition-none-single-867cb273-submit' '/home/user/work/runtimes/agent-remotion-app-p1-787-2a9-1830/.toolchain/node-v20.19.4-linux-x64/bin/node' --max-old-space-size=6144 --import tsx scripts/testing/d66-plain-stack.mjs 'p2-transition-none-single' --submit

env -u NODE_PATH -u ASTRID_PUBLIC_CHECKOUT -u ASTRID_APP_DIRECT_DIST -u APP_DIRECT_DIST D66_SUBMIT_TARGET='app-pin-867cb273' D66_SUBMIT_SUITE='d141-p2-transition-none-bulk-867cb273-submit' '/home/user/work/runtimes/agent-remotion-app-p1-787-2a9-1830/.toolchain/node-v20.19.4-linux-x64/bin/node' --max-old-space-size=6144 --import tsx scripts/testing/d66-plain-stack.mjs 'p2-transition-none-bulk' --submit

env -u NODE_PATH -u ASTRID_PUBLIC_CHECKOUT -u ASTRID_APP_DIRECT_DIST -u APP_DIRECT_DIST D66_SUBMIT_TARGET='app-pin-867cb273' D66_SUBMIT_SUITE='d141-p2-register-asset-867cb273-submit' '/home/user/work/runtimes/agent-remotion-app-p1-787-2a9-1830/.toolchain/node-v20.19.4-linux-x64/bin/node' --max-old-space-size=6144 --import tsx scripts/testing/d66-plain-stack.mjs 'p2-register-asset' --submit

env -u NODE_PATH -u ASTRID_PUBLIC_CHECKOUT -u ASTRID_APP_DIRECT_DIST -u APP_DIRECT_DIST D66_SUBMIT_TARGET='app-pin-867cb273' D66_SUBMIT_SUITE='d141-p3-867cb273-submit' '/home/user/work/runtimes/agent-remotion-app-p1-787-2a9-1830/.toolchain/node-v20.19.4-linux-x64/bin/node' --max-old-space-size=6144 --import tsx scripts/testing/d66-plain-stack.mjs 'p3' --submit
```

For each command, D66 derives the preflight row by appending `-preflight`; the normal row is the suite name above. The generated row command is the exact `serviceRecipe` form in `scripts/testing/d66-plain-stack.mjs`, using full 40-character SHA/tree pins and the four D66-created checkout paths. Do not replace those paths with normal homes, local dist, or an overlay.

## Service outputs and guards

- Checkout receipts: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/queue/done/checkout-{app,agent,runtime,composition}-{full-head}`.
- Submit plans: D66 defaults to `/tmp/d66-{selector}/{selector}-submit-plan.json` unless the future controller supplies its own private `D66_OUTPUT_DIR`.
- Test result directories: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/{service-result-id}`.
- D73 sequence is `request-test <target> <row>-preflight --no-cache`, `wait-test <preflight-id>`, then `request-test <target> <row> --no-cache`; the normal request is not issued before preflight PASS.
- Keep source/hash/clean guards before and after each body, preserve the private raw outputs and `KEEP` markers when a result names them, and retain all failures.
- Admission is measured once when the controller is dispatched at >5.2 GB available; stop newest non-gate work at 4.0 GB. This worker did not measure or request admission.

No generated command was run here. No broad `p2`, SWAP, Element, live-edit, source checkout request, test-service request, browser, build, import, or product execution was performed.
