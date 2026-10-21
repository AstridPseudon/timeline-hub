# App M2 popup owner/birth seam — HOME r75 handoff

Date: 2026-10-21  
Scope: App source-only trace and bounded seam proposal  
Status: **NO-CARRIER for a complete occurrence birth; parent-session passthrough is available for reciprocal agreement.**

## Decision

The qualified parent-to-popup path already carries the explicit occurrence identity and the parent command-session authority used by `shot.set` and `occurrenceDuplicate`. It does not currently carry that parent `occurrenceAddMediaPort` into the nested popup provider.

That existing path can supply:

- the explicit owner `occurrence:${canonicalOccurrence.occurrenceId}`;
- the parent session’s retained bundle, local basis, and display-head fence through `OccurrenceAddMediaCapturePort`;
- the authoritative parent `TimelineData` needed by `capture`;
- the selected occurrence’s raw revision and existing child configuration through `PreparedShotComposition`.

It cannot, from the currently existing values, supply an approved **newborn raw child row** and the original five-field `MediaSelection` as one existing carrier. The selected raw child config describes existing children; copying or deriving it would not be a new-birth authority. The ordinary parent asset-drop planner is also the wrong scope. Therefore the occurrence ADD remains visibly refused until App2 and HOME agree on an existing authoritative birth result. No App2 inference is requested.

## Existing source provenance

### Main popup opening and nested provider

1. `src/tools/video-editor/components/AstridTimelineEditor.tsx:95-104` owns `canonicalShotEditor` and the mounted parent runtime.
2. The parent data selector exposes `data` and `dataRef` at `:163-177`; the existing ops selector exposes `shotSet` and `occurrenceDuplicate` at `:178-193`.
3. The canonical occurrence popup opens by setting the selected occurrence at `:386-391`.
4. The original dialog host is `:699-746`. It mounts `LocalTimelineShotBrowser` at `:723-742` with the already-qualified carriers:
   - `shotSetPort={shotSet}` (`:731`);
   - `mediaProvider={runtime.provider}` (`:732`);
   - `shotRef`, `timelineRef`, and `initialComposition` (`:724-730`).
5. The nested provider is in `src/tools/travel-between-images/components/ShotTimelinePreview.tsx:638-656`. It currently receives its own `dataProvider`, local `timelineId`, editability, and initial local data, but no parent command-session port or parent current-data callback.

### Existing qualified parent carriers

- `shot.set` is already captured in `src/tools/travel-between-images/pages/ShotEditorView.tsx:364-392` by `handleSettingsIntent`, passed to `SettingsAutoDisable` at `:547-552`, and uses the parent `shotSetPort` plus `canonicalComposition` and `canonicalOccurrence.occurrenceId`.
- The parent duplicate path is `src/tools/video-editor/components/AstridTimelineEditor.tsx:393-404`. It captures with the mounted parent port, parent `data`, and explicit ``occurrence:${occurrence.occurrenceId}``.
- The existing port is already part of the parent command session: `src/tools/video-editor/hooks/useTimelineCommandSession.ts:307-318,459-473` wraps and returns `occurrenceAddMediaPort` with the existing clean-save fence.
- The exact port signature is `src/tools/video-editor/commands/commitSession.ts:106-129`:

  ```ts
  interface OccurrenceAddMediaCapturePort {
    capture(input: {
      ownerRef: `occurrence:${string}`;
      row: Record<string, JSON>;
      media: MediaSelection;
      current: TimelineData;
    }): OccurrenceAddMediaCaptureBasis;
    finish(basis: OccurrenceAddMediaCaptureBasis, verifiedMedia: VerifiedMedia): {
      command: EditCommand;
      preview: TimelinePatch | null;
    };
    submit(input: { command: EditCommand; preview: TimelinePatch | null }): void;
  }
  ```

- Its implementation at `commitSession.ts:577-618` retains the existing bundle, owner, row, media, local generation/basis, and display head; `capture` rejects a parent-data/head mismatch and `finish`/`submit` reject stale or uncaptured work. This is the existing authority and writer; the proposal does not add another.

### Existing canonical identity, timing, and raw child bindings

- `PreparedShotComposition` already contains `occurrences` at `src/tools/video-editor/data/shotCompositionAdapter.ts:112-141`; each `CanonicalShotOccurrence` has `occurrenceId`, parent document identity, timing, and raw `revision: JsonObject`.
- The local model copies raw child objects from `revision.timeline.clips` at `src/tools/travel-between-images/pages/localTimelineShotModel.ts:164-216`; each local clip retains the raw `clip` object, `clipId`, asset, lane, and timing at `:7-17`.
- Projection binds raw identity without parsing display IDs at `src/tools/video-editor/data/shotCompositionProjection.ts:327-349`: `ownerRef` is `occurrence:${occurrence.occurrenceId}`, `rawClipId` is the authored child ID, and ambiguous/missing identities produce `clipRef: null`.
- Projection retains raw timing/ownership metadata at `:405-438`, including `app.canonical` and `app.canonicalTiming` (`sourceOffsetMs`, speed, duration, occurrence timing). These are read-side bindings, not a newborn-row result.
- The occurrence command validator requires an explicit owner and raw child row at `src/tools/video-editor/commands/occurrenceMediaCapture.ts:184-208,211-250,309-342`. It refuses absent/ambiguous identity, unsupported occurrence mapping, missing raw `id`/`track`/`clipType`, invalid timing, and non-exact media verification.

## Exact NO-CARRIER boundary

The following pieces are nearest but are not an approved birth carrier:

