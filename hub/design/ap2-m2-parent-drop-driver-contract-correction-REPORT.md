# AP2 M2 parent drop driver contract correction

## Result

Ported the approved mounted manual-drop browser row onto latest HOME and
corrected only its stale import-entry identity expectation. The row-local
changes are limited to:

- `tests/e2e/local/support/app.ts`: exact approved `File`/`DataTransfer` drop
  helper from `e07d31f2608ed5c8c63e04f01946217974758700`.
- `tests/e2e/local/three-products.spec.ts`: exact approved browser evidence and
  manual-drop row from `d4c60b271d43df1512477cdbe2cf78dddf3a72e6`.
- `src/integrations/runtime/mediaImport.test.ts`: existing triage84 test hunk,
  making the immutable five-field selection assertion explicit.

A read-only source comparison verified the mounted row is identical to the
approved `d4c60b2` row except that `entry.digest` was removed. The positive
identity now remains `entry.object_id === harness.seed.video.objectId`, with
size and media type retained. The five-field selection remains independently
checked from normal selection and verified read responses.

All 16 independently approved custody/source guards remain unchanged and are
retained by lineage; the prior approved guard report records 16 passed. The
row also retains genuine decodable WebM/File evidence, negative and positive
selection checks, raw/opaque/order assertions, reload/lost-ACK/restart/exact
retry/undo coverage, zero legacy traffic, and strict custody checks. No
`useTimelineOps`, session, Provider, Viewing, schema, pin, dependency, or
guessed `afterClipId` changes were made.

## Verification

- `./node_modules/.bin/eslint --no-cache --max-warnings 0 tests/e2e/local/support/app.ts tests/e2e/local/three-products.spec.ts src/integrations/runtime/mediaImport.test.ts` — passed.
- `node node_modules/playwright/cli.js test --config playwright.three-products.config.ts --grep 'M2 real mounted manual video drop' --list tests/e2e/local/three-products.spec.ts` — exactly 1 test collected.
- `node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-bootstrap-transport-assertion-repair/notes/vitest-runner.cjs node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism src/integrations/runtime/mediaImport.test.ts src/integrations/runtime/dataProvider.test.ts src/tools/video-editor/hooks/useAssetManagement.mediaImport.test.tsx` — 3 files, 84 tests passed.
- `git diff --check` — passed.
- Read-only lineage comparison against approved `d4c60b2` row and `e07d31f` drop helper — passed.

Per task scope, no browser run, central `request-test`, localhost/live-socket
run, or build was performed. The retained `real23319` evidence remains the
source for the genuine Runtime contract: import `201` with `entry.object_id`,
wrong verified selection refusal, and positive verified selection success.
Later recovery/undo assertions still require HOME's authorized browser gate.
