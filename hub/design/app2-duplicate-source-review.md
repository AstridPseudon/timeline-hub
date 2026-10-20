# D01-app-duplicate source handoff review

Reviewed App `tl/app-m2-refreshed-duplicate-source-port` at `85efd0ffa5cefc4ba38c63e0fb75e50258c5c28c`; the reviewed current root is `b1ef4b9b910ba72375c34cf319692f90d22edc25`. The frozen R4 SDK reference `origin/codex/handover-timeline-r4-20261019-candidate-sdk` is `11caf1d9de291d76f491cf69f7942606b7471d7a` and does not replace the current source decision.

## Decision

The exact Agent prerequisite for duplicate inverse is `68a51203310eb7c1bad343e50a42cf75c46c5321` (`tl/agt-m2-duplicate-reload-inverse-fix`), carried by merged descendant `9cb1090458428fb09067e359be92cdbb6608a206`. Do not qualify App duplicate against the older S2/current source pin `d8749a9ce12a699672faf3ad96b4e4cbea9245c2` alone. The repair records the compiler-derived destination `stable_deep_link` and `output_identity` in the duplicate occurrence create record, so accepted RAW data, reload, guarded inverse, redo, and retry agree. The Agent review reports 570 source tests plus 16 published-Runtime cases, with the unchanged parent still failing the six identity inverse cases; this is the necessary producer correction, not App activation evidence.

## Reusable App source and seam

- Keep `src/tools/video-editor/data/shotCompositionEditor.ts:duplicateIndependentShot`. It is the existing pure graph builder: clones the source revision/internal timeline, applies reserved shot/revision/occurrence IDs, preserves opaque raw child data, and uses `withOccurrenceIdentity` for the local graph.
- Keep `src/integrations/runtime/dataProvider.ts:toRuntimePublication`. It forwards the graph’s raw child payload and parent occurrence rows into the existing Runtime publication envelope; no new App DTO or identity field is needed.
- Keep `src/integrations/runtime/dataProvider.ts:RuntimeDataProvider.shotComposition.publish`. This is the App/Runtime boundary: project/timeline identity and CAS head validation, deterministic idempotency key, `/v1` publication, then exact committed-head reload. The handler should continue to call this port, not a placement writer.
- The Runtime/Agent owns authoritative compilation and inverse semantics. App must not “fix” identities after publication or supply a second identity scheme.

The current consumer is `src/tools/video-editor/components/AstridTimelineEditor.tsx:handleDuplicateDocumentShotGroup` (introduced by `f6c6453ef`). Its canonical branch is the reusable path:

```text
canonicalIdentity
  -> duplicateIndependentShot(contract, occurrenceId, reserved IDs)
  -> runtime.shots.shotComposition.publish({ expectedHeadRevisionId, graph })
  -> refetchShots()
```

The exact local-vs-App seam is therefore the pure graph function versus the `shotComposition.publish` port. The handler currently has a second branch that calls `duplicateShotGroup`, which is the legacy placement-document/pack-task writer and must remain reachable only until the canonical consumer is qualified.

## Raw identity inspection requirement

Do not use only `PreparedShotComposition.occurrences` or `runtimeGraphToContract()` as proof. `runtimeGraphToContract()` deliberately derives/replaces `stable_deep_link` and `output_identity` for the display graph. The acceptance probe must inspect the immutable Runtime payload before that adapter normalization:

- publication request: `POST /v1/projects/<project>/timelines/<timeline>/composition-revisions`, `body.parent_composition.occurrences[]`;
- committed read: `GET .../composition-revisions/<new-head>`, `payload.occurrences[]`;
- accepted closure if exposed by the provider: `canonical_document.parent_revision.payload.occurrences[]`.

For the copied occurrence, assert the raw values are derived from the actual destination shot/revision/occurrence and the escaped parent document ID, while source/sibling rows and opaque nested/output/task/association values remain byte-for-byte unchanged. This is the only meaningful App-side observation of the Agent repair; a normalized graph can conceal a bad stored identity.

## Smallest consumer cut after qualification

Against the reviewed App root, the bounded deletion is:

