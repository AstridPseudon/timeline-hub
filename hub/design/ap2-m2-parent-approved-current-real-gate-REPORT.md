# AP2 M2 parent approved current real gate

## Result

Ported the exact three row-local files from donor
tl/ap2-m2-parent-drop-driver-contract-correction (commit
6221b114004e3f807e32fcf7849762514f72382a) onto latest HOME:

- src/integrations/runtime/mediaImport.test.ts
- tests/e2e/local/support/app.ts
- tests/e2e/local/three-products.spec.ts

The files are byte-for-byte equal to the donor versions. No product writer,
provider, native contract, UI, pin, schema, dependency, or shared-file change
was made. The import entry uses authoritative entry.object_id; the verified
five-field selection remains separately asserted. The negative
verified-selection case remains present, and the selector identifies exactly
one manual-drop test.

The effective Vite config hash is
7248b56d295ab3b273ae6eeeb1d1263ddc17919c, matching ce6deafa3;
e401af721 and ce6deafa3 are ancestors, and retired alias bytes are absent.
The current diff contains exactly the three donor paths.

## Tests and preflight

- ESLint:
  ./node_modules/.bin/eslint --no-cache --max-warnings 0 tests/e2e/local/support/app.ts tests/e2e/local/three-products.spec.ts src/integrations/runtime/mediaImport.test.ts — passed.
- Targeted Vitest:
  node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-bootstrap-transport-assertion-repair/notes/vitest-runner.cjs node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism src/integrations/runtime/mediaImport.test.ts src/integrations/runtime/dataProvider.test.ts src/tools/video-editor/hooks/useAssetManagement.mediaImport.test.tsx — 3 files, 84 passed.
- Playwright collection preflight:
  node node_modules/playwright/cli.js test --config playwright.three-products.config.ts --grep 'M2 real mounted manual video drop' --list tests/e2e/local/three-products.spec.ts — exactly 1 test.
- Strict custody guard suite:
  node --test --experimental-test-isolation=none scripts/testing/current013-integration.test.mjs — 15 passed, 0 failed. The approved independent report records 16 for its earlier source tree; the current checked-in suite contains 15.
- Central named suite, exactly once with --no-cache:
  ap2-m2-parent-drop-real-central-qualification, run
  ap2-m2-parent-approved-current-real-gate-ap2-m2-parent-drop-real-central-qualification-1020231135-5013 — failed, exit 1, 247s.

The central run passed source/artifact guards, hosted build, and browser launch,
then failed in the negative case while waiting 90s for the tampered
GET /media-selection/verified response (three-products.spec.ts:1427).
Therefore native positive add, reload/lost-ACK/restart/exact-retry, Runtime
undo, and zero-legacy assertions were not reached and are unverified.

## Bounded failure evidence

Retained sanitized service log/source identity:

- App snapshot tree: 78f3784287d78fc92677ebe5eb710d162b0f50ae
- Agent: 3c4f6de4fa777323b3386c01c7266b619b86af6d
- Runtime: 202074110717146fc7f08af2306a8dd7f695b0b1
- Producer: a0dca16975dfe8f5e762703b99d9791a16cf7fd7
- Central failure: TimeoutError at the negative-case response wait.

The selected existing qualification wrapper removes its disposable browser
root, so no trace, request/response summary, or error-context file survived;
none is claimed. The previous retained-evidence 23319 result was read but not
reused because its fixed source pin targets the older tree and would fail
before execution.

## Cleanup and next step

Worktree has no build output or temporary files; git diff --check passed.
Free disk was 19 GiB. No bounded physical writer cut is prepared because the
gate failed before qualifying the positive consumer path. The next step is an
orchestrator-approved diagnosis/fix of the missing negative verified-selection
response, followed by a new explicitly authorized gate.