- `src/tools/video-editor/lib/timeline-asset-plans.ts:321-425` (`buildAssetDropEdit`) creates ordinary parent `ClipMeta` and a parent timeline action. It defaults image births to 5 seconds and video rows to a duration/5-second fallback, but it has no occurrence owner, raw child birth result, or occurrence command basis.
- `src/tools/video-editor/commands/provisioning.ts:6-14` (`TimelineProvisionedAsset`) may retain the original `mediaSelection`, but has no owner or raw child row.
- `src/shared/lib/dnd/dragDrop.ts:50-58` (`GenerationDropData`) has generation/variant/media/display metadata only, not the closed five-field selection.
- The nested `ShotTimelineDataProvider` forwards media import and verified-media methods at `src/tools/travel-between-images/components/shotTimelineDataProvider.ts:46-52,369-385`; it does not create or expose the parent command-session basis.

Consequences:

- Owner can be explicit from the selected occurrence object; it must not be parsed from a display ID, timeline ID, or first/latest occurrence.
- The existing raw child config can prove the selected occurrence and its current child semantics, but does not authorize inventing a new child `id`, `track`, placement, hold, or trim values.
- Gallery ingress remains refused where the original five-field selection is absent. File import may be qualified only where `PreparedMediaImport.mediaSelection` survives into the prepared asset; that narrower slice still needs the approved newborn-row carrier.
- Catalog/unplaced ambiguity remains a visible refusal unless existing authoritative context proves that the requested project operation is allowed.

## Bounded HOME-owned proposal for reciprocal agreement

This is a source-only proposal; no product hunk is applied in r75.

### 1. State / Provider

No new store, state authority, command, DTO, or writer is needed. `useTimelineState` already forwards the mounted session port at `src/tools/video-editor/hooks/useTimelineState.ts:1170-1177,1261-1272`; its public ops type already has `occurrenceAddMedia` at `src/tools/video-editor/hooks/useTimelineState.types.ts:235-242,265-273`.

Add only an existing-provider passthrough to `VideoEditorProviderProps` (`src/tools/video-editor/contexts/VideoEditorProvider.tsx:790-822`) and its instance destructuring (`:834-855`):

```ts
occurrenceAddMediaPort?: OccurrenceAddMediaCapturePort;
getOccurrenceAddMediaCurrent?: () => TimelineData | null;
```

At the existing `editorOps` assembly (`VideoEditorProvider.tsx:745-756`), delegate `capture`, `finish`, and `submit` to that supplied port. The delegate must call `getOccurrenceAddMediaCurrent()` at capture time, refuse when it returns null, and pass that parent `TimelineData` to the existing port. `finish` and `submit` must remain direct delegates. The nested provider must never create a second command session or substitute its shot-local `TimelineData`.

This is a passthrough only: the parent session remains the authority, and the existing `useTimelineState`/ops surface remains the state carrier. Do not modify `useAssetManagement` or `useExternalDrop` in this HOME handoff.

### 2. Popup host and local callback props

Thread the same two existing types through the already-mounted popup path:

```ts
// LocalTimelineShotBrowserProps
occurrenceAddMediaPort?: OccurrenceAddMediaCapturePort;
getOccurrenceAddMediaCurrent?: () => TimelineData | null;

// ShotEditorViewProps
occurrenceAddMediaPort?: OccurrenceAddMediaCapturePort;
getOccurrenceAddMediaCurrent?: () => TimelineData | null;

// ShotTimelinePreviewProps
occurrenceAddMediaPort?: OccurrenceAddMediaCapturePort;
getOccurrenceAddMediaCurrent?: () => TimelineData | null;
```

The bounded call-site hunks are:

```tsx
// AstridTimelineEditor.tsx:178-193, 723-742
const { ..., occurrenceAddMedia } = useTimelineOpsSelector((ops) => ({
  ...,
  occurrenceAddMedia: ops.occurrenceAddMedia,
}), shallow);

<LocalTimelineShotBrowser
  ...
  occurrenceAddMediaPort={occurrenceAddMedia}
  getOccurrenceAddMediaCurrent={() => dataRef.current}
/>
```

Then forward those same props unchanged at:

- `LocalTimelineShotBrowser.tsx:165` and its `ShotEditorView` call at `:296-315`;
- `ShotEditorView.tsx:112-131` and its `ShotTimelinePreview` call at `:526-536`;
- `ShotTimelinePreview.tsx:638-656`, where they become the existing `VideoEditorProvider` passthrough props.

The callback reads the parent `dataRef` already selected by `AstridTimelineEditor`; it does not snapshot or reconstruct nested popup data. `canonicalOccurrence.occurrenceId` remains the sole explicit owner input for any later App2 caller.

### 3. What remains reciprocal / not proposed

This passthrough alone does **not** authorize a newborn occurrence add. Before App2 activates the route, the owner must identify an existing source that already returns the approved raw child birth row using the planned semantics and 5-second main policy, plus the original five-field selection for the eligible File-import slice. No new birth DTO, alternate writer, latest-media lookup, display-ID parsing, first-occurrence choice, or guessed track/hold/owner is approved.

Once that existing birth result is identified and agreed, App2 may consume the forwarded existing port with the settled order: capture synchronously, await the exact verified media, finish, then submit; report success only after submit; preserve the draft and visibly refuse on missing port, missing selection, stale basis, or command refusal.

## Verification disposition

No source or test file was changed. Per the task, no actual, browser, build, install, full suite, graph, live-socket, or repeated-44 run was performed. The handoff is based on the source provenance above and remains unverified as an implementation until reciprocal agreement and a bounded product patch exist.
