Repaired A2 on base `b2380539c5545661954d2794976631312ee1d939`.

The actual interaction: `7551` raw preservation restores `at_ms` after `rowsToConfig` serialization; prepared-media validation then rejects it as `unexpected_clip_key` on anchor and peer. The unchanged test passed with the pre-`7551` module, failed on the join, and passes with this repair. No historical `13583` causality is claimed.

Only `commands/media.ts` and its focused tests changed. Prepared-media preview now removes only a matching numeric `at_ms` alias before raw-field restoration. Contradictory aliases refuse. Original source data, raw capture, opaque fields, transitions, owner/read guards and outbox forwarding remain intact. The production command service calls this path.

Validation used Node `v20.20.0`, the existing resolver, private config/preload, and no shared caches:

```bash
NODE_OPTIONS="--import=$TMPDIR/preload.cjs" /opt/node20/bin/node node_modules/vitest/vitest.mjs run \
  --config "$TMPDIR/current.config.mjs" --configLoader runner --no-cache \
  --maxWorkers=1 --no-file-parallelism \
  src/tools/video-editor/commands/media.test.ts \
  src/tools/video-editor/lib/timeline-data.test.ts \
  src/tools/video-editor/lib/timeline-asset-plans.test.ts \
  src/tools/video-editor/hooks/useTimelineCommandsService.persistence.test.tsx \
  src/tools/travel-between-images/components/ShotTimelineMediaControls.test.tsx \
  src/tools/video-editor/hooks/useTimelinePersistence.test.tsx \
  src/tools/video-editor/hooks/timelineLocalSaveHandoff.test.ts \
  src/tools/video-editor/commands/localSaveSession.v2.test.ts \
  src/tools/video-editor/commands/parentAfterAnchorCapture.test.ts
```

**252 passed across nine files.** Includes mounted parent ready/delayed witnesses, occupied V2 popup placement, raw-track/disabled refusal, and raw `at_ms` refusal. Final standalone `media.test.ts` rerun: **26 passed**.

The original timing test was run with `--testNamePattern 'canonicalizes matching at_ms'`: pre-parent control **1 passed**, joined source **1 failed**, repaired source **1 passed**. Its body remains byte-for-byte unchanged.

```bash
for config in tsconfig.json tsconfig.app.json tsconfig.node.json; do
  flock /tmp/timeline-app-tsc.lock /opt/node20/bin/node node_modules/typescript/bin/tsc \
    --noEmit --incremental false -p "$config" || exit
done

/opt/node20/bin/node node_modules/eslint/bin/eslint.js \
  src/tools/video-editor/commands/media.ts \
  src/tools/video-editor/commands/media.test.ts --max-warnings 0

git diff --check
```

All passed. Protected-scope comparison passed; no cross-owned files changed.

No blockers. Commit message and `DONE` written. Next step: independent review. Browser/backend journeys and live Runtime acceptance remain unverified.