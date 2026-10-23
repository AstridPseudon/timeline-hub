# P1 D25 real failure artifact qualification

PASS for the requested offline qualification. Imported exactly the three cumulative blobs from `d0898e216f545057b8cfdf2f525c35c74cddfa5c` using read-only Git blob reads and file writes onto current App `2107e1870e51c650d59315f4cc1ab6af338f198c`. Added one regression to `p1-diagnostic-safety.test.ts`. Relative to d089, the spec and diagnostic helper remain byte-exact; only that regression and its builtin import are new. No other current App file changed.

## Actual caller proof

The regression transpiles and executes the complete on-disk spec, diagnostic helper, and existing `support/app.ts` modules. It captures the spec's actual registered beforeEach/afterEach callbacks through a passive test registration boundary. It does not extract/reimplement `captureFailureContinuation`, replace `commandOutboxes`, stub diagnostic helpers, or add a production export/hook. Fixtures, prerequisite beforeAll and the two original journey bodies are registered but never run.

The actual beforeEach response listener populates its private diagnostic trace with 40 safe wire heads. The registered failing afterEach calls the real capture continuation, file formatter/writer and existing commandOutboxes seam. The page.evaluate boundary invokes the real support/app.ts IndexedDB callback; indexedDB.databases is controlled to remain unresolved or throw. The page/locator boundary also covers unresolved DOM promises and a closed page. Before each attempted DOM/IndexedDB read, the regression opens the real output file and verifies its early phase, parseability, exact title/status/tuple and explicit UNKNOWN fields. Boundary assertions are retained and checked outside production's intentional catch path so they cannot be swallowed as diagnostic failures.

The test verifies the file is larger than 16 KiB and the 40th safe revision is physically beyond byte 16,384, while raw keys, response bodies and tokens are absent. After the hook returns, the file and its tail still parse and survive. An independent 2,500 ms watchdog bounds the actual registered hook even while IndexedDB/DOM promises remain unresolved. Separate controls exercise throwing reads, closed page, outputPath throwing, a real write error (directory path), attach rejection and attach never settling. Each keeps the original AssertionError object primary through failing-test finally teardown, with testInfo.error/errors unchanged. Matching expected status bypasses reads and attachments.

## Exact source and integrity

- Base commit: `2107e1870e51c650d59315f4cc1ab6af338f198c`; base tree: `a3ff3584e9b559bbb3c3a82b77be7516ed8e761c`.
- Final worktree tree: `5ce46b64b63862f103379df3f3d74982e4ef461a` (computed with Git object serialization/SHA-1; no Git tree/index/ref write).
- `tests/e2e/local/three-products.p1-chain.spec.ts`: blob `ef48477c1ae3382a155717acfeb79ab26bb72a4e`; SHA-256 `be63db711ea6857c45bfcb3b41909ae083d4147cd0f608760701f5044f12e497`.
- `tests/e2e/local/p1-diagnostic-safety.ts`: blob `aa767e0c72c083173ee42b46ae018da103e2bff5`; SHA-256 `92e780dc73165857ab8090a8cfebd6220fa4044689493c8cf9fa4c0cf8b4c6a0`.
- `tests/e2e/local/p1-diagnostic-safety.test.ts`: blob `4ca90a159f89c57233857f77edfdba82632ced9b`; SHA-256 `a965098ec8b019d4988cd22e0450a53e7e6b1069bd6c0e0fc24610be9dca80b1`.
- First title-to-second-title boundary SHA-256: `4b04ad7ef74b8106244d87c23d12c7a18da251dd8f5a746f42d3221a72ea8b7f`.
- Second title-to-EOF SHA-256: `2f7501184477c8aec38d3cd289dd13c0d011fa8f69ecd43378f24f6c3100a2f7`.
- Both protected slices match the mandated hashes. The second catch, original afterEach predicate, assertions and timeouts are unchanged from the exact imported source.
- Read-only scope verification: `git diff 2107e1870e51c650d59315f4cc1ab6af338f198c -- . ':(exclude)tests/e2e/local/three-products.p1-chain.spec.ts' ':(exclude)tests/e2e/local/p1-diagnostic-safety.ts' ':(exclude)tests/e2e/local/p1-diagnostic-safety.test.ts'` is empty. `git diff --name-only` and `git status --short` contain only those three authorized files, with nothing deleted.
- `git merge-base --is-ancestor d0898e216f545057b8cfdf2f525c35c74cddfa5c 2107e1870e51c650d59315f4cc1ab6af338f198c` and the equivalent check for `53b5733c3cc930bab55b3216b9f72f1bee112888` both return 1 (absent ancestry). HEAD remains current2107. Harness must create/verify the single own commit and final tree after exit; no commit hash exists yet.

