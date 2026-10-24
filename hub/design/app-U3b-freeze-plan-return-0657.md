# U3b corrected freeze plan

## Decision and refs

The freeze stays closed until P2/P3 GO is recorded.

Use these exact refs:

- Current App integration: `9b810408ccf8aadbca708dd0bc461afc19576427` (tree `9a37265f0286128df7e6240a9df9877d959474af`)
- Held draft: `7fc54e1f95ce`
- Draft/main base: `65c1771b78ab`
- Local upstream main: `2a288e629c47` — not live proof

The held draft is unsafe to replay wholesale: 687 reachable commits beyond `65c177`, 232 changed paths, and stale merge `81b6d4ce0d`. Do not merge it wholesale or cherry-pick its merge commits. `69099d6db7` is historical; the current reviewed tree is authoritative.

## Safe own-only packet

After P2/P3 GO, the lead must refresh refs and verify live `ls-remote` equality before any merge.

Starting from current `9b810`, create only worker-owned commits:

1. Provenance/caller-scope check each reviewed non-merge delta against current App:
   - Playwright discovery guard: `e546e5ac5f`
   - public-trim preflight: `f380c7be29`
   - reviewed P1 diagnostic composition: `e2e75b38e2`
   - reviewed diagnostic safety additions: `7fc54e1f95ce`

2. Port only the reviewed diagnostic/P1 paths whose current callers reach the existing A2 outbox and `commitTimeline` path. The `7fc54` diagnostic scope is limited to:

   - `src/tools/video-editor/hooks/timelineLocalSaveHandoff.ts`
   - `src/tools/video-editor/hooks/timelineLocalSaveHandoff.test.ts`
   - `src/tools/video-editor/hooks/useTimelinePersistence.ts`
   - `src/tools/video-editor/hooks/useTimelineSave.ts`
   - `src/tools/video-editor/hooks/useTimelineSave.test.tsx`
   - `src/tools/video-editor/lib/timeline-diagnostics.ts`
   - `src/tools/video-editor/lib/timeline-diagnostics.save.test.ts`
   - `tests/e2e/local/p1-diagnostic-safety.ts`
   - `tests/e2e/local/p1-diagnostic-safety.test.ts`
   - `tests/e2e/local/mounted-readiness-safety.ts`
   - `tests/e2e/local/mounted-readiness-safety.test.ts`
   - `tests/e2e/local/three-products.p1-chain.spec.ts`
   - `tests/e2e/local/three-products.mounted-readiness.spec.ts`
   - `tests/e2e/local/three-products.p2-popup.spec.ts`

3. Requalify serializer/label overlap against current integration before porting any hunk. Current files remain authoritative, especially `serialize.ts`, `timeline-data.ts`, `timeline-mutation-engine.ts`, `useTimelineCommit.ts`, and AgentChat label handling. Do not import `7978ed829e`, `81b6d4ce0d`, or `14d4acd749` wholesale.

4. Every packet commit gets its own review. No merge commit is replayed blindly.

## Upstream merge inventory

The held/current overlap is:

- `src/tools/video-editor/hooks/useTimelineCommit.ts`
- `src/tools/video-editor/lib/timeline-data.ts`
- `src/tools/video-editor/lib/timeline-data.test.ts`
- `tests/e2e/local/support/app.ts`
- `tests/e2e/local/support/harness.ts`

Only `harness.ts` has a textual held/current conflict.

The refreshed upstream merge has 10 conflict hunks across these nine paths:

1. `config/testing/vitest.astrid-renderer.config.ts`
2. `package.json` — two hunks
3. `src/tools/video-editor/components/AgentChat/AgentChat.tsx`
4. `src/tools/video-editor/components/AgentChat/AgentChatMenu.test.tsx`
5. `src/tools/video-editor/components/AgentChat/AgentChatMenu.tsx`
6. `src/tools/video-editor/hooks/useTimelineCommit.ts` — two hunks
7. `src/tools/video-editor/tour/runner/useEditorTourTrigger.ts`
8. `tests/e2e/local/support/harness.ts`
9. `supabase/functions/_tests/mocks/groqSdk.ts` — added in both; reconcile one implementation, never duplicate it

