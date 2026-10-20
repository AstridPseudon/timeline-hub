# Parent manual media: original selection source

**BLOCKED: no original five-field selection reaches the actual manual producer.** This is the brief's explicit missing-carrier branch. No applicable producer patch is supplied; inventing the missing catalog authority or obtaining a later selection would violate the task. No product/shared files were changed, no legacy producer retired, and no merge/qualification is claimed.

Inspected App base `82fec72c9ab5b0c5a8d838ec450df274ec135521` (assigned branch), App integration `590c19795111fd1891bbd50a5f8d48bef3505a26` read-only, and a private snapshot of Runtime `a51af885ea631c695a857985239c7fe7bf2e871f`. Read PLAN sections 2, 3, 6 and `design/handoff-app-to-app2-parent-media.md` plus `design/app2-parent-media-native-capture.md`. The named `design/ap2-m2-parent-producer-patch-review.md` does not exist; read its surviving worker `report.md` and detailed logged review instead.

## Exact missing boundary

| Boundary in assigned App base | Existing value | Missing authority |
| --- | --- | --- |
| `src/tools/video-editor/hooks/useTimelineCommandsService.ts:78`, `:442` | `AddClipCommandInput.preparedAsset?: TimelineProvisionedAsset`, or registry `assetId`; `TimelineCommands.addClip` is synchronous (`:163`) | Original `MediaSelection`; cannot derive it from `assetId` |
| `src/tools/video-editor/commands/provisioning.ts:5` | `TimelineProvisionedAsset = {assetKey, mediaType, durationSeconds, entry, source}` | No five-field pin; no catalog digest |
| `src/tools/video-editor/data/AssetResolver.ts:30` | `PreparedMediaImport = {provider, project, importOperationId, generationId, variantId, assetId, entry}` | No five-field pin; no catalog digest |
| `src/integrations/runtime/dataProvider.ts:1233`, `:1529` | `prepareMediaImport` calls `toPreparedMediaImport`; `entry` contains object `media_id`/`content_sha256` and generation/variant IDs | No call obtaining the original selection, including before returning preparation |
| `src/tools/video-editor/hooks/useAssetManagement.ts:201` | `prepareGenerationAsset` turns import/drop data into the existing provisioned asset | Copies entry and generation/variant IDs; no selection originates here |
| `src/tools/video-editor/types/index.ts:584` | `AssetRegistryEntry` holds locator, object hash, generation/variant and optional metadata | Object hash is not `catalog_digest`; no authoritative selection minted into metadata |
| `src/shared/lib/dnd/dragDrop.ts:53` | `GenerationDropData` carries generation, optional variant/media ID and display metadata | Neither the full pin nor an authoritative original catalog snapshot |

The concrete manual prepared producer is `createTimelineCommands(...).addClip` in `useTimelineCommandsService.ts:442`. Its prepared branch previews `PlacePreparedMediaCommand` and calls `state.ops.applyEdit({type: 'prepared-media', command}, ...)` at `:499`; the registered branch calls `buildAssetDropEdit` at `:573` then the rows mutation. Both remain legacy. Existing direct tests exercise this actual facade successfully without any selection input. The manual drop preparation alternative has the same missing boundary, ending at `TimelineProvisionedAsset` in `useAssetManagement.ts:201`. Automatic/staged/popup/recovery ADD and duplicate-generation were not candidates for conversion.

A repository-wide production search for `catalog_digest`, `getProjectMediaSelection(` and `captureParentClipAddMediaFromRuntime` found the generated schema, Runtime wrappers, the native helper's validation and the unused adapter. There is no production prep/gesture caller that obtains and retains an original pin. Read-only integration inspection found no such carrier either. Generic metadata permits opaque data but no producer writes an authoritative selection into it; it cannot be treated as existing authority.

## Exact Runtime/native contract

`src/integrations/runtime/timeline-commit-types.ts:33` defines the existing `MediaSelection` with exactly `asset`, `generation_id`, `variant_id`, `object_id`, `catalog_digest`. The query at `:111` contains only the first three; it is a lookup, not a pin.

Runtime `runtime_protocol/timeline_commit_port.py:828` computes `catalog_digest = digest(record)` over a reconstructed record containing realm/project, selected alias, generation/variant metadata, managed entry, and applicable output lifecycle/provenance. It is not the CAS object digest. At `:831` a mismatching original catalog digest refuses; at `:838` verification requires the closed five-field selection. `runtime_protocol/service.py:2530` exposes the existing selection read and `:2538` verifies the exact selection. `runtime_protocol/server.py:51` routes the three-field lookup and five-field verified read separately. No new Runtime endpoint/schema is needed to read a selection at the correct original preparation boundary.

The native helper already has the right input contract: `captureParentClipAddMedia(bundle, row, media, verifiedMedia)` at `parentClipAddCapture.ts:294` and deterministic `finishParentClipAddMedia` at `:303`. `row.asset` is its original authored alias and must remain distinct from any assumptions about selected asset naming. The helper cannot manufacture a previously missing pin.

## Smallest peer seam required

App owns the preparation boundary, existing carriers, session/outbox and temporary freeze. Before a real consumer patch can be made, App must identify/establish the original selection read at one chosen manual preparation boundary and retain its **existing Runtime `MediaSelection` value**, associated with the original project, raw bundle, allocated row/clip ID and authored alias. For the import/prepared path the exact peer join is `RuntimeDataProvider.prepareMediaImport` / `toPreparedMediaImport` -> existing `PreparedMediaImport` -> `prepareGenerationAsset` -> `TimelineProvisionedAsset` -> manual `addClip`. For an already registered asset it must originate at the selected asset's original gesture/preparation, not after async work. The owner must choose the existing internal carrier/closure; this worker does not add a DTO, store, endpoint or public API to conceal its absence. An absent original on a resumed legacy preparation cannot be silently refreshed.

