# H4 timeline UI: how shots are drawn, edited, and opened

Repo: ~/Developer/astrid-video/astrid-local/labs/app-gallery-bar (branch feat/gallery-bar). Editor = src/tools/video-editor (abbrev. VE). Read-only. The repo has uncommitted changes from other work; none were touched.

## 1. Rendering

**Shot group model.** `VE/hooks/useShotGroups.ts`
- `useShotGroups` (L175-260): canonical path maps each occurrence to a `ShotGroup`. The row is the occurrence's `trackId` (`declaredRow`, L207). Children are every action on ANY row whose id is the occurrence id or starts with `${occurrenceId}:` (L191-201, L232-245). So children are found across rows by id prefix, not by row.
- Start and end come from the occurrence interval, not the children (L237-238). Comment at L188-189: "The committed occurrence interval is the geometry authority."
- Colour: `getShotColor` (L167-173) hashes the id into 8 fixed colours. Used for the label and border only (L258, L313).
- `projectCanonicalShotRows` (L129-165) rewrites only a legacy shell's geometry to the occurrence interval; canonical children keep their own absolute times.
- L47-48: "The parent timeline intentionally has no editable child actions for canonical shots." That is a comment, not a gate. I found no code that enforces it.

**Layout.** `VE/lib/timeline-row-layout.ts:70-76`: one row per track in array order, plus data lanes. Row top = `trackRects`.

**Label and border (on the occurrence row only).** `VE/components/TimelineEditor/ShotGroupOverlay.tsx`
- `ShotGroupLabels` (L65-236): a 4px strip at rest, growing to an 18px label with the shot name on hover (L118-119, L172). It sits above the action rect at `TIME_RULER_HEIGHT + top - SHOT_GROUP_LABEL_HEIGHT` (L160). Badges for final video, stale, and task (L193-229).
- `ShotGroupBorders` (L238-337): a 2px border at `left-2, top-2, width+4, height+4` in colour at 60% (L314-324). The box is the occurrence row's rect only. It does not span other rows. Thumbnail on the block (L272-297); a Film icon if no thumbnail (L298-313). Pending blocks pulse (L250-270).
- `TimelineCanvas.tsx`: `positionedShotGroups` at L751-792. `top` = occurrence row's `trackRects.top + ACTION_VERTICAL_MARGIN` (L786). Width = (end-start)*pps (L787). Groups whose row is not the occurrence row are dropped (L753-756).
- `hideShotGroups = isDragging ?? dragSessionRef?.current !== null` at L939. Labels and borders are hidden during a drag (L1303, L1366).
- Rendering order: labels at L1300, grid/actions, then borders at L1364 (zIndex 1).

**Children on shared rows.** The child action is drawn on its own track with its own type colour. Nothing ties it visually to the shot: no shot colour, no border, no label. The only link is `shotName` replacing the clip text (`VE/components/TimelineEditor/ClipAction.tsx:651`, fed by `TimelineEditorCore.tsx:59-70` `shotNameForAction`). `getShotColor` is used only for the label, the border, and the lightbox (`hooks/useVideoEditorLightboxNavigation.ts:245`).

## 2. Interactions

