# App runner handoff: zero-test guard

App worker `app-m2-runner-zero-tests-argv-guard-r1` found the app2 0250 row-local runner correction in `fb07523d5` (manual selector forwarding), with the later preflight composition in `45fbfc867`. This worker intentionally does not duplicate either selector/config/argv repair.

The only source change here is the existing App-owned `tests/e2e/local/support/run-parent-manual-drop-evidence.sh`: after its child returns, a zero-test signature or missing registered manual-drop title turns an otherwise successful child into failure. Its existing `probe` now plants `No tests found` plus `Running 0 tests` with exit 0 and proves refusal, then accepts a one-title discovery. Preserve this hunk when composing the app2 row-local runner changes.

Diagnosis for the registered invocation: `node node_modules/playwright/cli.js test --config playwright.three-products.config.ts --grep 'M2 real mounted manual video drop' --list` discovers exactly one test at `tests/e2e/local/three-products.spec.ts:1440`; the config inherits `testDir: './tests/e2e/local'` from `playwright.direct.config.ts` and overrides `testMatch` to `three-products*.spec.ts`. There is no separate `include` setting.
