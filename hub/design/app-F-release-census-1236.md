## Report

- Fixed both D54 nodes by restoring the exact upstream script in `package.json`:
  - `verify-extension-ship.test.mjs:51` — core release manifest/gate validation.
  - `verify-extension-ship.test.mjs:617` — core help/plan non-execution boundary.
- Root cause: U3 package join dropped `test:e2e:chrome-export`; upstream `2a288e6` contains:
  `node scripts/portable-developer-command.mjs timeline-chrome-export`.
- Classification: regression, not environment/pre-existing/deferred/dead-scope. No tests, locks, release config, security logic, or browser commands changed.

Evidence:

- Full run `16138`: exit 1; both failures reported missing `package.json` script.
- Upstream/current verifier and helper source blobs match; only the package script was missing.
- `git diff --check`: passed.
- Exact manifest test: passed, 1/1.
- Direct `--help` and `--plan`: exit 0; plan remained non-executing and includes the Chrome export gate.
- The second exact Node test could not run locally because sandboxed `spawnSync(process.execPath, …)` returns `EPERM`. Central targeted service only invokes Vitest and found no test files. No browser/release execution occurred.

Changed only `package.json`. Commit message and `DONE` marker created.