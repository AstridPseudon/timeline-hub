# P2/A3 readonly report — ADD27885

## Result

The first independently proved divergence is downstream of selection ownership:

- The reviewed `06014` fix only changes `TimelineEditorCore`’s direct/context-menu selection callback to pass `marqueeOwner` (`TimelineEditorCore.tsx:501-504`). Its test exercises `contextMenu`, not the post-reload ordinary click.
- The failing ADD trace proves the ordinary click selected the new clip: after click, the DOM contains `data-selected="true"` (`ADD trace 0-trace.trace:620`).
- ADD projects the new row as `clipType: hold`; SWAP selects the existing `clipType: media` row (`three-products.p2-popup.spec.ts:887-889`).
- `ShotTimelineMediaControls` derives the label from `canSwap`, which explicitly excludes `hold` (`ShotTimelineMediaControls.tsx:127-132`). Therefore ADD renders the fallback “Add at …” text even though the hold clip is selected; SWAP renders “Selected clip …” for the eligible media clip.

This does not prove owner clearing or failed pointer routing. The pointer path already passes `selectionOwner` through `useClipDrag` (`useClipDrag.ts:407-447`).

## Wholepath bound

Client ADD uses occurrence-raw-track placement (`ShotTimelineMediaControls.tsx:267-275`), applies the prepared-media projection locally (`useTimelineCommandsService.ts:485-524`), captures/enqueues `occurrence.add-media` (`commitSession.ts:602-644`), and sends it through the Runtime commit route (`integrations/runtime/dataProvider.ts:751-767`). Runtime returns the accepted canonical document, identity map, and receipt (`dataProvider.ts:807-827`). After reload, the test reaches the projected clip and fails only at the selected-label assertion (`three-products.p2-popup.spec.ts:867-892`).

## Comparator

Retained SWAP9674 reaches the selected-label assertion successfully for the existing media clip, then fails later during Undo with Runtime 503. It is selection-boundary evidence only; no SWAP gate transfer is claimed.

## Tests/evidence

No test command was run in this readonly investigation.

Retained results:

- ADD27885: readiness passed; one failure at selected-label assertion, `p2-popup-add.xml:1-29`.
- SWAP9674: selected-label boundary passed; later Undo failed at accepted status, `p2-popup-swap.xml:11-31`.
- Worktree remains unchanged and clean.

## Missing input / next step

A product decision is still required: should a selected but non-swappable `hold` clip display a selected identity label, or the current “select one media clip to swap” state? The source currently implements the latter. If the label requirement is authoritative, the minimal remedy is to separate “selected clip” display from `canSwap`; no patch was made because that semantic decision belongs to the designated solution owner.

No gate-closure claim.