All 22 changed-in-both paths are those nine plus:

- `README.md`
- `config/testing/vitest.boundary.config.ts`
- `config/testing/vitest.config.ts`
- `config/vite/vite.config.ts`
- `public/install`
- `scripts/dev-local-workspace.mjs`
- `src/app/main.bootstrap-order.test.tsx`
- `src/integrations/runtime/client.ts`
- `src/shared/components/SettingsModal/sections/ConnectionSection.tsx`
- `src/tools/video-editor/commands/runner.ts`
- `src/tools/video-editor/components/AgentChat/AgentChat.hosted.test.tsx`
- `src/tools/video-editor/pages/VideoEditorPage.test.tsx`

Resolve semantically:

- Preserve current outbox, gesture basis, prepared-media, opaque/raw source, catalog, parameter, popup, parent, timing, door, and `690` real-caller fixes.
- Combine current door/lifecycle harness controls with upstream skip-condition controls.
- Adopt upstream native/offline setup only where non-overlapping.
- Do not resurrect `NewChatMenu`, `TourChatPanel`, old tour manifests, or retired extension routes.
- Retain the current AgentChat contract while adopting compatible selector UI.
- Combine `package.json`, Vitest aliases, `useTimelineCommit`, and harness changes; do not choose either side wholesale.

## D31/D37 retention

Reviewer wording is broader than the actual settled scope.

Retain unchanged:

- Literal transcript subset: `src/tools/video-editor/commands/transcriptAssociateCapture.ts`, its test, and required helpers. The test remains exactly 397 lines with 40 assertions. Production transcript flow remains through `project-transcript-host.ts` and `useProjectTranscriptHost.ts`.
- Raw-birth subset: `src/tools/video-editor/commands/parentAfterAnchorCapture.ts` and its test.
- Same-order track implementation: `src/tools/video-editor/commands/trackReorderCapture.ts` and its test.

Also retain the current dormant rows exactly as recorded in `design/deletion-ledger.app.md:69-74` and `design/deletion-ledger.md:31-35`:

- `APP-A4-D37-SESSION-CHAIN`
- `APP-A4-D37-NATIVE-LABEL`
- `APP-A4-D37-EXECUTOR`
- `APP-A4-D37-RAW-BIRTH`
- `APP-A4-D37-TRACK`

They remain dormant, unchanged, owner-review follow-ups. Do not add provider migrations, new operations, or a new A4 scope. Do not restore production legacy writers. The old-writer census must establish production reachability; absence of literal `D31`/`D37` strings is not evidence.

## Actual final dependency order

1. P2/P3 GO.
2. Lead refreshes live refs and verifies equality.
3. Port and independently review only the own diagnostic/P1 packet.
4. Perform the sanctioned App upstream merge from refreshed main.
5. Requalify current A2/outbox behavior, Runtime door authorization, prepared-media timing, opaque/raw/source retention, catalog/parameter/popup/parent callers.
6. After actual Agent U4a is merged, re-vendor `astrid-browser` through the normal provenance-producing tool.
7. Adopt the Runtime D39 canonical producer, generated client, and schema once; no new contract and no pin churn.
8. Complete App U4p from that exact generated output.
9. Run the 27-file union, Gate-5 controls, three serialized typechecks, scoped lint, old-writer census, and Playwright discovery.
10. Run authorized full suites, final P1–P3 gates, Farm delivery build, and final validation.

The production C0v2 request must retain:

`api_version`, `project_id`, `timeline_id`, `base_revision_id`, `base_publication_id`, `commands`, `label`, `steps` with `id`, `label`, `intent`, `tags`, `command_ordinals`, `patch`, `reads`, `merge`, `reads`, `Idempotency-Key`, `dry_run`, `source`, `rationale`, `group_id`.

Replies remain `{data, receipt}` with `accepted`, `merged`, or historical `rebased`; `canonical_document`, `document_digest`, `id_map`, `records`, `dependencies`, `effects`, `steps`, `history`, `undo_steps`, `preview`, `required`, `would_status`; conflicts include `reason` and `head`; invalid replies include `code`, `path`, `hint`, and `suggested_command`.

