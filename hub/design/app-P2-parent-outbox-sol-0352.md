Added four offline controls in [useTimelinePersistence.test.tsx](/home/user/work/wt/app-P2-parent-outbox-sol-0352/src/tools/video-editor/hooks/useTimelinePersistence.test.tsx:268), using the production persistence hook, handoff and persisted session.

- Mirrored parent-only move passes: exact `at: 0 → 5` patch, captured base pair, durable acceptance and canonical adoption.
- Both child-closure cases fail before `appendDocument()` with `child ownership/fork mapping is unavailable`.
- Top-level-only clips separately fail with `authored collection is unavailable: config/clips`.
- Preserved success expectations as three `it.fails` cases. No existing behavior test was weakened.

**No production repair claimed.** The required changes are outside my ownership in `timelineLocalSaveHandoff.ts`: narrow both child guards at lines 237/396 for verified parent-only moves; extend top-level clip mapping and original read paths at lines 243/413–471. Simply deleting the guards is insufficient.

Validation, using Node 20.20.0 and private configuration/cache:

- Vitest prefix: `/opt/node20/bin/node --import /tmp/w-ab5b0870c4/vitest-preload.mjs /home/user/work/app/node_modules/vitest/vitest.mjs run --config /tmp/w-ab5b0870c4/vitest.config.mts --configLoader runner --no-cache`
- Prefix + `src/tools/video-editor/hooks/useTimelinePersistence.test.tsx -t 'P2 parent move'`, before expected-failure markings: **1 passed, 3 failed** at the named boundaries.
- Prefix + persistence, handoff, and seven `localSaveSession` test files: **9 files passed; 171 passed, 3 expected failures**.
- Final prefix + `src/tools/video-editor/hooks/useTimelinePersistence.test.tsx`: **87 passed, 3 expected failures**.
- `flock -w 300 /home/user/work/.app-tsc.lock /opt/node20/bin/node /home/user/work/app/node_modules/typescript/bin/tsc --noEmit --incremental false -p <config>`: individually passed for `tsconfig.json`, `tsconfig.app.json`, `tsconfig.node.json`.
- `/opt/node20/bin/node /home/user/work/app/node_modules/eslint/bin/eslint.js src/tools/video-editor/hooks/useTimelinePersistence.test.tsx --max-warnings 0`: passed.
- `git diff --check`: passed.

Read the original assertion and bounded retained trace metadata/errors without request, body or environment dumps. Actual `12221` rejection attribution remains **UNKNOWN**; retained verdict stays **3 failed / 5 NOTRUN**, with no P2 credit. Next evidence needed: the mounted capture rejection code and append/dispatch reachability under matching captured/current heads.

Commit message and empty `DONE` marker written. No browser, backend, full suite or shared dependency changes.