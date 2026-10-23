# Handoff: app-F-opaque-opaque-roots-1054

Status: PASS

## Baseline

- Base: `7e0af6c9cda5a81a89505b006fcd653d4a5fc770`.
- Original focused command:
  `node node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --maxWorkers=2 src/tools/video-editor/commands/runner.test.ts`
- Baseline result: 1 test file failed; 12 failed / 15 total. Every failure reported an unexpected top-level key for `opaque` and `__proto__` before the intended clip/track/live-binding/shader diagnostic.

## Cause and repair

The mounted production caller is `runner.ts` -> `serialize.ts` -> `assertValidTimelineConfigSnapshot`. U3 changed the runner away from the existing `assertValidTimelineEditSnapshot` path, so internal command effects were checked by the closed top-level allowlist. Existing canonicalization and `cloneTimelineExtras` already preserve foreign roots, including null and omitted fields.

Changed `timeline-domain.ts` so the mounted assertion validates with the opaque-root-preserving mode. Safe foreign root names are retained; `__proto__`, `constructor`, and `prototype` are always refused with a distinct `unsafe_top_level_key` diagnostic. Nested opaque values are not traversed or rewritten by this root guard.

Added runner coverage for production data/config effects preserving an opaque array, null, and absence, plus explicit refusal coverage for all three unsafe root names. Existing malformed-field expectations were retained unchanged.

## Tests

- Focused runner after: 20 passed / 20; 1 file passed.
- Adjacent serializer/domain tests:
  `node node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --maxWorkers=2 src/tools/video-editor/lib/serialize.test.ts src/tools/video-editor/lib/timeline-domain.live-bindings.test.ts src/tools/video-editor/lib/timeline-domain.shaders.test.ts src/tools/video-editor/lib/timeline-domain.shot-groups.test.ts src/tools/video-editor/lib/timeline-domain.transition.test.ts`
  Result: 5 files passed; 70 tests passed / 70.
- App typecheck:
  `flock -w 600 /home/user/work/.app-tsc.lock env NODE_OPTIONS=--max-old-space-size=4096 ./node_modules/.bin/tsc --noEmit -p tsconfig.app.json --pretty false`
  Result: exit 0.
- Scoped lint:
  `./node_modules/.bin/eslint src/tools/video-editor/lib/timeline-domain.ts src/tools/video-editor/commands/runner.test.ts --max-warnings 0`
  Result: exit 0.
- Diff hygiene:
  `git diff --check`
  Result: clean.

## Touched paths

- `src/tools/video-editor/lib/timeline-domain.ts`
- `src/tools/video-editor/commands/runner.test.ts`

No runner implementation, executor, capture port, DTO, or unrelated product path was changed. Full/browser/journey suites were not run per task scope.

