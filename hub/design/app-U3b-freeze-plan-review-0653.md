# U3b freeze-plan review — FAIL pending correction

Read-only review complete. Worktree remains clean; no product/test/spec/design changes.

The prior plan’s whole-branch “held draft first” recommendation is unsafe:

- Held draft has 7 first-parent commits, but 687 reachable commits beyond `65c1771b78ab`.
- From common ancestor `7417b53c456a`, it changes 232 paths: `133 M / 76 A / 22 D / 1 R`, `+6359/-2794`.
- It includes a stale upstream-main merge (`81b6d4ce0d`) and broad editor/onboarding/tour changes. Do not merge it wholesale or blindly cherry-pick its merge commits.
- Port only reviewed diagnostic/P1 deltas, then re-review label/serializer changes against current integration.

## Verified refs and delta

- Current integration: `9b810408cc`
- Held draft: `7fc54e1f95ce`
- Draft/main base: `65c1771b78ab`
- Local `origin/main`: `2a288e629c47`
- Upstream delta: 18 commits, 111 paths, `+3900/-1357`
- Counts: 76 modified, 25 added, 9 deleted, 1 renamed

Live `ls-remote` equality was not verified. The lead must refresh refs and compare live `origin/main` immediately before merging; local `2a288e629c47` is not live proof.

## Held-draft overlap

Five paths overlap current integration:

- `src/tools/video-editor/hooks/useTimelineCommit.ts`
- `src/tools/video-editor/lib/timeline-data.ts`
- `src/tools/video-editor/lib/timeline-data.test.ts`
- `tests/e2e/local/support/app.ts`
- `tests/e2e/local/support/harness.ts`

Only `tests/e2e/local/support/harness.ts` produces a textual conflict.

## Current-vs-main conflict inventory

`git merge-tree` reports 10 conflict hunks across these 9 paths:

1. `config/testing/vitest.astrid-renderer.config.ts`
2. `package.json` — two hunks
3. `src/tools/video-editor/components/AgentChat/AgentChat.tsx`
4. `src/tools/video-editor/components/AgentChat/AgentChatMenu.test.tsx`
5. `src/tools/video-editor/components/AgentChat/AgentChatMenu.tsx`
6. `src/tools/video-editor/hooks/useTimelineCommit.ts` — two hunks
7. `src/tools/video-editor/tour/runner/useEditorTourTrigger.ts`
8. `tests/e2e/local/support/harness.ts`
9. `supabase/functions/_tests/mocks/groqSdk.ts` — added in both

All 22 changed-in-both paths:

- `README.md`
- `config/testing/vitest.astrid-renderer.config.ts`
- `config/testing/vitest.boundary.config.ts`
- `config/testing/vitest.config.ts`
- `config/vite/vite.config.ts`
- `package.json`
- `public/install`
- `scripts/dev-local-workspace.mjs`
- `src/app/main.bootstrap-order.test.tsx`
- `src/integrations/runtime/client.ts`
- `src/shared/components/SettingsModal/sections/ConnectionSection.tsx`
- `src/tools/video-editor/commands/runner.ts`
- `src/tools/video-editor/components/AgentChat/AgentChat.hosted.test.tsx`
- `src/tools/video-editor/components/AgentChat/AgentChat.tsx`
- `src/tools/video-editor/components/AgentChat/AgentChatMenu.test.tsx`
- `src/tools/video-editor/components/AgentChat/AgentChatMenu.tsx`
- `src/tools/video-editor/hooks/useTimelineCommit.ts`
- `src/tools/video-editor/lib/timeline-data.test.ts`
- `src/tools/video-editor/lib/timeline-data.ts`
- `src/tools/video-editor/pages/VideoEditorPage.test.tsx`
- `tests/e2e/local/support/app.ts`
- `tests/e2e/local/support/harness.ts`

Added in both:

- `supabase/functions/_tests/mocks/groqSdk.ts`

## Preserved current anchors

The current tree contains the reviewed compatibility and save-path anchors:

- `src/integrations/runtime/clientLocalAdapter.ts:54-59, 95-143` — pinned Runtime operation adapter and task reservation cleanup.
- `src/tools/video-editor/hooks/useTimelineCommit.ts:75-106, 401-405` — single mutation vocabulary, gesture basis, outbox scheduling.
- `src/tools/video-editor/hooks/timelineLocalSaveHandoff.ts:24-43, 54-72` — original verified basis and scoped persistence binding.
- `src/tools/video-editor/hooks/useTimelineSave.ts:60-83, 29-32` — element parameter ownership and local-save/outbox wiring.
- Current catalog, params, popup, parent, and timing fixes are present in the current integration ancestry, including `b2380539c5`, `1d9d2c8453`, `79cd94f7e0`, `0267ed4f03`, `5e242c64e3`, and `9b810408cc`.

