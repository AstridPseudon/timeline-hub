Completed A3 qualification in `VideoEditorProvider.staging.test.tsx`.

- Added exact `am-burst` / `effect` / `astrid_motion` tile Apply coverage through the real editor, A2 handoff, persisted outbox, and production commit transport.
- Verified one intended insertion, request metadata, persisted idempotency key, accepted-head adoption, and raw closure preservation.
- Restored `registry.opaque.keep: null`. Preserved existing assertions and refusals.
- Reproduced OLD missing-capture RED: “The captured timeline head changed or is missing.” Restored caller: GREEN.

Validation:

```bash
NODE_OPTIONS=--import=/tmp/w-3e4c955876/a3-preload.mjs /opt/node20/bin/node node_modules/vitest/vitest.mjs run --config /tmp/w-3e4c955876/a3-vite.config.ts --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/components/ElementsLibraryPanel.test.tsx src/tools/video-editor/runtime/element-adapter.test.ts src/tools/video-editor/contexts/VideoEditorProvider.staging.test.tsx
```

**3 files, 31 tests passed.** OLD RED used the same configuration with staging only and `-t 'applies the original am-burst'`.

```bash
flock -w 600 /home/user/work/.app-tsc.lock bash -c 'set -e; for project in tsconfig.json tsconfig.app.json tsconfig.node.json; do /opt/node20/bin/node node_modules/typescript/bin/tsc --noEmit --incremental false -p "$project" --pretty false; done'
```

**All three passed.** Scoped ESLint `--max-warnings 0`, `git diff --check`, and protected-file census passed.

Decision: retained generic text-card/transition coverage and added the mandatory exact witness. No production guards changed. No blockers. Browser/backend/full suites remain unverified as instructed.

Commit message and `DONE` written. Recommended next step: independent review.