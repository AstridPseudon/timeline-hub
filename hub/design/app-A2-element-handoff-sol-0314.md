Implemented A2/A4: registered element operations use the mounted handoff → persisted localSaveSession/outbox → commitTimeline. Removed adapter calls to both legacy save methods.

Preserved raw parent data, full child closure, canonical reply adoption, refusal retention, and supported browser persistence. Captured turns check publication, revision, scope, and local previews. Element reads come from operation inputs; captures use atomic merge. D31/D37 remain unchanged.

Validation:

```sh
N=/opt/node20/bin/node
$N --import /tmp/w-ddbb3183f0/vitest-dirname.mjs node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=2 src/tools/video-editor/runtime/element-adapter.test.ts src/tools/video-editor/contexts/VideoEditorProvider.test.tsx src/tools/video-editor/contexts/VideoEditorProvider.staging.test.tsx src/tools/video-editor/hooks/timelineLocalSaveHandoff.test.ts src/tools/video-editor/hooks/useTimelineSave.test.tsx
```

**5 files, 221 tests passed.**

- OLDRED: same mounted cases with the original handoff injected via `/tmp/w-ddbb3183f0/oldred.config.ts`: **4 failed at the child-ownership guard**.
- Each of `tsconfig.json`, `tsconfig.app.json`, `tsconfig.node.json` passed:
  `flock -w 600 /home/user/work/.app-tsc.lock env NODE_OPTIONS=--max-old-space-size=4096 /opt/node20/bin/node node_modules/typescript/bin/tsc --noEmit --incremental false -p <config> --pretty false`
- Passed: `/opt/node20/bin/node node_modules/eslint/bin/eslint.js $(git diff --name-only -- '*.ts' '*.tsx') --max-warnings 0`
- `git diff --check` passed; caller census found no legacy save calls in adapter/provider registration.

No blockers. Commit message and `DONE` written. Next: integration review. Runtime commits were stubbed; no full, browser, backend, or service runs performed.