`69099d6db7` is an ancestor of current integration, not an external unqualified tree. Its adapter files remain present, but five of its six touched files changed later; preserve the current versions, not the old commit blobs.

No literal `D31`/`D37` identifiers exist in source. The current concrete anchors are:

- D31-equivalent: dormant `src/tools/video-editor/commands/transcriptAssociateCapture.ts` plus its test; production transcript flow is through `project-transcript-host.ts` and `useProjectTranscriptHost.ts`.
- D37-equivalent: existing `commitSession*.test.ts` and replay/generic-patch declarations. Keep these unchanged until the old-writer census proves a faithful current replacement.

## Recommended merge order

1. Keep freeze gate CLOSED until P2/P3 GO.
2. Lead refreshes all refs and verifies live `ls-remote` equality.
3. Start from current `9b810408cc`.
4. Port only reviewed held-draft diagnostics/P1 changes. Exclude the held draft’s stale upstream-main merge and broad onboarding/tour/editor replay.
5. Resolve held/current harness by combining current Runtime door/lifecycle controls with upstream skip-condition controls.
6. Merge refreshed App main last, but resolve semantically:
   - preserve current outbox, gesture-basis, prepared-media, opaque/raw, catalog/params/popup/parent/timing behavior;
   - adopt upstream native/offline setup controls where non-overlapping;
   - do not resurrect retired `NewChatMenu`, `TourChatPanel`, old tour manifests, or retired extension routes;
   - retain current `AgentChat` contract while adopting only compatible upstream selector UI;
   - combine, rather than choose wholesale, `package.json`, Vitest aliases, `useTimelineCommit`, and harness changes.
7. After actual Agent U4a exists, re-vendor `astrid-browser` through the normal provenance-producing tool. Adopt D39 generated client/schema/producer outputs once; do not churn pins.
8. Run targeted checks, then Runtime final tuple/U4p, then original P1–P3 and Farm gates.

## Required post-merge commands

Not run in this review.

```bash
node_modules/.bin/vitest run \
  --config config/testing/vitest.config.ts \
  --configLoader=runner --no-cache --maxWorkers=2 \
  src/tools/video-editor/lib/timeline-data.test.ts \
  src/tools/video-editor/hooks/useTimelineCommit.test.tsx \
  src/tools/video-editor/hooks/timelineLocalSaveHandoff.test.ts \
  src/tools/video-editor/hooks/useTimelinePersistence.test.tsx \
  src/tools/video-editor/hooks/useTimelineSave.test.tsx \
  src/tools/video-editor/lib/timeline-diagnostics.save.test.ts \
  src/integrations/runtime/clientLocalAdapter.test.ts \
  src/integrations/runtime/dataProvider.test.ts \
  src/integrations/runtime/operationHost.test.ts \
  src/integrations/runtime/bootstrapInitialization.test.ts
```

```bash
node --import tsx --test --test-concurrency=1 \
  tests/e2e/local/p1-diagnostic-safety.test.ts \
  tests/e2e/local/mounted-readiness-safety.test.ts \
  tests/e2e/local/support/quick-descriptor.test.ts \
  scripts/astrid-landing/offline-verifier/verify.test.mjs \
  scripts/dev-local-workspace.test.mjs \
  scripts/node-package-manager.test.mjs
```

```bash
npx tsc -p tsconfig.json --noEmit --incremental false
npx tsc -p tsconfig.app.json --noEmit --incremental false
npx tsc -p tsconfig.node.json --noEmit --incremental false
npx eslint \
  config/testing/vitest.astrid-renderer.config.ts \
  config/testing/vitest.boundary.config.ts \
  config/testing/vitest.config.ts \
  config/vite/vite.config.ts \
  scripts/dev-local-workspace.mjs \
  src/integrations/runtime/client.ts \
  src/tools/video-editor/commands/runner.ts \
  src/tools/video-editor/hooks/useTimelineCommit.ts \
  src/tools/video-editor/lib/timeline-data.ts \
  tests/e2e/local/support/app.ts \
  tests/e2e/local/support/harness.ts \
  --max-warnings 0
git diff --check
```

Before A4 deletion, run the old-writer census:

```bash
rg -n -I 'saveTimelineAtHead|saveTimeline|publishParentComposition|document_diff|three_way|commands-file|apply --native|undo --publication|/composition-revisions' \
  src scripts tests --glob '!**/*.test.*'
```

Verify generated adoption with:

```bash
npm run check:astrid-conformance
git diff --check
```

Full backend/browser/live runs, `npm run test:e2e:three-products`, `npm run test:e2e:direct`, and final P1–P3/F gates remain Farm/central-test-service work only.