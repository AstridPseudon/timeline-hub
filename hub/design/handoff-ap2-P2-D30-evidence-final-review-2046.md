# D30 P2 evidence review

Verdict: P2 remains unqualified. The retained body run is RED; no alternate run or workaround was attempted.

| Dimension | Verdict | Finding |
|---|---|---|
| Original 8 / no weakening | PASS | Current App is exactly `2107e1870e51c650d59315f4cc1ab6af338f198c`, tree `a3ff3584e9b559bbb3c3a82b77be7516ed8e761c`; clean diff. Approved selector listing returned exactly 8 tests: 3 + 3 + 2. |
| Finite final row changes / custody | INSUFFICIENT | Final row changes and hashes are retained, but P2 Agent row pin `079580ca` conflicts with declared `ext` `9a095a95`; actual daemon/provider identity and environment equivalence are unknown. |
| Exact first failed boundary per case | INSUFFICIENT | Exact first boundaries are known for tests 1, 4, and 6; the five serial non-runs have no captured per-case reason. |
| Safe evidence limits / owner | PASS | Only bounded projections were used. P2/P3 historical runs remain diagnostic only. Graph/toolchain-2020 refusal remains stopped and unresolved; no workaround or permission conclusion was made. |

Known run results:

- P2 `31814`: exit 1, 204s; 0 passed, 3 failed, 5 did not run.
- Preflight `14651`: green, but did not mount the editor and is not body evidence.
- First failures:
  - `elements-assets:376`: `runtime-connection-status` element absent during `openTimeline`.
  - `popup:807`: fixture setup received safe-projected HTTP 422 `validation_error` / `capture_mismatch` for undeclared created identities, before the gesture.
  - `tour:564`: same absent connection-status element during `openCommandTimeline`.
- Tests 2, 3, 5, 7, and 8 did not run; the source’s serial mode explains the likely skip chain, but no actual per-case reason was captured.

Source review:

- Approved command completed successfully with status 0 and listed all 8 selectors:
  `/home/user/work/runtimes/agent-remotion-ap2-current-bac-d9e-1643/.toolchain/node-v20.19.4-linux-x64/bin/node /home/user/work/app/node_modules/playwright/cli.js test --config playwright.three-products.config.ts tests/e2e/local/three-products.p2-tour.spec.ts tests/e2e/local/three-products.p2-elements-assets.spec.ts tests/e2e/local/three-products.p2-popup.spec.ts --list`
- Relevant source confirms the hosted/same-origin connection gate and pill distinction; this does not establish the actual runtime cause.
- Historical popup identity repair `17324ed4b` → `93cddc687` was not duplicated or credited as new body evidence.
- No tests, lint, typecheck, browser, HTTP, socket, service, seed, graph, build, install, or full suite was run. `git diff --check` passed.