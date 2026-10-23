# A4/D31 reachability audit

Verdict: **PASS for the scoped YES verdict**—equivalent production transcript-association semantics are reachable. **Literal `transcriptAssociateCapture` remains test-only/unreachable**, as expected.

Production chain verified:

`VideoEditorPage.tsx:196-198` → local extension/catalog registration → reviewed allowlist → `BrowserVideoEditorProvider.tsx:221-239` → lifecycle synchronization/activation → `extension.tsx:44-56` → `VideoEditorAssetPanelSurface.tsx:54-70,128` → `ExtensionPanelHost.tsx:72-105` → `TranscriptPanel.tsx:415-426` → binding/useTimelineState/useProjectTranscriptHost → `project-transcript-host.ts:600-674,747-857`.

Legacy obligations:

- Config-mirror fallback: **not equivalent**. It exists only in `transcriptAssociateCapture.ts:501-506`; production uses canonical construction in `timeline-save-utils.ts:31-70`.
- Atomic review delete/move: **reachable and preserved** through `reconcileTranscriptReferences.ts:125-145`, invoked by the host at `project-transcript-host.ts:621-651`.
- Collision/shared-row `identity_conflict`: **not equivalent**. The literal helper throws these errors at `transcriptAssociateCapture.ts:321-329,351-357`; production reconciliation preserves occupied destinations and skips non-unique owners at `reconcileTranscriptReferences.ts:113-139`.

Important scope correction: the mounted page’s normal persistence path is `saveTimelineAtHead → publishParentComposition` (`useTimelinePersistence.ts:412-416`, `dataProvider.ts:1028-1159`), not `dataProvider.commitTimeline` (`dataProvider.ts:750-762`). Therefore the appended v2 request/reply contract was not independently evidenced as the mounted transcript caller. If D31 requires the v2 commit path specifically, that narrower claim is **FAIL**.

Agent audit at `09b44830519898d5811bee1c4b1230deb77e6ee5`: bounded CLI/SDK/sheets inspection found no transcript-association operation or carrier. Only generic `doc.patch`, transcript sync, and `clip.anchor` paths were found (`commands.py:29-138`, `cli.py:4008-4044`, `timeline_sheet.py:720-778`). Generic document patch/import APIs were not treated as association evidence.

App head verified: `419dcab90fd7db0314884efb67d23a0c0c989860`.

Tests: **none run**, per the read-only/no-behavioral-tests brief. Only read-only `git show`, `git grep`, `rg`, and line inspection were used.

No source, test, or design files changed. Commit message and `DONE` marker written.