1. In `AstridTimelineEditor.tsx`, remove the `duplicateShotGroup` import and the fallback block in `handleDuplicateDocumentShotGroup` (the `projectSlug` check through the legacy success/error handling, current lines 422–444). Keep `configVersion` and `reloadFromServer`; the adjacent promote-primary handler still uses them.
2. In `src/tools/video-editor/lib/shot-group-pack-commands.ts`, once no consumer remains, delete only duplicate-only code: `DUPLICATE_SHOT_GROUP_FAMILY`, `DeepCopyShotGroupInput`, `DeepCopyShotGroupResult`, `safeIdPart`, `uniqueId`, `requireSourceGroup`, `sourceClipIds`, `destinationStart`, `deepCopyShotGroupInDocument`, `admitDuplicateShotGroupPackCommand`, `parseParams`, `finalVideoReplacementFromTask`, `mediaIdFromContentRef`, `sourceFinalVideo`, and `duplicateShotGroup`. Retain the shared promote-primary family, `packKey`, `waitForShotPackCommand`, and promote implementation.
3. Prune only duplicate-specific expectations/imports in `src/tools/video-editor/lib/shot-group-pack-commands.test.ts` and replace the consumer test in `src/tools/video-editor/components/AstridTimelineEditor.document-shots.test.tsx` with a canonical callback carrying `canonicalIdentity`; retain unrelated promote and shot-group behavior tests.

No deletion is justified yet in this source-review task. The native graph path must first pass the acceptance checks below, including zero legacy duplicate traffic.

## Existing tests and exact gaps

- `src/tools/video-editor/data/shotCompositionEditor.test.ts` covers in-memory linked/independent duplication and a generic history move/undo/redo. It does not publish the duplicate, reload it, or inverse the duplicate.
- `src/integrations/runtime/shotCompositionRuntime.test.ts` checks raw child timeline preservation and popup add/swap lost-ACK/reopen/exact retry. Its duplicate assertion only checks the copied internal timeline payload from `toRuntimePublication`; it does not commit a duplicate and inspect raw occurrence identities or inverse/redo.
- `src/tools/video-editor/components/AstridTimelineEditor.document-shots.test.tsx` exercises the legacy fallback: its mock duplicate callback omits `canonicalIdentity`, so it never exercises the canonical branch. There is no assertion that the canonical click emits no legacy writer/task traffic.
- `src/tools/video-editor/lib/shot-group-pack-commands.test.ts` covers the legacy helper’s media refusal and document-only copy, not canonical duplicate activation.
- Generic reload/retry/undo suites (`useTimelinePersistence.test.tsx`, `useTimelineHistory.test.ts`) do not establish duplicate graph durability. No existing test closes the combined duplicate `RAW compile -> immutable reload -> guarded undo -> redo -> exact retry -> zero legacy traffic` gap.

## Overlap / current status

The App status names `app-m3-current013-native-core-finalgate` and `app-m2-sevenjourney-native-agent-migration` as active qualification lanes, including the legacy-helper migration. That is the live overlap to coordinate with; this review makes no product/test changes and does not claim those lanes qualified. The status also says duplicate work is yielded to app2, while the Agent inverse repair remains a separate prerequisite. No App row is marked retired by this review.

## Acceptance commands

1. Agent producer gate at the repaired revision:

   ```sh
   cd /home/user/peteromallet/astrid-agent
   git show --no-patch --format='%H' 68a51203310eb7c1bad343e50a42cf75c46c5321
   PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q -c /dev/null -p no:cacheprovider tests/editing_conformance/test_recipe_occurrence_duplicate.py
   ```

2. App source/runtime targeted lane, after the runner-config blocker is resolved without touching shared caches:

   ```sh
   ./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache --configLoader=runner src/tools/video-editor/data/shotCompositionEditor.test.ts src/integrations/runtime/shotCompositionRuntime.test.ts src/tools/video-editor/components/AstridTimelineEditor.document-shots.test.tsx
   ```

3. The duplicate consumer regression should run as a targeted Vitest test in `AstridTimelineEditor.document-shots.test.tsx` plus `shotCompositionRuntime.test.ts`, asserting canonical callback routing, raw committed occurrence identities, exact retry body/idempotency key, reload/inverse/redo, and zero calls to `duplicateShotGroup`/legacy pack admission. Do not infer browser durability from this unit lane; the browser/three-products gate remains separate.

## Evidence and blocker

No App product or test files were changed. `git diff --check` is clean and the worktree remains clean. The required targeted Vitest command was attempted with `--no-cache --configLoader=runner` but stopped before collection with `ReferenceError: __dirname is not defined` from `config/testing/vitest.config.ts:14`; Vitest 4.1.5 also rejected the attempted `--cacheDir` CLI option. No dependencies, shared node_modules, shared caches, browser, socket, or full suite were run or changed.

