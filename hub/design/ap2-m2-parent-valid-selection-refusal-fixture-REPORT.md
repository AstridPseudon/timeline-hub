# AP2 M2 parent valid-selection refusal fixture

## Result

Repaired the wrong-selection fixture in `tests/e2e/local/three-products.spec.ts` only. The mounted manual-drop route now asserts the real `object_id` has the Runtime digest shape and flips exactly one hex digit, preserving the other selection fields. The negative assertion remains `[404, 409]`; no product, API, schema, pin, dependency, or shared-source change was made.

## Validation

- `git diff --check` — passed.
- `npx eslint tests/e2e/local/three-products.spec.ts --ext ts --max-warnings 0` — passed.
- `npx vitest run --config config/testing/vitest.config.ts --no-cache --configLoader=bundle --maxWorkers=2 --no-file-parallelism src/tools/video-editor/commands/parentClipAddCapture.test.ts src/integrations/runtime/dataProvider.test.ts src/integrations/runtime/mediaImport.test.ts` — passed, 3 files / 86 tests.
- `npx playwright test --config playwright.three-products.config.ts --grep 'M2 real mounted manual video drop' --list tests/e2e/local/three-products.spec.ts` — passed, 1 test collected.

The first attempted Vitest command used `--configLoader=runner` and failed before test collection because this repository's config uses `__dirname`; it was rerun with the default bundled loader and `--no-cache`.

## Central harness

Requested exactly once:

`ap2-m2-parent-valid-selection-refusal-fixture-ap2-m2-parent-drop-real-central-qualification-1020205301-29398`

The existing parent-drop wrapper selected only the mounted manual-drop test. It passed the repaired negative refusal assertion (the run advanced beyond line 1172), then failed later at line 1208 after 90 seconds because the positive path produced no intercepted native commit (`wire.posts.length` stayed 0). This later positive-path failure is unverified as a fixture issue and was not addressed with product changes.

No full suite, local browser, localhost, socket, or dirty-source run was performed.

## Decision

A dynamic one-hex-digit mutation was used instead of a hard-coded digest so the fixture remains a valid mismatch against the actual imported object while retaining the original request's other fields. Existing Runtime tests continue to cover malformed digest refusal; the e2e assertion was not loosened.
