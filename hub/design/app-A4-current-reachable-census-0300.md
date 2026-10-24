## Result

A4 is not end-state PASS: one reachable fallback writer remains.

Current production paths use the v2 Runtime commit:

- Editor/UI: `VideoEditorPage` → `RuntimeDataProvider` → `VideoEditorProvider` → `useTimelineSave` → `createLocalSaveSession` → `provider.commitTimeline`.
- Prepared image/video, staged generation, popup saves, history, and automatic placement all converge on that local-save/v2 commit path.
- `registerAsset` uses `patchRegistry` through the command facade; direct Runtime `registerAsset`/`uploadAsset` has no App production caller.
- Preview helpers remain active document-planning helpers, not dormant writers.

Remaining reachable writer:

- `VideoEditorProvider.tsx:307-330` creates `createElementTimelineRoutes`.
- Agent-chat registration exposes the element adapter at `VideoEditorProvider.tsx:358-372` and `:1059`.
- `element-adapter.ts:95-110` calls `provider.saveTimelineAtHead`.
- Runtime `dataProvider.ts:1028-1159` turns this into legacy `publishParentComposition`.

Smallest migration packet: replace the element adapter’s save boundary with the mounted A2 `LocalSaveSession`/`commitTimeline` handoff while preserving authority checks, expected-head validation, registry, bundle, and reload behavior. Then retire the legacy writer.

The TS executor, native bootstrap initialization, `commitSession`, generic patch adapter, capture family, and direct provider asset writers have no non-test production value caller. Their implementations and tests remain unchanged. Protected closures include the commit-session tests, generic/ordinary-member tests, capture-specific tests, `runner.test.ts`, and legacy fixtures (`recipe_*`, `ordinary_real_batch.json`, authoring-bundle fixtures, prepared-image producer, and P1 corpus). D31 transcript capture remains unchanged.

D37 ledger wording remains exactly:

- `APP-A4-D37-TRACK`: “dormant: no production caller; follow-up deletion for owner review.”
- `APP-A4-D37-RAW-BIRTH`: “dormant: no production caller; follow-up deletion for owner review.”

## Verification

- HEAD: `dbde9cc37d10ead931694a1e8fd955d798d97bdb`
- Tree: `a24a97b0d59504412b82a15153d035714ae5ba7a`
- `git status --short --branch`: clean
- `git diff --check`: passed
- Targeted `rg` caller census completed for writers, bootstrap, executor, placement, registration, and adapter paths.
- No tests/build/browser/backend/service runs, per task instructions.

The referenced R4 control-doc path was unavailable in this sandbox; prior census/D31/D37 reports were available and used only as historical comparison. Commit message and `DONE` marker were written.