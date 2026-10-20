# App M2 shot-name final source-runner execution

Result: PASS.

## Final source and pins

- App branch: `tl/app-m2-shot-name-final-source-runner-executor`
- App HEAD: `e245125168979218ebc0fcc880b59769250a4039`
- App committed tree: `b52120ac0772d1874ed5d1c569c614c556f0033a`
- Central harness synthetic final tree: `c037e8f9a4d751eebfd5b86b77c6d2974338ece3`
- Agent: `8130a401bf44a518d5a40ae274d398b8c560be55`, tree `236c3e57e0265c52b81ba8085de3193026176bff`
- Runtime: `2c4ac180c2220bdad966bc01e95ad230e99ce26a`, tree `7ab412cc4bcbe517efcfa806e092336390312e18`
- Runtime producer manifest: 75 artifacts, `sha256:6f000bc615a9cb24fb00cc69a97af75eae71006ebfe87e3caa272fcdbbb1af56`
- Composition public12 archive: `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`, 77 regular files
- Chrome: Chromium 141.0.7390.37, `85918a9937192b78da8edb51c38a7af4920ac6bd9ba19939ecb0bb724d5a1a95`
- Setup guard: `88888d44ddd375caacb7b45b74001b70428bf4404b76fe11c84a83f8b05a6cfa`
- Final external runner SHA256: `91db6be2a3915f0d85bb04c919239564d03ef96b27c49c9a300f591d0a47656`

## Changes

- Retired the shot-name input assertion through the existing production-specific locator.
- Refined that locator to `input[class*="w-[200px]"]:visible`, excluding mounted track-label and aspect-ratio inputs while retaining the real desktop header field.
- The strict runner uses private dependency/Agent overlays, safe stage-only error reports, source/cache guards, and removes only its generated `dist` before postflight. No product source was changed.

## Evidence

Local targeted checks:

```text
node_modules/.bin/eslint tests/e2e/local/shot-name-command.spec.ts tests/e2e/local/support/app.ts --ext ts --max-warnings 0
VITEST_CACHE_DIR=/tmp/tl-shot-name-final-vitest-cache-v2 node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-file-parallelism src/tools/video-editor/commands/shotSetCapture.test.ts src/tools/video-editor/commands/commitSession.test.ts src/tools/video-editor/commands/shotSetSession.test.ts
```

Both passed; Vitest: 3 files, 80 tests passed.

Central browser request/wait:

- Test ID: `app-m2-shot-name-final-source-runner-executor-e2e-shot-name-final-source-e2451251-treec037e8f9-agent8130-runtime2c4-public12-v13-e2e-integration-1020162734-27536`
- Result: exit 0, 266s
- Resolver: 9 tests passed
- Playwright: exactly 1 discovered and 1 passed in 1.5m
- Postflight: source, public source, dependency cache, 75/77 artifact, and runtime producer checks passed

The passing browser case covered raw Unicode/opaque preservation, reload and Undo, lost-ACK restart retry, exact request key/body/receipt, original 409 draft retention, and absence of legacy saves. No row-deleted claim was made. No full suite, TypeScript check, install, or product edit was run.

Earlier central attempts were classified as runner/source or test-carrier setup failures: stale tree registration, then broad dialog input selection, then the aspect-ratio input match. The final run reached and passed the product contract.
