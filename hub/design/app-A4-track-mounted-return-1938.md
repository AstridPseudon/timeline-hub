# A4 mounted track return — 1938

## Result

Repaired the independent 1932 findings in `src/tools/video-editor/hooks/useTimelineTrackManagement.persistence.test.tsx` only.

- The mounted harness now uses `RuntimeDataProvider` and `AstridRuntimeClient` with the generated Workspace transport.
- Accepted saves assert the exact commit route, serialized POST body, `Idempotency-Key`, accepted canonical closure, digests, base/previous/accepted pairs, authoritative commands/steps/`merge_mode`, and `receipt.result` equality.
- Structured 409 refusal asserts the contract envelope using `details.current` (no invented `details.head`) and preserves code, path, hint, and suggested command.
- Refusal revalidation adopts a distinct `remote-r2`/`remote-p2` canonical head while retaining the rejected durable intent.
- Existing capture tests and the same-order mounted no-op remain unchanged.

## Verification

- `NODE_OPTIONS="--import /tmp/w-5fbcb85e3b/app-A4-track-mounted-return-1938/vitest.dirname.mjs" node node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=2 src/tools/video-editor/hooks/useTimelineTrackManagement.persistence.test.tsx src/tools/video-editor/hooks/useTimelineTrackManagement.test.ts src/tools/video-editor/commands/trackReorderCapture.test.ts` — PASS, 3 files / 37 tests.
- `flock -w 600 /home/user/work/.app-tsc.lock env NODE_OPTIONS=--max-old-space-size=4096 ./node_modules/.bin/tsc --noEmit -p tsconfig.app.json --pretty false` — PASS.
- Same command with `-p tsconfig.node.json` — PASS.
- Same command with `-p tsconfig.json` — PASS.
- `node node_modules/eslint/bin/eslint.js src/tools/video-editor/hooks/useTimelineTrackManagement.persistence.test.tsx --max-warnings 0` — PASS.
- `git diff --check` — PASS.

No full, browser, live-socket, or integration suite was run.
