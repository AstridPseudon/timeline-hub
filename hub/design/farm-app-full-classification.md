# App full-suite failure classification (tf-app-classify)

**Status: CLASSIFIED: full run FAIL (89 failed / 18706 passed); no product or test edits made.**

## Run under classification

| Item | Value |
|---|---|
| Run | `app-full-1023100721-23537` (test service, `full` on `integration:app`) |
| Command | `npm test -- --maxWorkers=3` |
| Tree tested | `87c00cb43a076b21264896c3224e859b545d78ee` = commit `23b0901ba` (`Merge tl/ap2-A3-shared-json-type-return-0902`) |
| Integration head now | `0cdc76782` (tree `654a66946`), 2 commits later. Six files differ from the tested tree (`useTimelineCommit.ts`, `useTimelineSave.test.tsx`, `serialize.test.ts`, `serialize.ts` +16, two e2e files). None of the 20 failing files changed. |
| Upstream base | `7c17cc9d9` (verified ancestor of tested commit `23b0901ba`; 599 integration commits on top) |
| Counts | Test Files 20 failed / 1288 passed (1308). Tests 89 failed / 18706 passed (18795). |
| Log | `.../orch/tests/app-full-1023100721-23537/log.txt` |

**Pre-existing on upstream: none confirmed.** No allow-listed suite runs an upstream tree, and I did not add one. For every group I checked whether the failing expectation exists on `7c17cc9d9`. In each case the upstream product or test did not match the failing integrated behaviour, so I classify these as integration-introduced. Upstream runs are still needed to confirm this (see next steps).

**Deferred (D14 anchor-undo): none.** No failing test name matches anchor or undo.

## Classification table (89 tests, 20 files)

Class key: **REAL** = product or integrated-test defect on the integrated head. **TEST-STALE** = the test or fixture predates an integrated product change. **ENV** = environment. **UNRESOLVED** = not traced to a root cause. First error line is from the log.

