# P1 D25 full diagnostic artifacts

## Result

PASS for the requested D25 diagnostic-file transport change. This is test-only App instrumentation; it does not change the product caller, request body, retry behavior, preflight, benchmark, service, or causal/oracle expectations.

The failure-only `afterEach` path now builds a safe, parseable JSON artifact before capped priority-console logging, writes it through Playwright `testInfo.outputPath()` and `testInfo.attach()`, and catches every artifact write/attach failure so it cannot replace the original assertion failure. The artifact has no overall 16 KiB or global-depth truncation. Existing allowlisted structural fields, credential redaction, string/array limits, and bounded traces remain in force.

## Source and exact diff

- App base: `2107e1870e51c650d59315f4cc1ab6af338f198c` / tree `a3ff3584e9b559bbb3c3a82b77be7516ed8e761c`.
- Changed files only:
  - `tests/e2e/local/three-products.p1-chain.spec.ts` — blob `60f918d536cc313860c2456a0935c046283077f6`, SHA-256 `492ba4e4d6a28672b82ec183da8ac749d3e8ae3e428d18a188afc80142fe7ea6`.
  - `tests/e2e/local/p1-diagnostic-safety.ts` — blob `3ad197264e0bf272679d205cede1bc53bb8ec948`, SHA-256 `391b5dccbc3ac27eebea7ec1b5bdbbc431a9ab5c683526876ac5d636e3a35404`.
  - `tests/e2e/local/p1-diagnostic-safety.test.ts` — blob `5e979d9ccf014da38dbef37b5c0664b210cdd8ad`, SHA-256 `a6048ef395069a4d4e2ec66426807a1f8c948d807cb1c60cfc465b0fa08ca3bd`.
- `git diff --check`: PASS.
- First protected test title-to-boundary slice SHA-256: `4b04ad7ef74b8106244d87c23d12c7a18da251dd8f5a746f42d3221a72ea8b7f`.
- Second protected test title-to-EOF suffix SHA-256: `2f7501184477c8aec38d3cd289dd13c0d011fa8f69ecd43378f24f6c3100a2f7`.
- No files outside the three allowed paths changed.

## Transport and safety boundary

- Artifacts include exact test title, status, expected status, capture time, phase, duration, project/timeline tuple, source-window before/after data when available, selected identity, wire-head projections, bounded request body/key presence/byte/equality projections, owner/pending/intent counts, recovery/UI observations, error signals, and second-case context only when the second-case collector actually observed it.
- Raw request bodies and exact keys remain available only to the original protected assertions and in-memory request tracking. Artifacts expose only equality-safe projections; wire heads are separate from mounted observations.
- `mountedObservations`, `mountedDataRef`, callback patch/capture resolution are explicitly `UNKNOWN` when not available. Case 1 is never populated from case 2 context.
- Source assets, response/request bodies, principals, cookies, authorization values, tokens, and credentials are excluded or redacted. Artifact serialization uses the existing allowlist and per-field bounds, but intentionally omits the console's overall 16 KiB cap and depth cap.
- A failed output-path write or attachment returns `false` and leaves the original test failure untouched.
- Trace arrays remain bounded at the existing 40-item limit; no launcher, ledger, service, product debug hook, or indefinitely growing trace was added.

## Verification

Using the approved Node `v20.19.4` executable and existing private TSX graph:

1. `N --import D/tsx/dist/loader.mjs --test tests/e2e/local/p1-diagnostic-safety.test.ts` — PASS, 14/14 tests.
2. `N node_modules/typescript/bin/tsc --noEmit` — PASS.
3. `N node_modules/typescript/bin/tsc -p tsconfig.app.json --noEmit` — PASS.
4. `N node_modules/typescript/bin/tsc -p tsconfig.node.json --noEmit` — PASS.
5. `N node_modules/eslint/bin/eslint.js tests/e2e/local/three-products.p1-chain.spec.ts tests/e2e/local/p1-diagnostic-safety.ts tests/e2e/local/p1-diagnostic-safety.test.ts --max-warnings 0` — PASS.
6. `N node_modules/playwright/cli.js test --config playwright.three-products.config.ts tests/e2e/local/three-products.p1-chain.spec.ts --list` — PASS, exactly 2 tests listed.
7. `git diff --check` — PASS; protected slice hash checks — PASS.

No browser, HTTP, service, seed, body, preflight, benchmark, journey, full-suite, install, dependency, or shared-cache run was performed.

## Decisions and limits

- The existing afterEach collector is the only transport point changed. The protected first and second test bodies remain byte-exact.
- Full artifact files retain safe projected data beyond console capacity, while unknown mounted/capture evidence remains unknown rather than inferred from wire heads or aggregate state.
- Current D25 causal verdicts remain unchanged: both historical causes are insufficient evidence; this change is independent artifact transport only.

