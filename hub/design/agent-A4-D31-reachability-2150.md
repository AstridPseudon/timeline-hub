## D31 reachability report

Result: **NO** — no mounted production caller reaches `transcriptAssociateCapture` or emits `transcript.associate` at the audited source heads.

Sources:

- Agent: `c36ca8c94b695b0e25b7d42c89f194661f187423`, tree `50689a445fcae5ca54ba2e7e8f1d99e9a2c43c92`.
- App: `419dcab90fd7db0314884efb67d23a0c0c989860`, tree `a52d35b7ebecbed59ec87a758dc5f2b85e64f7f1`.
- Frozen published App candidate: `8f0c2484463e9b666d184a744d52e252984e551a`, tree `26ad064632fac9ff123670aa7d6ed0e3d8f89178`; it contains none of the relevant current transcript/save source, so it cannot establish current consumer reachability.

Callgraph:

`editorRuntimeAssembly.tsx:650` → `useTimelineState.ts:627` → `useTimelineSave` → `useProjectTranscriptHost.ts:22-67`.

The mounted host is supplied `save.commitData` and `save.flushPendingSave` at [`useTimelineState.ts:1146-1157`](/home/user/work/app/src/tools/video-editor/hooks/useTimelineState.ts:1146). Transcript import/source selection reaches `project-transcript-host.ts:600-674`, where it calls the separate `reconcileTranscriptReferences` helper and then `commitData(next, { save: true, semantic: true })` at [`project-transcript-host.ts:621-651`](/home/user/work/app/src/tools/video-editor/lib/project-transcript-host.ts:621).

The actual persistence path is:

`commitData` → `createTimelineLocalSaveHandoff` → `createLocalSaveSession` → persisted outbox → `doc.patch`.

The request construction is [`localSaveSession.ts:159-185`](/home/user/work/app/src/tools/video-editor/commands/localSaveSession.ts:159): API version, project/timeline scope, base revision/publication pair, commands, label, steps/patch, merge/read metadata, `source: app`, and `dry_run: false`. The idempotency key is generated and persisted by [`commitOutbox.ts:464-483`](/home/user/work/app/src/tools/video-editor/commands/commitOutbox.ts:464), then passed to `commitTimeline` by [`localSaveSession.ts:180-185`](/home/user/work/app/src/tools/video-editor/commands/localSaveSession.ts:180).

`transcriptAssociateCapture.ts` remains dormant: its exports and `transcript.associate` envelope are at [`transcriptAssociateCapture.ts:517-573`](/home/user/work/app/src/tools/video-editor/commands/transcriptAssociateCapture.ts:517), but value-import search found no production caller. Its retained test is 397 lines / 40 assertions.

The mounted App helper has only partial overlap with old behavior:

- Fallback is transient source projection at [`project-transcript-host.ts:339-390`](/home/user/work/app/src/tools/video-editor/lib/project-transcript-host.ts:339), not the old config-mirror fallback.
- The helper can delete/move a review key for a sole owner at [`reconcileTranscriptReferences.ts:125-146`](/home/user/work/app/src/tools/video-editor/data/typed/reconcileTranscriptReferences.ts:125), but this is not the legacy atomic `transcript.associate` path.
- Shared/collision cases are preserved/left unchanged at [`reconcileTranscriptReferences.ts:105-115`](/home/user/work/app/src/tools/video-editor/data/typed/reconcileTranscriptReferences.ts:105), not refused with legacy `identity_conflict`.

Agent registry [`commands.py:69-106`](/home/user/work/wt/agt-A4-D31-reachability-2150/astrid/sdk/timeline/commands.py:69) has `doc.patch` and `clip.add-media`, but no `transcript.associate`. SDK, CLI, and sheets all route through the generic commit session: [`commit_session.py:161-251`](/home/user/work/wt/agt-A4-D31-reachability-2150/astrid/sdk/timeline/commit_session.py:161), [`cli_native.py:401-423`](/home/user/work/wt/agt-A4-D31-reachability-2150/astrid/packs/timeline/cli_native.py:401), and [`timeline_sheet.py:876-881`](/home/user/work/wt/agt-A4-D31-reachability-2150/astrid/sdk/timeline_sheet.py:876).

C0 shapes remain represented in App types: accepted/merged, canonical document, receipt, records, bindings/effects/dependencies, history, undo steps, preview `would_status`/`null` receipt, and structured errors at [`timeline-commit-types.ts:67-112`](/home/user/work/app/src/integrations/runtime/timeline-commit-types.ts:67). Agent preview/error preservation is at [`_commit_preview.py:83-105`](/home/user/work/wt/agt-A4-D31-reachability-2150/astrid/sdk/timeline/_commit_preview.py:83) and [`_commit_errors.py:74-110`](/home/user/work/wt/agt-A4-D31-reachability-2150/astrid/sdk/timeline/_commit_errors.py:74).

No repository edits or tests were run, per the read-only/source-only brief. Worktree status remained clean. No secrets were handled; credential scan result: 0 modified files.

Recommendation: keep the dormant legacy implementation and its tests unchanged. This evidence supports the bounded **NO** branch; retirement or semantic migration still requires an authoritative mounted replacement and Agent/Runtime proof.