## Exact verification commands

All commands ran in `/home/user/work/wt/ap2-P1-D25-artifact-integration-sol-1936`, with shared dependencies read-only and scratch/cache output under the existing private TMPDIR. Final check logs are alongside this report.

- Focused safety: `/home/user/work/runtimes/agent-remotion-ap2-current-bac-d9e-1643/.toolchain/node-v20.19.4-linux-x64/bin/node --import /home/user/work/app/node_modules/tsx/dist/loader.mjs --test tests/e2e/local/p1-diagnostic-safety.test.ts` — PASS (exit 0; file-level TAP: 1 pass, 0 failures; new regression completes all seven fault conditions).
- Root TypeScript: `/home/user/work/runtimes/agent-remotion-ap2-current-bac-d9e-1643/.toolchain/node-v20.19.4-linux-x64/bin/node /home/user/work/app/node_modules/typescript/bin/tsc --noEmit` — PASS (exit 0).
- App TypeScript: `/home/user/work/runtimes/agent-remotion-ap2-current-bac-d9e-1643/.toolchain/node-v20.19.4-linux-x64/bin/node /home/user/work/app/node_modules/typescript/bin/tsc -p tsconfig.app.json --noEmit` — PASS (exit 0).
- Node TypeScript: `/home/user/work/runtimes/agent-remotion-ap2-current-bac-d9e-1643/.toolchain/node-v20.19.4-linux-x64/bin/node /home/user/work/app/node_modules/typescript/bin/tsc -p tsconfig.node.json --noEmit` — PASS (exit 0).
- Scoped lint: `/home/user/work/runtimes/agent-remotion-ap2-current-bac-d9e-1643/.toolchain/node-v20.19.4-linux-x64/bin/node /home/user/work/app/node_modules/eslint/bin/eslint.js tests/e2e/local/three-products.p1-chain.spec.ts tests/e2e/local/p1-diagnostic-safety.ts tests/e2e/local/p1-diagnostic-safety.test.ts --max-warnings 0` — PASS (exit 0).
- P1 discovery: `/home/user/work/runtimes/agent-remotion-ap2-current-bac-d9e-1643/.toolchain/node-v20.19.4-linux-x64/bin/node /home/user/work/app/node_modules/playwright/cli.js test --config playwright.three-products.config.ts tests/e2e/local/three-products.p1-chain.spec.ts --list` — PASS (exit 0; exactly 2 original tests in 1 file).
- Whitespace: `git diff --check` — PASS (exit 0).

The first developmental regression run failed because its VM omitted the process global used by existing fixture registration. Supplied the standard process global to the test context, removed temporary diagnostics, and reran the approved focused check successfully on final bytes. No caller/helper fix or test weakening was needed.

## Decisions, limits and next step

Used whole-module VM execution to exercise the actual registered caller and real existing commandOutboxes seam without creating a browser, service, socket or product hook. No design decision was changed. Full v2 request/reply contract, real mounted App/outbox product code, both original P1 bodies, assertions, preflight, provisioning and dependencies remain unchanged. Unknown mounted dataRef, callback patch/result, originalLocalSaveBasis, capture result and session adoption remain UNKNOWN; wire/DOM observations do not infer them.

No browser/HTTP/service/full suite, original journey body, install, dependency mutation, shared-cache write, Git write, commit, merge or push was performed. This qualifies offline artifact reliability only; it does not resolve or rerun the actual journey. Actual 18607 remains 1 PASS / 1 FAIL, NO-GO; historical causal claims remain insufficient evidence. Nothing is blocked within this task.

Next: independent Luna review of this exact final tree before any remote App merge; harness verifies one own commit directly on current2107, with no d089/53b ancestry. Do not promote the actual P1 verdict from this offline qualification.
