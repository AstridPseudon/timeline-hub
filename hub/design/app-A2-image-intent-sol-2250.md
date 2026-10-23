Implemented A2 on base `e4ef3e62a4`.

- Changed only the prepared IMAGE handoff to emit `intent: {}`.
- Tightened the existing mounted regression to require an exactly empty policy. Exact `args.media`, metadata, retry, adoption, refusal, and dependent-trim assertions remain intact.
- Confirmed the policy against Agent registration and schema SHA-256 `d106dfe8212500709b4072d7bc0486f83c27d5d8de33d215cb52b9ea7d46357d`.

Validation used a private config/cache under `$TMPDIR`; its setup validates emitted `clip.add-media.intent` against the actual schema fragment.

```bash
node_modules/.bin/vitest run --config "$TMPDIR/vitest.config.ts" --configLoader=runner --no-cache src/tools/video-editor/hooks/useTimelineSave.test.tsx -t 'routes mounted shot prepared media'
```

Before fix: **5 failed, 1 passed, 45 filtered**, with schema rejection of `ownership`. After fix: **6 passed, 45 filtered**.

```bash
node_modules/.bin/vitest run --config "$TMPDIR/vitest.config.ts" --configLoader=runner --no-cache src/tools/video-editor/hooks/useTimelineSave.test.tsx src/tools/video-editor/hooks/timelineLocalSaveHandoff.test.ts src/tools/video-editor/hooks/useClipEditing.test.ts src/tools/video-editor/commands/localSaveSession.test.ts src/tools/video-editor/commands/localSaveSession.v2.test.ts src/tools/video-editor/commands/media.test.ts
```

**129 passed across 6 files.**

These commands also passed:

```bash
flock -w600 /home/user/work/.app-tsc.lock bash -c 'node_modules/.bin/tsc --noEmit -p tsconfig.json && node_modules/.bin/tsc --noEmit -p tsconfig.app.json && node_modules/.bin/tsc --noEmit -p tsconfig.node.json'
node_modules/.bin/eslint src/tools/video-editor/hooks/timelineLocalSaveHandoff.ts src/tools/video-editor/hooks/useTimelineSave.test.tsx --max-warnings 0
git diff --check
```

No blockers or plan deviations. Synthetic transport evidence only; no Python, live Runtime, browser, build, or full-suite acceptance claimed.

Commit message and `DONE` written. Next: independent Luna review, lane merge, then a new App producer packet for the reserved Agent fixture. Old `33934817` remains unchanged and unaccepted.