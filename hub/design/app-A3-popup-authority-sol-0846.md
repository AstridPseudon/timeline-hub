**FAIL — blocked by provider rebase.**

Imported only the three files from `63e3956746`. `media.ts` and `media.test.ts` remain byte-identical to that source. Added one offline fixture helper using real provider execution, complete effects/dependencies, compilation, and final validation.

Both mounted cases reach preparation → addClip → capture → outbox → RuntimeDataProvider → generated POST. Accepted adoption passes, including the durable complete canonical response. Merged fails in Agent `_commit_patch.py:910 → :843`: `binding_changed` on an intermediate fork revision after a disjoint parent metadata edit. The expectation remains an ordinary failure; no skips or expected failures.

Sources: App base `82cb5c0005`; Agent `67d5f19716d1e6b2f30445e14bfdcbf3927108de` (provider bytes unchanged from `0ff3d103`); Runtime imports `becfe6db88b2cc034dba3fafa6c050117cdf2b06`.

Final checks: **66 passed, 1 failed** — mounted 1/2, media 29/29, provider 36/36. Exact commands:

```bash
NODE_OPTIONS='--import=data:text/javascript,globalThis.navigator={};globalThis.__dirname=process.cwd()+String.fromCharCode(47,99,111,110,102,105,103,47,116,101,115,116,105,110,103)' PATH=/opt/node20/bin:$PATH /opt/node20/bin/node node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism src/tools/travel-between-images/components/ShotTimelinePreview.full-caller.a3.test.tsx src/tools/video-editor/commands/media.test.ts src/tools/travel-between-images/components/shotTimelineDataProvider.a3.test.ts

for config in tsconfig.json tsconfig.app.json tsconfig.node.json; do
  flock -w 600 /home/user/work/.app-tsc.lock env NODE_OPTIONS=--max-old-space-size=4096 /opt/node20/bin/node node_modules/typescript/bin/tsc -p "$config" --noEmit --pretty false --incremental false || exit $?
done

/opt/node20/bin/node node_modules/eslint/bin/eslint.js src/tools/video-editor/commands/media.ts src/tools/video-editor/commands/media.test.ts src/tools/travel-between-images/components/ShotTimelinePreview.full-caller.a3.test.tsx --max-warnings 0
git diff --check
```

All TypeScript, lint, and whitespace checks passed.

Fixture corrections supply complete reachable closure, valid digests/media identities, provider-supported authored timing, and an eight-second enclosure while retaining the five-second add and occupied V2 clip. Request reads remain absent; step dependencies come from native captures. D13 completeness beyond those captures is unproven.

Receipt, identity, import, and selection remain mocks; the media preview renderer is stubbed. No live authority, browser/backend/HTTP/full/build/provisioning ran.

Recommend an Agent fix for intermediate fork binding continuation, then rerun this gate before merge. Commit message and `BLOCKED` marker written; no `DONE`.