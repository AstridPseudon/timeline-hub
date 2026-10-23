Implemented A2 on base `e99cde635e83419d971b460d8e924127d671f626`. Only the two authorized files changed.

- Accepted-display config now uses the existing Runtime load defaults before assembly.
- Canonical data and the source guard remain unchanged.
- Mounted regression covers split ACK → Source In `{from: 3}` through handoff, session, outbox, and generated transport, including accepted/merged replies, absent fields, explicit nulls, paired heads, and unpadded authored payloads.

Validation:

```bash
node node_modules/vitest/vitest.mjs run --config "$TMPDIR/vitest.a2.config.mts" --configLoader=runner --no-cache src/tools/video-editor/hooks/useTimelineSave.test.tsx -t 'chains Source In after a mounted'
```

Old production code: **2 failed** at `checkSource`; **2 explicit-null controls passed**.

```bash
node node_modules/vitest/vitest.mjs run --config "$TMPDIR/vitest.a2.config.mts" --configLoader=runner --no-cache src/tools/video-editor/hooks/useTimelineSave.test.tsx src/tools/video-editor/hooks/useTimelineSave.recovery.test.tsx src/tools/video-editor/hooks/useTimelineSave.recovery.persistence.test.tsx src/tools/video-editor/hooks/timelineLocalSaveHandoff.test.ts src/tools/video-editor/hooks/timelineDeclaredReadChain.test.tsx src/tools/video-editor/hooks/useClipEditing.test.ts src/tools/video-editor/hooks/p1RawHandoffCorpus.test.ts
```

**124 passed across 7 files**, including existing mismatch-refusal coverage. Loader and cache stayed in `$TMPDIR`; shared dependencies were read-only.

```bash
flock -w 600 /home/user/work/.app-tsc.lock bash -c 'export NODE_OPTIONS=--max-old-space-size=4096; node node_modules/typescript/bin/tsc --noEmit && node node_modules/typescript/bin/tsc -p tsconfig.app.json --noEmit && node node_modules/typescript/bin/tsc -p tsconfig.node.json --noEmit'

node node_modules/eslint/bin/eslint.js src/tools/video-editor/hooks/useTimelineSave.ts src/tools/video-editor/hooks/useTimelineSave.test.tsx --max-warnings 0
git diff --check
```

All passed; scope check passed.

Decision: reuse the Runtime normalization expression on the display copy. No blockers or additional fixes. Synthetic transport coverage establishes App behavior; no browser, backend, or actual24510 rerun credit.

Independent cause audit reports **PASS**. Next: independent repair review before manager-controlled merge.

[commit-msg](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-A2-adoption-output-sol-2221/commit-msg) and [DONE](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-A2-adoption-output-sol-2221/DONE) created. No commit or merge performed.