| Action | Exists? | Where |
|---|---|---|
| Select a whole shot | Yes | Label click, `ShotGroupOverlay.tsx:125-135`. `TimelineCanvas.tsx:820-840` `handleSelectShotGroup` clears clips and sets `inspectorTarget` to `kind:'shotOccurrence'`. |
| Move a whole shot on canvas | No UI commit path | Label has no drag handler. `data/shotCompositionEditor.ts:563` `moveCanonicalOccurrence` and L583 `trimCanonicalOccurrence` have no caller in `src/` outside tests. The only caller of the shot-timeline update path is `tools/travel-between-images/components/shotTimelineDataProvider.ts:476`. |
| Trim a whole shot | No UI commit path (same as above) | `trimCanonicalOccurrence` (L583-615) throws unless duration equals the content extent. It allows no empty tail and cannot end before content. So it can only be a no-op or a content edit. |
| Delete a whole shot | Legacy only | `ShotGroupContextMenu.tsx` "Delete shot" (L99). `AstridTimelineEditor.tsx:592` passes `onShotGroupDelete` only when NOT canonical. In canonical mode the item is hidden. "Deconstruct shot" (menu L8) unpins the group. |
| Duplicate a whole shot | Yes (canonical) | `ShotGroupContextMenu.tsx:68` "Duplicate shot" → `AstridTimelineEditor.tsx` `handleDuplicateDocumentShotGroup` → `shotCompositionEditor.ts:631` `duplicateIndependentShot`. |
| Select / move / trim a child | Child select and move exist; not gated for canonical children | Child drag in `hooks/useClipDrag.ts`; resize in `hooks/useClipResize.ts`. `lib/timeline-editability.ts:23-35` has the check API. Canonical lock only while a shot draft is open (`withCanonicalShotDraftLock`, L50-67). I found no per-child canonical gate. The commit path for a canonical child edit was not traced (open question). |
| Drag a child across rows | Generic track drag | `useClipDrag.ts`; no shot-specific rule found. |
| Drag a loose clip into a shot's time range | Nothing shot-aware | No code tags a dropped clip as a shot child. The legacy model is a pinned group (`lib/shot-group-commands.ts:114` buildPinShotGroupMutation, `usePinnedShotGroups.ts`) = a list of clip ids on one track. Canonical children are identified only by id prefix (see §1). |
| Split | Yes | `ClipAction.tsx` split-at-playhead; `useKeyboardShortcuts.ts:316-320` key `s`; `hooks/clip-editing/useClipSplitting.ts`. |
| Copy / paste | No | No `c`/`v`/`x` clipboard keys in `hooks/useKeyboardShortcuts.ts` (keys listed at L244-328: z/y undo-redo, arrows, Ctrl+A, m, f, s, Backspace/Delete, Escape). |
| Undo | Yes | `hooks/useKeyboardShortcuts.ts:244-250` → `useTimelineHistory.ts` (keeps `canonicalHistory` L68, L220). `shotCompositionEditor.ts:663` `CanonicalShotCompositionHistory`. |
| Delete a child | Yes | `hooks/useKeyboardShortcuts.ts:322`; `lib/keyboard-delete.ts`. |
| Double-click a child video clip | Opens the shot dialog for canonical children | `TimelineEditorCore.tsx:604-617` `handleDoubleClickVideoClip`, with `hasResolvableCanonicalTimeline` (L123). Same in `TimelineEditorCoreBody.tsx:578-585`. |

## 3. Existing "enter shot" / sub-timeline surfaces

**Yes, a sub-timeline editor already exists. It is a dialog, not a page.**
- Entry, double-click on a shot label: `VE/components/TimelineEditor/ShotGroupOverlay.tsx:136-146`. It calls `onShotGroupOpen(group.canonicalIdentity)`, falling back to `onShotGroupNavigate` for legacy.
- Entry, double-click on a canonical child clip: `TimelineEditorCore.tsx:604-617`.
- Wiring: `components/AstridTimelineEditor.tsx:587` `onShotGroupOpen={hasCanonicalOccurrences ? handleOpenCanonicalOccurrence : undefined}`. `handleOpenCanonicalOccurrence` at L309-314 calls `setCanonicalShotEditor(occurrence)`. The comment says the parent route is left untouched.
- Dialog: `AstridTimelineEditor.tsx:615-650`. A Radix `Dialog`, 4xl, 90vh, with an sr-only title "Edit {shotId}". Escape closes it (L620-634). It renders `LocalTimelineShotBrowser` with `shotRef=stableDeepLink` and the canonical draft callbacks.
- `tools/travel-between-images/pages/LocalTimelineShotBrowser.tsx:159` → `pages/ShotEditorView.tsx` → `components/ShotTimelinePreview.tsx:626-638` (`VideoEditorProvider` + `ShotTimelineEditorSurface`). `ShotTimelinePreview.tsx:315` renders a full `TimelineEditorCore` for the shot's OWN timeline, with its own `RemotionPreview` (L281). So the shot's internal tracks are edited in the same editor component.
- No breadcrumb. No "back to parent timeline" control inside the dialog. The only "Back" text is "Back to Shots" in `ShotEditorView.tsx:478`, shown on not-found. Close is via the dialog's X or Escape.
- Shot inspector: `components/PropertiesPanel/PropertiesPanel.tsx:167-186` `ShotOccurrenceInspectorSection`. It shows the header "Canonical shot occurrence" and fields: shot, occurrence, revision, track, interval. No editable fields. Shown when `inspectorTarget.kind === 'shotOccurrence'` and no clips are selected (L260-262, L500-501).
- Chapters: no chapter UI in `src/tools/video-editor`. The only hit is `sequences/metadata.ts:80` (a prompt guidance string about chapter titles). Chapter rows and labels do not exist in the editor. Chapters are shots, per the CONTEXT note.
- Searched terms with no editor hit: openShot, focusShot, drill, breadcrumb, ShotPanel, shotId in URL params. Not checked: the global router for `shotRef` params in travel-between-images. `LocalTimelineShotBrowser` does import `useLocation` and `shotLocation` from `shared/lib/tooling/toolRoutes.ts`, so a route may exist for the shot list (not traced further).

## 4. Copy quoted