## Acceptance commands

Exact 27-file union:

```bash
/opt/node20/bin/node node_modules/vitest/vitest.mjs run \
  --config config/testing/vitest.config.ts \
  --configLoader runner --no-cache --maxWorkers=1 --no-file-parallelism \
  src/tools/video-editor/lib/timeline-data.test.ts \
  src/tools/video-editor/lib/serialize.test.ts \
  src/tools/video-editor/lib/time-grid-conformance.test.ts \
  src/tools/video-editor/hooks/useClipDrag.test.tsx \
  src/tools/video-editor/hooks/useTimelineCommit.test.tsx \
  src/tools/video-editor/hooks/useTimelinePersistence.test.tsx \
  src/tools/video-editor/hooks/timelineLocalSaveHandoff.test.ts \
  src/tools/video-editor/commands/localSaveSession.v2.test.ts \
  src/tools/video-editor/commands/localSaveSession.replayProtocol.test.ts \
  src/tools/video-editor/lib/timeline-asset-plans.test.ts \
  src/tools/travel-between-images/components/ShotTimelineMediaControls.test.tsx \
  src/tools/video-editor/commands/media.test.ts \
  src/tools/video-editor/hooks/useAssetManagement.assetDrop.test.ts \
  src/tools/video-editor/hooks/useExternalDrop.test.tsx \
  src/tools/video-editor/contexts/VideoEditorProvider.test.tsx \
  src/tools/travel-between-images/components/shotTimelineDataProvider.a3.test.ts \
  src/tools/video-editor/hooks/useTimelineCommandsService.persistence.test.tsx \
  src/tools/video-editor/hooks/useClipEditing.test.ts \
  src/tools/video-editor/hooks/useTimelineSave.test.tsx \
  src/tools/video-editor/components/PropertiesPanel/AstridElementParams.test.tsx \
  src/tools/video-editor/components/PropertiesPanel/ClipEffectsTab.test.tsx \
  src/tools/video-editor/components/PropertiesPanel/PropertiesPanel.test.tsx \
  src/tools/video-editor/contexts/VideoEditorProvider.staging.test.tsx \
  src/tools/video-editor/runtime/element-adapter.test.ts \
  src/tools/video-editor/commands/localSaveSession.recoveryBasis.test.ts \
  src/tools/video-editor/components/PropertiesPanel/PropertiesPanel.mounted.test.tsx \
  src/tools/video-editor/components/ElementsLibraryPanel.test.tsx
```

Gate-5 controls:

```bash
/opt/node20/bin/node --import tsx --test \
  tests/e2e/local/support/gate5-reset-precondition.test.mjs
```

Serialized typechecks:

```bash
/opt/node20/bin/node node_modules/typescript/bin/tsc --noEmit --incremental false -p tsconfig.json
/opt/node20/bin/node node_modules/typescript/bin/tsc --noEmit --incremental false -p tsconfig.app.json
/opt/node20/bin/node node_modules/typescript/bin/tsc --noEmit --incremental false -p tsconfig.node.json
```

Scoped lint and hygiene:

```bash
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
npm run check:astrid-conformance
```

Old-writer census:

```bash
rg -n -I \
  'saveTimelineAtHead|saveTimeline|publishParentComposition|document_diff|three_way|commands-file|apply --native|undo --publication|/composition-revisions' \
  src scripts tests --glob '!**/*.test.*'
```

Playwright discovery:

```bash
/opt/node20/bin/node node_modules/@playwright/test/cli.js test \
  --config playwright.three-products.config.ts \
  tests/e2e/local/three-products.spec.ts --list
```

Expected discovery remains P1=2, P3=1, P2=8, mounted-readiness=1. Full browser, live HTTP, backend, and Farm runs are central-service/Farm work only.

## Execution status

No repository files, tests, merges, refs, specs, ledgers, or reports were changed. No tests were run for this plan-only task. The worktree is clean; `DONE` and the required commit message were created.