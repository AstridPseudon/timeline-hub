# Handoff: ap2-P2-popup-seam-review-1002

## Verdict

**REFUTE the hard blocker.** Base `23b0901ba` has the A3 receiver and a reachable replacement action, but lacks the popup-specific media-import/replacement control. The frozen qualified App ref and SDK ref contain the faithful production caller and closed Agent+Runtime fixture needed to finish P2.

## What is present on base

- Production popup route: `ShotEditorView.tsx:355-365` → `ShotTimelinePreview.tsx:518-530` → `createShotTimelineDataProvider` with the parent A2 `timelineDataProvider`.
- Receiver: `shotTimelineDataProvider.ts:709-789` verifies exact occurrence/child roots, reads Runtime selection identity, and emits `occurrence.fork` then `occurrence.add-media`/`occurrence.swap-media`; `:1107-1139` invokes it in the A2 save.
- Reachable replacement action: `TimelineEditorCore.tsx:836` → `useStaleVariants.ts:161-196` (`Update to current variant` → primary variant lookup → registry patch/save). This is not a `parentClipSwapMediaPort` caller.
- Exact search confirms `parentClipSwapMediaPort` has no production caller on base; it occurs only in `commitSession.ts` and tests. This confirms the narrower current-base caller gap, not a wholly absent replacement capability.

## Existing faithful route

Use the frozen qualified App ref `origin/codex/handover-timeline-r4-20261019-candidate-app-qualified`:

- `ShotTimelineMediaControls.tsx` is the real mounted caller. It uses Runtime media import, `prepareGenerationAsset`, occurrence context capture, and `commands.addClip` with `replaceClipId` for swap or normal drop placement for add.
- Frozen `ShotTimelinePreview.tsx:265-267` mounts it in the popup.

Use the frozen qualified SDK ref `origin/codex/handover-timeline-r4-20261019-candidate-sdk`:

- `tests/fixtures/timeline_editing/tiny_publishable.json` + `tests/sdk/test_popup_media_226.py:fixture()` build an exact canonical closure with a shared source-mapped occurrence and request-bound selected media identity.
- `test_public_narrated_shared_media` covers add/swap, selected-occurrence isolation, sibling preservation, inverse, and idempotent replay.
- `tests/sdk/popup_media_wire226.py` runs the closed RuntimeCommitService path; `astrid/sdk/timeline/commit.py` enforces exact selected media/project/catalog/source-mapping identity and scope refusal.

The current App A3 tests already assert the v2 command order and envelope shape, but their manually assigned generation/variant IDs should be replaced/supplemented with the exact source-mapped closure/media-selection helper. Extend that existing helper for two valid old/new media selections for current v2 SWAP; do not require user data, invent an authority, or use working aliases as physical identity.

## Required next action

Port the known mounted caller and fixture helper, then run the real popup route through the parent A2 `POST /commits`. Preserve the full C0 v2 request/reply shape, accepted/merged/refused behavior, canonical child/parent preservation, reload, and guarded Runtime undo. Do not scope promised ADD/SWAP/shared-fork/selected-child behavior away.