- `VE/tour/tourScript.ts:84`: "The finished shot is trimmed to 14 seconds on the top row, ready to play."
- `VE/tour/tourScript.ts:87`: title "Your agent uses everything on your timeline to create the final shot".
- `VE/tour/tourScript.ts:98`: recap "Finished shot".
- `VE/tour/timeline/tourStages.ts:86` `tourTrackOrder` doc: "The tracks that exist after `stage`, top row first."
- `VE/tour/timeline/tourStages.ts:118`: "vocabulary: `track.add` (above the current top row)…" (a code comment, not user copy).
- `VE/hooks/clip-editing/useClipTextOverlay.ts:70-72` (code comment for the Text button): "New text at the playhead, in front of the picture: on the front visual track (the top row) when it has room there, otherwise on a new track above it."
- `VE/components/PropertiesPanel/ClipInspectorActions.tsx:5-12` (code comment): "The clip's action grid on touch devices, where it is the one way to move, trim, split, mute or change the track of a clip… An action the clip's type cannot do is not shown… one that has nowhere to go now (Track up on the top track) is disabled." Actions are "Move", "Trim", "Split", "Mute", "Track up", "Track down" (L39-44).
- Shot-level strings in the UI: "Canonical shot occurrence" (PropertiesPanel L170); "Open shot actions" (ShotGroupOverlay L182); "Duplicate shot", "Delete shot", "Deconstruct shot", "Jump to Shot" (ShotGroupContextMenu).
- Nothing in the tour or inspector copy says a shot is a layer or describes layering across shots. The copy is about "top row" / "track above" for ordinary clips.

## 5. Assessment (opinion, label as such)

Note: the timeline canvas draws children flattened onto their own shared rows. The projection (`data/shotCompositionProjection.ts` ~L271-315, `tracksFor`) merges shot tracks into the parent track list. So a loose clip on a lower row visually sits "under" the shot block but the block only exists on the occurrence row. The lookup `useShotGroups.ts:191-201` finds children by id prefix anywhere, so the model already "knows" children belong to the shot. The gap is presentation, not identity.

**(a) Shot as one block on its row; children hidden in the parent, shown only inside the shot.** Opinion: this is the smallest honest change.
- Reuses: `ShotGroupBorders` and `ShotGroupLabels` as-is (block, thumbnail, label, badges). `TimelineCanvas.positionedShotGroups` (L751-792) already computes the block rect.
- Change: filter child actions out of `renderRows` (`TimelineEditorCore.tsx:343-352` / `TimelineEditorCoreBody.tsx:336`, where `projectCanonicalShotRows` runs) so only the occurrence block shows. Keep the child ids for hit-testing via the dialog.
- Gap: block move and trim have no UI commit path (see §2). Those must be wired to `moveCanonicalOccurrence` / `trimCanonicalOccurrence` before the block can be dragged. `trimCanonicalOccurrence` as written forbids any trim that is not the content extent, so it would need a rule change too.

**(b) Double-click to enter the shot as its own timeline, with a breadcrumb back.** Opinion: the surface already exists. The shot dialog (AstridTimelineEditor.tsx:615-650) already renders a real `TimelineEditorCore` on the shot's own tracks. The remaining work is presentation: a visible "Parent timeline / shot" breadcrumb and a back control, plus the nested-layer rendering of the shot inside the parent.
- Reuses: `LocalTimelineShotBrowser` / `ShotTimelinePreview` / `TimelineEditorCore`; `handleOpenCanonicalOccurrence`; `ShotGroupLabels.onDoubleClick` (ShotGroupOverlay L136-146).
- Cost: low, since the dialog exists. But it does not change the parent view, which keeps showing the flattened children (the misleading part).

**(c) Keep children on shared rows.** Opinion: misleading as the owner describes it. A loose clip on a lower row visibly runs under a shot whose children are drawn on their own rows; the block border covers only the occurrence row. Keep only if the parent view is labelled as a flattened view.

Recommendation (opinion): (a) plus (b). Hide the children in the parent (a), keep the block as the one layer on its occurrence row (already drawn), and make double-click (b) the only way to see inner layering, with a breadcrumb. Reuse `ShotGroupOverlay`, the existing dialog, and `TimelineEditorCore`. The first blocker is the missing block-move/trim commit path, not the rendering.

## Open questions (not verified)
- Whether a canonical child drag or resize in the parent commits through the projection or is blocked. I did not trace `useClipDrag` → commit for canonical children.
- Whether `shotLocation` / `shotListLocation` in `shared/lib/tooling/toolRoutes.ts` gives a deep-linkable shot route.
- Whether the `legacy` lane (userId not null) renders shots as nested `TimelineRenderer` (CONTEXT says so). This is preview/render, not the timeline UI, so out of scope here.
