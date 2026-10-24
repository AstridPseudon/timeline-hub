# Report — A2/P2 independent whole-path review

- No product files, tests, specs, configs, pins, graphs, or ledgers changed. Worktree is clean.
- Source identity verified: App `c0fe889944` / tree `8e3ef15e`; Runtime `37eb6c7bdb` / tree `be411470`; Agent `079580ca46` / tree `2deab1a1`.

## Definite current defects

1. Mounted element apply fails before transport.

`ElementsLibraryPanel.tsx:46–98` invokes the persistent adapter directly via `adapter.execute(...)`.

`element-adapter.ts:400–405` only records `capturedHead` through `captureForTurn()`. The mutation guard at `element-adapter.ts:457–467` requires that captured head, but `execute()` does not derive it from `authority.getHead()`.

This exactly matches the observed P2 failure:

> “The captured timeline head changed or is missing…”

The failure occurs before `routes.save`, the local outbox, HTTP, Runtime, Agent, reply adoption, reload, or Undo.

Bounded next owner: App A2; bind the mounted panel operation to an actual head/generation capture boundary, then rerun the existing P2 element case.

2. The subsequent element-params writer has a separate missing causal join.

`AstridElementParams.tsx:40` → `ClipEffectsTab.tsx:119` → `PropertiesPanel.tsx:560` → `useClipEditing.ts:247–299` performs a generic selected-clip update with no element gesture basis.

For the occurrence-bearing P2 fixture, `timelineLocalSaveHandoff.ts:267–270` rejects such a save as `child-ownership-unavailable` before v2 encoding. The element-specific reads and atomic merge at `timelineLocalSaveHandoff.ts:337–380` are therefore not reached.

Bounded next owner: App A2/P2; preserve an element causal basis for property edits or provide an equivalent child-safe property operation.

## What is already joined

Once reached, `useTimelineSave.ts:724–749` hands element mutations to the local save handoff. `localSaveSession.ts:159–188` emits the required full-v2 request, including base revision/publication, `doc.patch`, steps, reads, merge, source, label, rationale/group, dry-run, and idempotency key. Runtime’s route/provider checks are present at Runtime `server.py:294–319`, `door.py:160–166`, and `timeline_commit_provider.py:55–90`.

No source evidence indicates a Runtime/Agent defect for the first element failure.

## Challenge to prior proof

The reviewed migration and joined tests do not cover the production caller:

- `element-adapter.test.ts:79–102` explicitly uses `captureForTurn()`.
- `element-adapter.test.ts:104–122` uses an adapter without authority/head, so it bypasses the mounted head guard.
- `VideoEditorProvider.staging.test.tsx:294–305` also calls `captureForTurn()`.

Thus they prove captured/offline adapter behavior, not the direct mounted Elements panel path.

## Separate P3 evidence

P3 readiness/native seed passed (`1 passed, 35.9s`), but Gate 5 failed independently: `page.waitForResponse` timed out after 90s at `three-products.spec.ts:1538` while waiting for a commit POST. Cause remains unknown; no scope or timing inference was made.

## Checks

- `git diff --check` — passed.
- Targeted/type/lint and full suites were not rerun per task instructions; existing central results above were used.

Commit message and `DONE` marker were written as requested.