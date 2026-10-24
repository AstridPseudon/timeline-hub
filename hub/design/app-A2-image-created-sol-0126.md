Completed A2 on `tl/app-A2-image-created-sol-0126`, based on `f7102bf4debe8e95b06c430f204a16cd6a37630a`.

Final source tree: `f83baace65ead931c346e3baf2b1b1a7fd2ea43d` (computed without Git writes).

- Changed only `timelineLocalSaveHandoff.ts` and `preparedImageRequestProducer.test.ts`.
- Image `clip.add-media` now claims `parent/asset:${row.asset}` only when absent from the pre-edit authored registry, then always claims `parent/clip:${row.id}`. This matches provider allocation order: `_registry(..., alias=row['asset'])` → clip creation.
- **Identity decision:** mounted tests demonstrate supported aliases where `row.asset !== media.asset`. Claims therefore use the actual row alias; the exact five-field media selection remains unchanged.
- Added six controls covering existing registration, new/existing aliases, forged asset/clip identity and clip collision. Strengthened raw opaque data, complete child closure and input immutability assertions. Existing behavior assertions remain.
- Preserved request metadata, reads, steps, intent `{}`, canonical adoption, refusal and retry handling. Old 0043 evidence was untouched.

Validation used Node `v20.20.0`, private `TMPDIR=/tmp/w-1eb212c91b`, and an owned preload setting `__dirname` to this worktree’s `config/testing`.

```bash
PATH=/opt/node20/bin:/usr/local/bin:/usr/bin:/bin \
NODE_OPTIONS=--import=/tmp/w-1eb212c91b/vitest-dirname.mjs \
/opt/node20/bin/node node_modules/vitest/vitest.mjs run \
--config config/testing/vitest.config.ts --configLoader=runner \
--no-cache --maxWorkers=2 \
src/tools/video-editor/hooks/timelineLocalSaveHandoff.test.ts \
src/tools/video-editor/commands/localSaveSession.test.ts \
src/tools/video-editor/commands/localSaveSession.v2.test.ts \
src/tools/video-editor/commands/fixtures/preparedImageRequestProducer.test.ts \
src/tools/video-editor/hooks/useTimelineCommandsService.persistence.test.tsx \
src/tools/video-editor/hooks/useTimelinePersistence.test.tsx \
src/tools/video-editor/hooks/useTimelineSave.test.tsx
```

**PASS: 7 files, 261 tests.** After a final test-only isolation correction, reran the same command with only `preparedImageRequestProducer.test.ts`: **28/28 passed**.

Each following command passed separately for `tsconfig.app.json`, `tsconfig.node.json`, and `tsconfig.json`:

```bash
flock -w 600 /home/user/work/.app-tsc.lock env -u NODE_PATH \
PATH=/opt/node20/bin:/usr/local/bin:/usr/bin:/bin \
NODE_OPTIONS=--max-old-space-size=4096 \
/opt/node20/bin/node node_modules/typescript/bin/tsc \
--noEmit --incremental false -p <config> --pretty false
```

Also passed:

```bash
PATH=/opt/node20/bin:/usr/local/bin:/usr/bin:/bin \
/opt/node20/bin/node node_modules/eslint/bin/eslint.js \
src/tools/video-editor/hooks/timelineLocalSaveHandoff.ts \
src/tools/video-editor/commands/fixtures/preparedImageRequestProducer.test.ts \
--max-warnings 0
git diff --check
git diff --name-only
```

No new external producer interface: existing canonical document/head/prepared-asset/placement input and request/idempotency-key/hash output remain unchanged.

No blockers. `A2:` commit message and `DONE` marker written. No commit, merge, service, browser, Runtime call or full suite ran. Mock acceptance establishes the App protocol boundary only; Python acceptance and further record validation remain unverified. Recommended next step: independent source review, then Agent-owned boundary qualification on a newly authorized fixture.