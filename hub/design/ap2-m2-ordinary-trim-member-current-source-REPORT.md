# Ordinary trim member integration

Implemented the missing App ordinary-batch dispatch for source-window trims.

- Added the ordinary trim adapter, reusing the existing native `captureClipTrim` / `executeClipTrim` builders. It keeps source-second arguments, native precision/guards/records, authored speed and opaque fields, and only admits the native parent clip identity; occurrence-owned trim members refuse without a fallback.
- Wired `clip.trim` membership into `genericPatchCapture` and its sequential executor. Supported batches produce one ordered command/record list; malformed or mixed unsupported batches fail during preflight before owner resolution or authored writes.
- Added the narrow native ordinary preview projection (`from`/`to`/`hold`) without changing the public TimelinePatch schema or wire types.
- Added focused exact-command/record, replay/opaque-preservation, malformed/occurrence refusal, mixed atomic refusal, and neighboring generic/session coverage.

## Verification

- `./node_modules/.bin/vitest run --no-cache --configLoader=runner --config config/testing/vitest.config.ts src/tools/video-editor/commands/ordinaryTrimMember.test.ts src/tools/video-editor/commands/genericPatchCapture.test.ts src/tools/video-editor/commands/clipTrimCapture.test.ts` — did not run tests; config loader failed because this repo config uses `__dirname`.
- `./node_modules/.bin/vitest run --no-cache --config config/testing/vitest.config.ts src/tools/video-editor/commands/ordinaryTrimMember.test.ts src/tools/video-editor/commands/genericPatchCapture.test.ts src/tools/video-editor/commands/clipTrimCapture.test.ts` — passed, 3 files / 77 tests.
- `./node_modules/.bin/vitest run --no-cache --config config/testing/vitest.config.ts src/tools/video-editor/commands/commitSession.genericPatch.test.ts src/tools/video-editor/commands/clipTrimGesture.test.ts src/tools/video-editor/commands/ordinaryScalarMember.test.ts src/tools/video-editor/commands/ordinaryMoveMember.test.ts` — passed, 4 files / 17 tests.
- `./node_modules/.bin/eslint src/tools/video-editor/commands/genericPatchCapture.ts src/tools/video-editor/commands/genericPatchCapture.test.ts src/tools/video-editor/commands/ordinaryTrimMember.ts src/tools/video-editor/commands/ordinaryTrimMember.test.ts --max-warnings 0` — passed.
- `git diff --check` — passed.

No full, browser, socket, activation, or central test-service suite was run, per task scope. No known blockers.

The expected `/home/user/work/app/STATUS.md` and `INBOX.md` were not present in the shared App integration worktree; the implementation was checked against the current integration source and settled plan.
