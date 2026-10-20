# Root clipOpacity import boundary

## Result

Blocked: no source change was retained. The requested root-import split is incompatible with the immutable public13 artifact present on the latest App base.

The actual public13 package (`vendor/artifacts/banodoco-timeline-composition-0.0.13.tgz`, SHA-256 `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`) exports `clipOpacity` from `dist/evaluation.js`, not from `dist/index.js`:

- installed root import: `typeof clipOpacity === 'undefined'`
- installed `/evaluation` import: `typeof clipOpacity === 'function'`
- `dist/index.d.ts`: no `clipOpacity` export
- `dist/evaluation.d.ts`: `export { clipOpacity } from './lib/clip-look.js'`

The proposed one-line split therefore fails the required behavior and hosted build. The original `/evaluation` import was restored unchanged. `VisualClip.tsx` already imports `getSanitizedPlaybackRate` from `/evaluation` and needed no edit.

## Exact introducing hunk

Commit `53adebfc4` (`refactor(viewing): delegate playback-rate sanitization to composition`) added `getSanitizedPlaybackRate` to the existing `playerEvaluation.ts` `/evaluation` import and removed the App wrapper. The relevant hunk is the import change shown in `PATCH.diff`; the current source has that hunk reverted to the public13-compatible form.

## Tests

- `npx vitest run --config config/testing/vitest.config.ts --no-cache src/tools/video-editor/compositions/playerEvaluation.test.ts src/tools/video-editor/compositions/VisualClip.evaluation.test.tsx src/tools/video-editor/compositions/VisualClip.test.tsx src/tools/video-editor/data/canonicalCompositionState.mainImageCap.test.ts` — PASS, 4 files / 60 tests.
- The requested root-import split under test — FAIL, 3 tests with `TypeError: clipOpacity is not a function`.
- `npm run build:hosted` with the requested root-import split — FAIL before output with Rollup `"clipOpacity" is not exported by .../timeline-composition/dist/index.js`.
- `npm run build:hosted` after restoring the actual public13-compatible import — PASS, 5,558 modules, 37.13s. Existing PostCSS/circular-chunk/large-chunk warnings only.

No package, lockfile, alias, fallback, test, or shared dependency was changed. The worktree is clean. The requested decision and the immutable artifact’s actual export map must be reconciled before a valid source patch can be landed.
