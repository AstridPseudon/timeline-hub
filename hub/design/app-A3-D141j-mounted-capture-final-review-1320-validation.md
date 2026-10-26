# Validation

- `node --import tsx --test --test-concurrency=1 tests/e2e/local/support/d141j-visibility.test.ts` — 6/6 passed.
- `./node_modules/.bin/vitest run --no-cache --config config/testing/vitest.config.ts src/tools/video-editor/components/TimelineEditor/TimelineEditorCore.test.tsx src/tools/video-editor/adapters/app/useAstridShotsHost.test.tsx src/tools/video-editor/hooks/useShotGroups.test.ts` — 3 files, 41/41 passed; only existing React `act(...)` warnings.
- `./node_modules/.bin/eslint tests/e2e/local/support/app.ts tests/e2e/local/support/d141j-visibility.ts tests/e2e/local/support/d141j-visibility.test.ts --report-unused-disable-directives --max-warnings 0` — pass.
- `./node_modules/.bin/tsc -p tsconfig.node.json --noEmit --pretty false` — pass.
- `./node_modules/.bin/tsc -p tsconfig.app.json --noEmit --pretty false` — pass.
- `git diff --check` — pass.
- Protected blob comparison against `ad651d89d3db583351a99d35cf791726b4c096bd` — all five protected blobs equal; candidate changes only `app.ts` and `d141j-visibility.test.ts`.

Not run by instruction: browser/native mounted run, Runtime/service/request/collection, D66, full suite, package/install/pin, or merge.
