# Current-pin producer ownership source proposal

## What changed

Added one focused App journey and one support helper:

- `tests/e2e/local/producer-ownership-current-pin.spec.ts`
- `tests/e2e/local/support/producer-ownership-current-pin.ts`

The journey seeds one dedicated timeline through the existing isolated `appTest`/Runtime harness and composition-publication genesis pattern. It uses valid transcript source intervals and existing output rows; it does not call transcript or scene action builders to mutate state.

The transcript setup has two in-window source items and one valid source item at source seconds `[6, 8]`, while the media carrier covers `[0, 4]`. The stale generated caption for the out-of-window item is placed after all protected rows. The normal UI Regenerate path is expected to produce only the existing owned row's native `clip.delete`; no fresh `clip.add` or unsupported host-field write is accepted by the assertion. If the current mounted projection refuses the action, the journey records an explicit `no-accepted-ownership-proof` annotation and checks atomic refusal, unchanged head, and unchanged protected rows after reload/retry.

The scene setup has one existing owned output plus foreign-owned and user-authored rows. The normal Move existing shots to markers UI path is expected to emit only native `clip.move` and hold-setting `clip.set` commands for the owned row. It checks that foreign/user rows retain their complete raw objects and order. The accepted path also covers reload, a real Runtime commit followed by a dropped browser acknowledgement, exact raw-body and idempotency-key retry, and Undo; each protected-row check is repeated.

## Source, cohort, and normal UI prerequisites

- App source: `tl/ap2-m2-producer-ownership-active-route-repair-0210` at `9a5e9ed6c` (`fix(app): preserve producer ownership metadata`).
- Custody behavior copied from the reviewed helper source at `tl/ap2-m2-producer-proof-custody-defects-repair-0247`, `384add7e3`.
- Behavior reference: current Agent8130, Runtime2c4, and Composition public13 cohort; no new operation, DTO, authority, carrier alias, or timing policy is introduced.
- The route must be opened with the exact seeded `project` and `timeline` query parameters in the isolated worker realm.
- The normal transcript lane must be mounted and show two chips; the test uses Transcript actions → “Regenerate transcript captions and replace edits”.
- The normal Scene Phase Markers panel must be mounted with the two seeded markers and its existing “Move existing shots to markers” control enabled.
- Undo must be available after the accepted scene commit.

## Live callers

The new spec calls the new support helper. The support helper calls the existing `appTest` direct harness, `compositionPublication`, Runtime composition-revision genesis endpoint, the transcript lane UI action, and the Scene Phase Markers UI action. Production callers exercised by those UI actions are:

- `src/tools/video-editor/dev/transcript-lane/extension.ts` (`transcriptLaneExtension`, `buildTranscriptCaptionPatch`)
- `src/tools/video-editor/dev/scene-phase-markers/extension.ts` (`scenePhaseMarkersExtension`, `moveExistingShotsToMarkers`)
- `src/tools/video-editor/dev/localExtensions.ts` (local extension registration)

No production source, shared three-product source, or future fresh-output proof file was changed.

## Checks

- `npx eslint tests/e2e/local/producer-ownership-current-pin.spec.ts tests/e2e/local/support/producer-ownership-current-pin.ts --ext ts --max-warnings 0` — passed.
- `npx tsc --noEmit --pretty false` — passed.
- `npx playwright test --config current-pin-playwright.config.ts --list` — passed; exactly 1 test collected. The temporary collection config was removed afterward.
- `git diff --check` — passed.
- `git diff --no-index --check /dev/null <each new file>` — no whitespace diagnostics; the command's normal untracked-file status was handled explicitly.

Per the source-only brief, no browser, localhost, socket, actual-gate, full-suite, or install run was made. Therefore this safely supplies the current-path proof source and its refusal evidence shape, but does not claim that the current host accepts the transcript stale-remove or scene MOVE/HOLD commits until the central gate runs. It also makes no fresh-creation-carrier or feature-complete claim.

## Next step

Run the single collected journey in the approved browser/socket gate. If the transcript lane refuses the stale-remove setup, retain the explicit refusal annotation and report the exact mounted-projection limit rather than changing the fixture to force acceptance.
