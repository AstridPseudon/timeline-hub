# App2 M2 resolved-edit serializer consumer cut plan

Source-only proposal; no App source or tests were changed.

## Basis and current state

- Requested current-root ref is available: `hub/timeline/app/tl/app-m3-root-cold-current-source-attribution`.
- Inspected App tree: `05b6b488d1834650c459c5c565f2530d9bea20e9` (current-root parent/current functional base: `b1ef4b9b910ba72375c34cf319692f90d22edc25`).
- `serializeResolvedTimelineEdit` has exactly three production callsites in this tree:
  `src/tools/video-editor/commands/runner.ts:244`,
  `src/tools/video-editor/hooks/useTimelineCommit.ts:532`, and
  `src/tools/video-editor/lib/timeline-mutation-engine.ts:208`.
- The helper is still a whole resolved-document serializer. It is not an EditCommand payload and must not remain as a fallback behind a native-looking producer.
- The existing generic safety repair preserves opaque authored roots, but is not a writer retirement. D01 remains open until each producer has a qualified native replacement.

## Smallest row-local proposal

| Consumer | Current dependency and result | Existing native/shared coverage | One next implementation task |
|---|---|---|---|
| `commands/runner.ts:3,244-255` (`applyTimelineCommandEffect`, `resolved-config` arm) | The arm calls the serializer, then `buildDataFromCurrentRegistry`, and preserves uploading clips. The live producer using this arm is `commands/media.ts:244-285` (`buildSwapMediaCommandEffect`), which currently builds a complete `resolvedConfig` for swap. The direct result is a local `TimelineData` projection, not a Runtime command. | App already has `applyPreparedMediaCommand`/`prepared-media` for prepared placement, and `semanticGestures.ts`/`clipMoveCapture.ts` for `clip.move`. Agent exposes `occurrence.swap-media`, but App has no capture bridge that supplies raw child ownership plus verified old/new media pins. Generic command descriptors must not silently fall back to this arm. | First migrate the swap producer to an existing-session native `occurrence.swap-media` capture/projection (or make the unsupported boundary visibly refuse); then remove the `resolved-config` effect arm and its serializer import once no descriptor emits it. Preserve the local projection and `commandHistory` behavior while removing whole-document serialization. |
| `useTimelineCommit.ts:22,532-553` (`applyEdit`, `type: 'config'`) | This is the shared save owner: it serializes `mutation.resolvedConfig`, rebuilds through `buildDataFromCurrentRegistry`, then calls `commitData`, which emits the legacy snapshot save. It is reached by generic update/trim/split/track/inspector paths, not only media. | Existing command-session ports are limited to clip move and track label. `prepared-media` is a native App carrier, but there is no general native capture carrier for this `resolvedConfig` union. Agent has `clip.set`, `clip.set-params`, `clip.trim`, `clip.split`, `track.create`, `track.set`, `clip.add`, and `clip.delete`; App does not yet capture these through the same session/outbox. `useTimelineCommandSession.ts`, `commands/commitSession.ts`, `useTimelineOps`, `DataProvider`, and related save plumbing are shared App-owned seams and require the App owner’s coordinated patch. | Migrate one producer cohort at a time to an Agent command plus local command projection, starting with scalar/trim paths that have exact Agent operations. Change this branch only after its callers supply authored command output: materialize that projection without `serializeResolvedTimelineEdit`, enqueue through the existing command session, and delete the `resolvedConfig` mutation variant last. Do not add a second snapshot serializer or invent a new wire DTO. |
| `timeline-mutation-engine.ts:3,208-215` (`previewTimelineMutation`) | This is the pure preview/validation twin used by `useTimelineCommandsService` (`validateMutation` and `applyValidatedMutation`). It serializes an arbitrary resolved config before rebuilding rows/meta/order, so preview can bless the same legacy path that the save owner later writes. | Existing row materialization (`materializeTimelineRows`), `buildDataFromCurrentRegistry`, and the command runner’s authored-config/data effects are reusable local projection helpers. `compileTimelinePatch` is an App-local patch preview, not proof of an Agent Runtime command. The service’s move path already uses `clipMoveCapture`; its update, trim, split, track-add/reorder/remove paths still construct `type: 'config'`. | Make preview consume the same native command projection/result as the eventual commit for the first migrated operation; then remove the serializer branch only when all `useTimelineCommandsService` config producers have command-backed projections or explicit refusal boundaries. Keep validation and preview pure; do not move Runtime I/O into this engine. |

The smallest safe cut is therefore producer-first: add/qualify native capture and local projection for one operation family, route both preview and commit through that projection, prove acceptance/reload/undo/retry, then remove only that producer’s legacy route. A global deletion of the helper or a serializer-only replacement would leave unresolved callers and would not close Gate 6.

## Native operation assignment and gaps

The current Agent operation registry/source exposes these relevant native operations: `clip.move`, `clip.delete`, `clip.add`, `clip.set`, `clip.set-element`, `clip.set-params`, `clip.trim`, `clip.split`, `track.create`, `track.set`, `occurrence.add-media`, `occurrence.swap-media`, and `occurrence.duplicate`. Existing App bridges cover only the already-qualified move/label shapes plus the prepared-media local carrier.

