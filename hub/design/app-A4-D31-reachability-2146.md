## D31 result: YES

A production-mounted App transcript UI reaches legacy transcript-association semantics.

Callgraph:

`VideoEditorPage.tsx:196-197` → reviewed `haus.astrid.transcript-lane` → `extension.tsx:44-56` registers `TranscriptPanel` → `TranscriptPanel.tsx:415-427` → `transcript-panel-binding.ts:106-115` → `useTimelineState.ts:1146-1158` → `useProjectTranscriptHost.ts:22-68` → `project-transcript-host.ts:600-674`.

Production entrypoints are:

- Project source selection: `project-transcript-host.ts:747-755`
- Transcript import: `project-transcript-host.ts:756-826`
- Source promotion: `project-transcript-host.ts:827-857`

The association writes through `commitData` at `project-transcript-host.ts:651`, then the normal timeline persistence/outbox path reaches `dataProvider.ts:750-762`.

The literal `transcriptAssociateCapture.ts` module has no production import/callers; only its own implementation and tests reference it. The reachable legacy behavior is the equivalent production implementation in `project-transcript-host.ts`.

Legacy obligation status:

- Atomic review-key delete-and-move is consumed by `reconcileTranscriptReferences.ts:125-145`, called from `project-transcript-host.ts:621-627`, and persisted atomically at line 651.
- The old config-mirror fallback in `transcriptAssociateCapture.ts:501-506` is not consumed; current persistence uses canonical data construction.
- The old `identity_conflict` refusal for collisions/shared ownership (`transcriptAssociateCapture.ts:321,353`) is not consumed. Current reconciliation silently preserves occupied destinations (`reconcileTranscriptReferences.ts:113-115`) and skips non-unique ownership (`:131-139`).

Agent CLI/SDK/sheets do not reach this path: no transcript-association operation is registered in `commands.py:29-131`; CLI transcript support is narration sync (`cli.py:4008-4014`); sheets only materialize transcript inputs for `clip.anchor` (`timeline_sheet.py:720-759`). Generic `doc.patch` is not counted as a semantic association path.

Current identities recorded:

- App: `419dcab90fd7db0314884efb67d23a0c0c989860`
- Agent: `09b44830519898d5811bee1c4b1230deb77e6ee5`

No source edits were made. No tests were run per the read-only D31 brief. Provider semantic migration on the existing carrier is still required before retirement; do not add a generic metadata guard or delete the deferred helper/tests.