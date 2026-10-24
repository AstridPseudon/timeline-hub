## FAIL — A3 full-caller witness

Source and test tree remain unchanged; `git status --short` and `git diff --check` are clean.

Finding: the RED is a genuine production defect, not a malformed V2 track/selection fixture.

- Real path: upload/import → `prepareGenerationAsset` → mounted `addClip` → `applyPreparedMediaCommand`.
- The projected existing clips contain derived `assetEntry` fields ([projection](</home/user/work/wt/app-A3-popup-full-caller-review-0814/src/tools/video-editor/data/shotCompositionProjection.ts:566>)).
- Prepared-media serialization validates those clips and rejects `assetEntry` as `unexpected_clip_key` ([guard](</home/user/work/wt/app-A3-popup-full-caller-review-0814/src/tools/video-editor/lib/timeline-domain.ts:2581>)).
- `applyPreparedMediaCommand` collapses this to `null`, so `addClip` returns `mutation_failed` before `applyEdit` ([helper](</home/user/work/wt/app-A3-popup-full-caller-review-0814/src/tools/video-editor/commands/media.ts:773>), [caller](</home/user/work/wt/app-A3-popup-full-caller-review-0814/src/tools/video-editor/hooks/useTimelineCommandsService.ts:506>)).
- Therefore capture, outbox, commit, and receipt assertions are unexecuted.

The scratch diagnostic invoked the actual helper and reported:

`FIELD_CATEGORY=unexpected_clip_key:assetEntry`

The V2/raw-V2/shared-occurrence input is structurally valid for reproducing this failure. However, the witness response mock is not authentic enough for PASS: it echoes requested steps instead of provider-authoritative patches/dependencies, supports only `accepted`, and returns an unchanged/incomplete canonical closure rather than the added media/fork result. It does not cover merged, conflict, invalid, or historical rebased outcomes.

Tests:

- Focused witness: 1 file passed, **1 expected failure**.
- Popup/service/prepared-media controls: **4 files, 51 tests passed**.
- TypeScript (`tsconfig.json`, `tsconfig.app.json`, `tsconfig.node.json`): passed.
- ESLint on witness: passed.
- `git diff --check`: passed.
- Node-only `shotTimelineDataProvider.a3.test.ts` cannot run under Node20 because its own node-environment setup assumes global `navigator`; this is an environment limitation, not the A3 defect.

No browser, backend, HTTP, full, build, or provision suite was run.