| # | File | Count | Class | Root cause | Owner lane | Suggested fix |
|---|---|---|---|---|---|---|
| 1 | `src/tools/video-editor/testing/__tests__/providerCompatibility.runtime.test.ts` | 29 | TEST-STALE | The integrated `dataProvider.readTimelineInOrder` (`dataProvider.ts:1425`, added in `5077995cb` "A2/P1 port paired timeline head refresh") now calls `client.getProjectTimeline` (`GET /v1/projects/{p}/timelines/{t}`). The fixture `src/test/fakeWorkspaceRuntime.ts:495` (unchanged since upstream) throws on that path. The Runtime at `49ce532` still serves this GET as a public head projection (`service.get_project_timeline`), so the call is valid and the fixture is stale. | App A2/P1 (author of `5077995cb`) | Teach the fixture to serve the GET public projection (head revision and publication id). Drop the "retired" throw only for the document route. Keep the call. |
| 2 | `src/integrations/runtime/resolveProjectSelector.test.ts` | 1 | TEST-STALE | Same as #1: `AssertionError: promise rejected "Error: unexpected GET /v1/projects/811a65…"`. The test transport does not serve the public timeline GET. | App A2/P1 | Serve the GET in the test transport. |
| 3 | `src/integrations/runtime/timelineCommit.test.ts` (added in integration) | 1 | TEST-STALE | Same as #1: `Error: unexpected Runtime request: GET /v1/projects/project-commit/timelines/timeline-commit`. | App A2/P1 | Same. |
| 4 | `src/tools/video-editor/pages/VideoEditorPage.test.tsx` (P2-L04) | 3 | TEST-STALE | Same root. The L04 offline transport throws `Unexpected L04 offline transport request: GET /v1/projects/l04-project-id/timelines/l04-timeline` (line 6814). The two `Unable to find [data-testid="l04-admitted-card"]` failures (5818, 6316) follow from the same rejected read. Not separately verified. | App A2/P1 | Serve the GET in the L04 offline transport, then re-check the card assertions. |
| 5 | `src/tools/video-editor/commands/runner.test.ts` (added in integration; 6 tests x data/config) | 12 | REAL | `validateSerializedConfig` (`timeline-domain.ts:2558`) rejects top-level keys not in `ALLOWED_TOP_LEVEL_KEYS`, so the opaque root `opaque` (and `__proto__`) is reported as `unexpected top-level key`. The tests require opaque roots to be preserved next to a clip/track error. `066b651b9` and `4aeb1088e` claim opaque-root preservation, so the allowlist is the defect. Note: `__proto__` should still be refused, so the fix must not simply allow it. | App timeline-domain / opaque-roots lane | Allow declared opaque root keys in the validator. Keep `__proto__` refused. Keep the test expectations. |
| 6 | `src/tools/video-editor/commands/semanticGestures.test.ts` (added in `e22c6f714`, edited in `eb51ff381`) | 22 | REAL (unresolved sub-cause) | Refusals return success: `expected { ok: true, …(1) } to match object { ok: false, …(1) }` (5113, 5159, 5184 ... 5389). Other tests fail with `Cannot read properties of undefined (reading 'applyResolvedClipMove')` (5361) and `vi.fn()` not called (5077, 5089, 5374). `semanticGestures.ts` changed only in `e22c6f714`, so the integrated port wiring diverged from what these tests exercise. | App A2 gesture lane | Restore the refusal paths (absent capture, invalid time, cross-track, host refusals, outbox refusal) and wire `applyResolvedClipMove` through the adapter. Do not weaken the tests. |
| 7 | `src/tools/video-editor/runtime/astrid-element-components.test.tsx` | 3 | REAL | `1b4ac8b68` ("remove retired Astrid vendor implementations") deleted 9 `component.tsx` files under `vendor/astrid-browser/.../rendering/elements/` (animations fade, fade-up, scale-in, slide-left, slide-up, type-on; effects text-card; transitions cross-fade, fade). Their `element.yaml` catalog entries remain. Upstream `7c17cc9d9` has all 9. First error: `packs/rendering/rendering/elements/animations/fade/component.tsx: expected undefined to be type of 'function'` (6904). This is not environment: the files are missing from git. | App U3 vendor lane | Restore the 9 component files from `7c17cc9d9`, or re-vendor them in the same commit that removes the catalog entries. Decide which, and say so. |
| 8 | `src/tools/video-editor/compositions/vendoredTimelineCompositionAliases.test.ts` | 3 | REAL | `927545cf5` removed the `@workspace-effects/animations/transitions` aliases from `config/testing/vitest.config.ts` and `vitest.boundary.config.ts`. The test (also changed in the integration) still requires them in all three runtime configs. First error: `expected 'import { defineConfig } from 'vitest…' to match /["']@workspace-effects["']\s*:/` (5487). `vite.config.ts:176` still has them. Internally inconsistent. | App vendoring / Composition lane | Decide whether the aliases are retired. If not, restore them in the testing configs. If yes, update the test in the same commit (owner decision). |
| 9 | `src/tools/video-editor/compositions/TimelineRenderer.test.tsx` | 1 | ENV | Shared `node_modules/@banodoco/timeline-composition` is an installed directory at version `0.0.13`. The integrated `package.json` pins the `635f4de` tgz (`0.0.14` in `package-lock.json`). The installed dist emits `bundled:2rp@0.1.0`, and the test expects `/timeline-theme-2rp/` (5468). `realpath` shows a real directory, not a link. | Environment / install owner | Reinstall the pinned tgz into a private overlay to confirm. Do not touch the shared install. |
| 10 | `src/tools/video-editor/compositions/TimelineRenderer.public-host.qualification.test.tsx` | 2 | ENV (probable) | Same installed-package mismatch as #9: `expected undefined to be defined` (5444, 5456) on catalog and registry identity. Not verified by a run. | Environment / install owner | Confirm with the same private-overlay check as #9. |
| 11 | `src/tools/video-editor/lib/timeline-save-utils.test.ts` (M) | 3 | REAL (probable, unresolved) | Serialized output differs from the expected string. The integration changed `serialize.ts` (+164), `timeline-data.ts` and the test file. The first two errors are at 6831 and 6872. | App save / serialize lane | Trace the serializer output diff. Keep the expectations. |
| 12 | `src/tools/video-editor/data/shotCompositionProjection.test.ts` | 1 | REAL | Unchanged upstream test. Integrated projection freezes the effective volume (`expected 1 to be undefined`, 5787). `shotCompositionProjection.ts` changed +41 in integration. | App shot-composition projection lane | Stop freezing the effective value when the source is unset. |
| 13 | `src/tools/video-editor/hooks/useAssetManagement.assetDrop.test.ts` | 1 | REAL (probable) | Unchanged upstream test. `expected null not to be null` (5806) when optional placement fields are absent. Product changed by integration (+2 in `useAssetManagement.ts`, plus `placementRequester` / `placement` lines). | App asset-drop lane | Trace the prepared-media command for absent placement fields. |
| 14 | `src/integrations/runtime/shotCompositionRuntime.test.ts` | 1 | REAL (probable) | Unchanged test. Output lacks `storedOccurrenceDurationMs` in the replayed popup publication (3326). | App shot-composition port lane | Trace the replay publication fields. |
| 15 | `src/tools/travel-between-images/components/ShotTimelinePreview.test.ts` (M) | 1 | REAL | `__proto__` own-key collision in the raw opaque app is turned into an Array prototype (`canonicalTiming: Array {…}`, 3417). The test name is "restores raw opaque app collisions". | App shot-timeline popup lane | Preserve raw opaque keys via own-property definition, not plain assignment. |
| 16 | `src/tools/travel-between-images/components/ShotTimelinePreview.integration.test.tsx` (M) | 1 | UNRESOLVED | `Element type is invalid: … got: undefined` (3402) in the render tree. No component name in the stack. Candidates: a missing vendored element (#7) or the stale composition install (#9). Not verified. | App shot-timeline popup lane | Get the component stack, then pick the root. |
| 17 | `src/tools/travel-between-images/pages/LocalTimelineShotBrowser.test.tsx` (M) | 1 | REAL (probable) | `expected "vi.fn()" to be called with arguments: [ ObjectContaining{…} ]` (3448). The forwarded occurrence session and current-data callback no longer match. Integration `5ca458868` changed the popup. | App shot-timeline popup lane | Forward the parent occurrence session as the test expects. |
| 18 | `src/shared/lib/__tests__/qualityCheck.contract.test.ts` | 1 | REAL | Integrated `quality:check` (`package.json`) chains `typecheck:strict-probe` and drops `typecheck:strict-islands` and `test:no-remote-hosts`. Upstream has both. First error: `expected 'npm run check:no-smoke-tests && npm r…' to contain 'npm run typecheck:strict-islands'` (3386). | App integration / hygiene (`8a40acdd7`, `064dca1e0`) | Restore the dropped gates in the canonical `quality:check`. Do not edit the test. |
| 19 | `src/app/main.bootstrap-order.test.tsx` (M) | 1 | REAL (stale merged test case) | The added case "injects the remote font links by default" expects `link[data-installed-app-fonts]` injection. No `src/` code injects it. Upstream `1fc2c3602` dropped the remote-font switch ("self-host Inter") and its test says "typography is self-hosted". The integrated `config/vite/vite.config.ts:113` keeps a `VITE_DISABLE_REMOTE_FONTS` leftover. First error: `expected false to be true` (3287). | App bootstrap / fonts lane | Decide per upstream policy. Remove the stale case and the switch leftover together, or restore the switch deliberately. |
| 20 | `src/tools/video-editor/components/PropertiesPanel/VideoEditorAssetPanelSurface.transcript.test.tsx` | 1 | UNRESOLVED (probable real) | `expected "vi.fn()" to be called at least once` (6952). The test is unchanged. The integrated surface and the vendored `TranscriptPanel` (`vendor/astrid-browser`, re-vendored in `216d5116d`) both changed. Not traced further. | App transcript / vendor lane | Trace the rebuilt host's transcript request. |

Totals by class (sum 89):

| Class | Tests | Rows |
|---|---|---|
| TEST-STALE | 34 | #1–#4 |
| REAL (includes "probable" rows) | 50 | #5–#8, #11–#15, #17–#19 |
| ENV | 3 | #9–#10 |
| UNRESOLVED | 2 | #16, #20 |

## Groups by root cause

| Root cause | Tests | Rows |
|---|---|---|
| A. Integrated read path calls the public timeline GET; fixtures don't serve it (TEST-STALE) | 34 | #1–#4 |
| B. Validator rejects opaque root keys (REAL) | 12 | #5 |
| C. Gesture refusals return success and the adapter is not wired (REAL) | 22 | #6 |
| D. Vendor deleted rendering element components still declared in catalog (REAL) | 3 | #7 |
| E. Vitest configs lost `@workspace-*` aliases (REAL, inconsistent) | 3 | #8 |
| F. Stale installed `@banodoco/timeline-composition` 0.0.13 vs pinned 0.0.14 (ENV) | 3 | #9–#10 |
| G. Serializer output (REAL probable) | 3 | #11 |
| H. Shot/asset/popup product drift (REAL, individually) | 5 | #12–#15, #17 |
| I. Gate removed from `quality:check` (REAL) | 1 | #18 |
| J. Stale font case from merge (REAL, policy decision) | 1 | #19 |
| K. Unresolved | 2 | #16, #20 |

## Notes

- Root cause A is the brief's hypothesis, but the direction is reversed for part of it. The fixture is stale, not the product. Runtime `49ce532` `service.get_project_timeline` still serves the public projection, and the R4 qualified candidate (`candidate-app-qualified`) does not call the GET. So the new dependency came in `5077995cb`. The owner should confirm the paired-head read is intended before the fixtures are updated.
- The "retired" throw in the fixture is an upstream assertion. I did not touch it. Per the orchestrator rule, do not weaken it; update the fixture so it serves the public projection.
- Two integrated-test files import behaviour that upstream retired (#19), and one integrated product removal was not reflected in its test (#8). Owners should check whether these are merge artifacts before fixing.
- Deletions in `1b4ac8b68` (#7) and `927545cf5` (#8) are integration-only, so they are not upstream behaviour.

## Commands and evidence

Read-only, no test runs. Nothing was run on the full suite.

- `git -C /home/user/work/app log --oneline 7c17cc9d9..23b0901ba` and `git diff --name-status 7c17cc9d9 23b0901ba` over the 20 failing files, to find added, modified and unchanged files.
- `git show 23b0901ba:…` and `git show 7c17cc9d9:…` for the product and test sources in #1–#20.
- `git -C /home/user/work/runtime show 49ce532:runtime_protocol/{door.py,service.py}` for the Runtime timeline GET.
- `git -C /home/user/work/app ls-tree -r --name-only` diff of `vendor/astrid-browser/.../rendering/elements` between the two trees (9 `component.tsx` removed).
- `realpath` and `package.json` / `package-lock.json` of `node_modules/@banodoco/timeline-composition` (read-only).
- The source log `log.txt` for every first error line.

## Next steps

1. Owner of `5077995cb` (App A2/P1): confirm the paired-head public GET is intended, then update `src/test/fakeWorkspaceRuntime.ts` and the two test transports (#1–#4). Do not remove the "retired" guard for the document route.
2. App timeline-domain owner: allow declared opaque root keys in `validateSerializedConfig` and keep `__proto__` refused (#5).
3. App A2 gesture owner: restore refusal paths and the `applyResolvedClipMove` wiring (#6).
4. App U3 vendor owner: restore or re-vendor the 9 deleted element components (#7).
5. Decide the `@workspace-*` alias policy for the testing configs (#8).
6. Reinstall the pinned composition tgz into a private overlay to confirm #9–#10 (environment). Do not touch the shared `node_modules`.
7. If upstream confirmation is needed for "pre-existing", request a named suite on a snapshot of `7c17cc9d9` (needs an orchestrator suite entry). Not run here.
8. Trace #11, #13, #14, #16, #17, #20 further before fixing.
