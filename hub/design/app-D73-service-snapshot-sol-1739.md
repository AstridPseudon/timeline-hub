Implemented D73 in only `scripts/testing/d66-plain-stack.mjs` and its test file.

- Accepts exact pinned App HEAD, or an unchanged-tree service snapshot whose **sole parent is that exact pin**.
- Refuses wrong parents, grandparent ancestry, multiple parents, dirty sources and incorrect selections.
- Defaults submission to the stable `app-pin-<capturedApp8>` target after receipt and metadata verification.
- Adds `--preflight`, sharing normal-run source verification and recording service snapshot identity separately from pins.

**Validation:** Node 20 executable:
```sh
NODE20=/home/user/work/runtimes/agent-remotion-app-p1-787-2a9-1830/.toolchain/node-v20.19.4-linux-x64/bin/node
```

Commands and results:

- `$NODE20 --test scripts/testing/d66-plain-stack.test.mjs` — **14 passed**, including real Git snapshot fixtures and missing-pin poison in both modes.
- `$NODE20 --check scripts/testing/d66-plain-stack.mjs` and corresponding `.test.mjs` check — passed.
- `$NODE20 node_modules/eslint/bin/eslint.js scripts/testing/d66-plain-stack.mjs scripts/testing/d66-plain-stack.test.mjs --max-warnings 0` — passed.
- `$NODE20 node_modules/typescript/bin/tsc -p tsconfig.node.json --noEmit` — passed.
- Same TypeScript command with `tsconfig.strict-islands.json` — exit 2; all **15 diagnostics match the prior D73 baseline verbatim**.
- `$NODE20 --import tsx scripts/testing/d66-plain-stack.mjs <suite> --collect` for `p1`, `p2`, `p2-element`, `p3` — **2/8/1/1**. Caches/output were confined to `$TMPDIR`.
- `git diff --check` — passed. All six protected spec SHA-256 values match HEAD exactly.

Tested launcher SHA-256: `e945b2a58490da52930fda0a8a5c150be1a16d7d042936a5b9661e43d531cace`.

**Manager flow after home integration:**
```sh
cd /home/user/work/app
env -u D66_SUBMIT_TARGET D66_SUBMIT_SUITE=d73-p1-snapshot \
  "$NODE20" --import tsx scripts/testing/d66-plain-stack.mjs p1 --submit
```

Register both emitted recipes. Run the emitted preflight request against its stable App target and wait for success; then run the emitted normal request using the **same captured tuple**, without rerunning `--submit`.

No plan deviations or blockers. Actual service/browser/full execution remains unverified, as required. Product code, C0 inventory and protected journeys are unchanged. Commit message and `DONE` written.