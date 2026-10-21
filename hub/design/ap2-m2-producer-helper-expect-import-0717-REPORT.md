# App M2 producer helper expect import — 0717

## Result

Implemented the one authorized product-tree change: `tests/e2e/local/support/producer-ownership-current-pin.ts` now imports the existing Playwright `expect` binding alongside `Page`.

No producer assertion, spec, config, body, option, timeout, selector, product, Runtime, pin, wrapper, or startup artifact was changed. No actual/browser/build/daemon/socket/full/install run was performed.

## Minimal diff and hashes

```text
-import type { Page } from '@playwright/test';
+import { expect, type Page } from '@playwright/test';
```

The diff is exactly one line in the assigned helper. The pre-edit helper hash was the required `50cbe5341f24c9a1ecc999018e2c6d975380a3440570abce151f9173c9752016`. Current helper hash is `d86721bd680691e29e705900e03862497a7d97b069f2e43c6192d739cbc9e09b`. Removing only the added `expect, ` from the import reproduces `50cbe534...` exactly.

The selected spec remains SHA-256 `d91d0c1cce22f68119cd30fcb0a288346474b0ad4b64c84dcee3b730fa468d89`; the producer config remains `5b880ceff883abce2575a3a85aaa4eda69d3bcb848768ff0e91f337d50cca4c0`; and the existing runner remains `329cfca7ff6fcc6764e5eaa6cb53ba77a40e6aa842361d0ed6795ca5b4398352`. Helper `expect(` count is unchanged at 1 before/after, and the selected spec was not edited.

## Checks

- `./node_modules/.bin/eslint --no-cache --max-warnings 0 tests/e2e/local/support/producer-ownership-current-pin.ts tests/e2e/local/producer-ownership-current-pin.spec.ts` — PASS.
- `./node_modules/.bin/eslint --no-cache --no-warn-ignored --max-warnings 0 --rule 'no-undef:error' tests/e2e/local/support/producer-ownership-current-pin.ts tests/e2e/local/producer-ownership-current-pin.spec.ts` — PASS; targeted AST free-runtime-name/binding check found no undefined runtime names.
- `./node_modules/.bin/tsc --noEmit --skipLibCheck --target ES2020 --module ESNext --moduleResolution bundler --allowImportingTsExtensions --strict --jsx react-jsx --types node --types @playwright/test tests/e2e/local/support/producer-ownership-current-pin.ts tests/e2e/local/producer-ownership-current-pin.spec.ts` — report-only FAIL from pre-existing dependency-graph diagnostics. The target-specific diagnostic is `TS2459: Module './app.ts' declares 'DirectHarness' locally, but it is not exported` at the helper's existing `type DirectHarness` import. `app.ts:8` imports `DirectHarness` from `harness.ts` but does not re-export it; the same helper import exists in `HEAD` before this change. Other output is existing unresolved source/dependency diagnostics; no second missing runtime binding was found by the no-undef AST check. Per task, this was not edited because only the expect import was authorized.
- `./node_modules/.bin/playwright test --config playwright.producer-ownership-current-pin.config.ts tests/e2e/local/producer-ownership-current-pin.spec.ts --list` — PASS; exactly `Total: 1 test in 1 file`. Collection only; no test body ran.
- Existing list/zero-test/child-exit guard logic, exercised with a disposable stub and cleaned afterward — PASS: list-one exit 0, zero-test refusal exit 1, child status 7 propagated as 7.
- Stripped-import SHA reconstruction, assertion/spec/config preservation checks, `git diff --check` — PASS.
- Current `harness.ts` SHA `0b5ac38fc5c11794d2e9ed75d03adf4e085262825a56db36aa73b08e4d630a14` and `app.ts` SHA `d1b317b71e4ddfae28aafedb5f5926d4acae68fbedc516720e7ede2194d4ca7d` equal their base versions.

## Reused evidence and custody

The existing startup evidence remains reusable for this test-only import change: startup test `ap2-m2-producer-realm-physical-path-diagnosis-0538-ap2-m2-producer-health-conversion-review-0703-startup-1021070652-30920` passed with physical TMPDIR startup, planted symlink refusal, direct/door identity, teardown, and zero producer/body execution. The retained owned probe SHA is `a062cab11ea3a86ef75ece5a86584d0555040336032ced515d6ac50de9481d8f`; the module-format probe SHA is `d4eeaeb74a582fe9ccb94c1cfba7f66c41ec50eef7823db34f61ed7185e12af3`; and the startup custody gate SHA is `ffeaa34c944b931a0e2f393156dd3dc78cb39318bf24c64bb4073e2b6b3d5a20`. Prior review records that the startup/probe artifacts preserve the existing `DirectHarness` startup/health/teardown and physical-root guards; this worker did not touch them.

Source protection was created before completion: worker `KEEP` and explicit `SOURCE_LEASE` are present under the assigned worker record. Current pre-commit source is HEAD `b8cc7e1c79ec5516b9eee3832b5c33d62dac1aa7`, tree `fd16d32fd3487e56c9fe1ff16582dba240f63b77`, plus the one uncommitted helper import. The final harness commit SHA/tree is not available until the harness commits the worktree.

## Blockers and next step

No task blocker remains. The report-only `DirectHarness` export diagnostic is pre-existing and should be handled separately if the App team wants a clean targeted TypeScript lane. The next producer qualification must obtain fresh custody for the changed helper hash before any actual run; this worker did not request or perform one.