Assign existing operations as follows:

- scalar clip fields/params → `clip.set` or `clip.set-params`, retaining explicit clears and exact raw-field reads;
- bounded trim → `clip.trim`; split → `clip.split`; track creation/label → `track.create`/`track.set`; delete/add → `clip.delete`/`clip.add` where ownership and created-ID capture are available;
- popup/ordinary media replacement → `occurrence.add-media`/`occurrence.swap-media`, with the existing verified media-selection inputs and raw occurrence/clip identity;
- duplicate → `occurrence.duplicate` only for the occurrence-owned path already covered by its dedicated handoff.

Missing or not yet assigned operations are the App capture/session adapters for those Agent operations, plus any current producer that changes several unrelated config roots (shader inspector, track reorder/remove with implicit clip deletion, sequence/whole-timeline transforms, or ordinary mixed batches). Those must either receive an explicit native Agent operation/batch contract or visibly refuse with the draft retained. They must not continue through `resolvedConfig` while claiming native migration.

## Cap and shared serializer coordination

The current-root tree does **not** contain the stored-cap/raw-basis serializer changes. The exact shared chain is:

1. `4720a864c81dc7002a9e95dbacf10cec8df5da81` — adds verified raw-basis/counterpart serialization and stored-cap restoration;
2. `1fe351b9847d35db66ab294a6edf631447fa78ce` — fixes the serializer’s own-property check for the ES2020 target;
3. `93696b62f30cf86eac632f975a80de4851489c17` — applies the same ES2020-safe check in the popup provider.

That chain is based directly on `b1ef4b9b910ba72375c34cf319692f90d22edc25`, not on the current-root tip, and it also changes the shared DataProvider/recovery/popup seams. It must be reviewed/integrated as one shared candidate before relying on it. The three serializer consumers above currently have no raw `PreparedShotComposition` basis argument; do not guess one from `TimelineData`, add a second store/DTO, or pass a cap scalar as a substitute for raw ownership.

The cap work and this serializer cut have separate responsibilities: cap work preserves derived-view stripping and raw opaque collisions at authored/draft/popup exits; the M2 cut removes the legacy resolved-document writer once command producers exist. If the cap candidate is integrated first, its exact raw-basis refusal behavior remains required. It does not make a `resolved-config` mutation native and does not qualify deletion of these three callers.

## Preservation and deletion gate

Retain the existing positive behavior throughout the migration, including:

- opaque roots containing `null`, `false`, `0`, ordered keys, and literal own `__proto__` data;
- authored registry-root preservation, including `null` and opaque nested values;
- malformed known-field refusal without dropping opaque siblings;
- asset-drop positives where unresolved duration remains `null` and the visible fallback remains intact.

The current targeted tests passed: `serialize.test.ts`, `runner.test.ts`, and `useAssetManagement.assetDrop.test.ts` — **3 files, 56 tests, exit 0**. These are source assumptions only, not writer-retirement evidence. Do not weaken, delete, or relabel these positives as refusal tests.

Delete the helper/imports and then the obsolete mutation variants only after each affected producer has:

1. an Agent-native command and exact raw/base/revision inputs;
2. a local preview equal to the command projection;
3. accepted Runtime `/v1` commit, reload, guarded undo, lost-ack exact retry, and draft/recovery preservation;
4. zero traffic through the old snapshot writer for the representative gesture, including popup add/swap where applicable.

## Tests required for the implementation

Native prerequisite, using the current Agent operation sources, should cover the operation-specific conformance/provider lanes (not a serializer substitute):

```sh
PYTHONPATH=/home/user/work/agent /home/user/work/venv-agent/bin/python -m pytest -q \
  tests/editing_conformance/test_recipe_m1_commands.py \
  tests/editing_conformance/test_recipe_clip_delete.py \
  tests/editing_conformance/test_recipe_m2_clip_add.py \
  tests/editing_conformance/test_recipe_m2_clip_split.py \
  tests/editing_conformance/test_recipe_m2_clip_trim.py \
  tests/editing_conformance/test_recipe_clip_set_element.py \
  tests/editing_conformance/test_recipe_scalar_commands.py \
  tests/editing_conformance/test_recipe_occurrence_media.py \
  tests/editing_conformance/test_recipe_occurrence_duplicate.py
```

For the App implementation, rerun the three focused files above with the root config and bounded flags, then add only the directly changed consumer neighbors. Qualification still needs the central App Gate 5/6 suites (no local browser/socket run): `full-e2e-three-products` for the adversarial commit/reload/undo/retry journey and `full-e2e-timeline` for representative gestures plus zero legacy writer traffic. Cross-repo native/runtime acceptance should use the existing Agent `commit-integration`/Runtime `input-integration` lanes with the exact selected Agent/Runtime pair. No full, browser, socket, or live-runtime suite was run for this source-only plan.