Once supplied, the adapter can accept that exact five-field value, detach/freeze original raw bundle/row/selection **before the first await**, call only the existing exact verified-media read, pass both unchanged to native capture, and enqueue one command through the existing outbox. Reserve/fence session generation, displayed head, local predecessor and bundle before awaiting; reject if any change afterward. Reuse the existing intent/body/key on retry/reload; do not reacquire a selection. These are remaining implementation requirements, not implemented or proven behavior in this task.

## Donor defects remain; do not promote it

`design/handoff-ap2-m2-parent-media-concrete-producer.patch` SHA256 `fadf7e27409d467fb4f943d5ae997e4754ab75472d7fc90dcf8a4b1f20283f7b`:

- `parentMediaProducer.ts:55` obtains a selection from the three-field query after preparation. It snapshots bundle/row only after its awaits. That cannot preserve a selection that was never carried in.
- The proposed `commitSession.ts` capture reads `localGeneration`, `lastIntent` and `known.head` **after** awaiting capture. It can label an old bundle with a newer session basis, so its later generation check does not establish the original gesture fence.
- The `parentMediaGesture.ts` new-file hunk declares 38 lines, ending at an open `if`. Extra plus-prefixed closing lines beyond the declared hunk are not applied. Parsing those 38 applied lines with TypeScript gives diagnostic 1005, `'}' expected`, line 39; no submit call exists. The module is absent from the assigned base. No source shell can be removed here; the unlanded donor must be replaced/omit that file when the producer seam is resolved.
- No production caller uses the adapter. Source-helper positives cannot qualify the manual producer or permit writer retirement.

No NEW flat product patch is emitted because the brief explicitly requires a missing-source report instead of invented authority when existing carriers lack the original selection. Reissuing an unused adapter or fixing only the shell would not satisfy the real-producer requirement.

## Exact evidence

All App runs used a private `git archive HEAD` copy under this worker's `private-app/`, a symlink to read-only shared dependencies, `--no-cache`, the runner config loader and an explicit private `cacheDir`. The private test config's two `__dirname` references were replaced with absolute original module directories so that the ESM runner could load it; no product implementation or test assertion changed. An initial config startup failed with `ReferenceError: __dirname is not defined` before tests; the following corrected runs passed. Runtime ran a private archive of its stated revision with bytecode/cache output disabled or directed to this worker. Copies and test temp/cache files were removed after evidence collection.

Let `W=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-original-selection-source`. From `$W/private-app`:

```sh
node node_modules/vitest/vitest.mjs run --config selection-source.vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/commands/parentClipAddCapture.test.ts src/tools/video-editor/commands/commitSession.test.ts src/tools/video-editor/commands/commitOutbox.test.ts src/tools/video-editor/hooks/useAssetManagement.mediaImport.test.tsx src/tools/video-editor/commands/media.test.ts src/integrations/runtime/mediaImport.test.ts
```

**6 files, 117 passed**, exit 0 (`targeted-tests.log`). This is bounded existing helper/session/outbox/import behavior, not a new consumer qualification. The adapter's existing query-based positive is unchanged and does not establish original-selection authority.

```sh
node node_modules/vitest/vitest.mjs run --config selection-source.vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/contexts/VideoEditorProvider.test.tsx -t 'returns structured public-command failures for missing assets|returns structured addClip failures|omits absent selection and optional prepared-media payload fields|preserves supplied prepared-media fields'
```

**5 passed, 60 unselected**, exit 0 (`manual-producer-tests.log`). Vitest prints unselected cases as skipped due to the command's test-name filter; no test was edited/skipped/disabled. These exercise real `addClip`/prepared-media behavior and retain the passing legacy expectations.

```sh
node node_modules/vitest/vitest.mjs run --config selection-source.vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism src/integrations/paired/pairedRoutePolicy.test.ts -t 'derives the App|local door only'
```

**9 passed, 1938 unselected**, exit 0 (`route-tests.log`). Existing source-derived local-door-only policy, selected explicitly to avoid rerunning the broad generated matrix.

From the assigned worktree, with `$W` expanded to the absolute path above:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$W/private-runtime" /home/user/work/venv-app2-native/bin/python -m pytest -q -p no:cacheprovider --basetemp="$W/runtime-test-tmp" "$W/private-runtime/tests/test_timeline_verified_media.py"
```

**28 passed, 1 warning**, exit 0, 7.69s (`runtime-targeted-tests.log`). Warning: existing environment lacks support for pytest's `timeout` config option. The file uses direct in-process handlers/service calls; no live HTTP server/socket/browser is started. It covers exact reads, original-pin catalog-change refusal without refresh/writes, authorization recheck, and malformed/nonexact query refusal.

Additional read-only checks: `git apply --numstat` on the donor confirms the 38-line gesture hunk; TypeScript parsing of exactly those applied lines records diagnostic 1005 in `donor-shell-parse.log`. `source-boundaries.log` contains exact type/producer extracts and the production-call search. Assigned worktree `git status --short` and `git diff --exit-code` are clean.

No full/browser/live-socket runs, installs, dependency writes, generated/pin/Git/ledger edits. No actual TS -> Agent310 **production-caller** command was generated or verified: there is no authorized original input from that caller. Earlier helper-only native parity is not counted as this task's evidence. Native acceptance, reload, guarded undo/redo, exact lost-ack retry, draft retention under the new async producer, and zero legacy traffic remain unverified.

Recommended next step: App/Runtime owners resolve the original-selection preparation/carrier join above, then assign a concrete manual-producer private patch with the unchanged five-field input. Only then run direct producer/session/route tests and actual TS -> Agent310 parity before any consumer retirement decision.
