# App M2 popup File-import birth — existing serializer proposal (r81)

Status: **UNAPPLIED; reciprocal agreement requested; File-import occurrence birth remains refused until the raw-row mismatch is resolved.**

This is one bounded proposal for the Runtime-qualified File-import path only. It
does not change product source, the r78 parent-port passthrough, or App2-owned
row/drop hooks. Gallery, no-selection, parent/list-level, audio, group, and
other unsupported shapes remain refused.

## Existing source to reuse

The Main popup's existing local editor conversion is `rowsToConfig`:

```ts
rowsToConfig(
  rows: TimelineRow[],
  meta: Record<string, ClipMeta>,
  output: TimelineOutput,
  clipOrder: ClipOrderMap,
  tracks: TrackDefinition[],
  pinnedShotGroups?: TimelineConfig['pinnedShotGroups'],
  extras?: Pick<TimelineConfig, 'clips' | 'theme' | 'theme_overrides' | 'generation_defaults' | 'app'>,
): TimelineConfig
```

Source: `src/tools/video-editor/lib/timeline-data.ts:272-414`.
The same conversion is used by the existing prepared-media materializer at
`src/tools/video-editor/commands/media.ts:521-558`. The popup provider's
`createCanonicalTimeline` at
`src/tools/travel-between-images/components/shotTimelineDataProvider.ts:153-200`
is not a birth builder: it retains/rewrites already-produced config clips for
canonical publication. Therefore the proposed mapping reuses `rowsToConfig`,
not a new popup DTO or writer.

## One concrete File-import mapping

The eligible ingress is a Runtime `prepareMediaImport` result. Runtime captures
the original five-field `MediaSelection` in
`src/integrations/runtime/dataProvider.ts:1640-1711`; image/video file import
keeps it in `PreparedMediaImport.mediaSelection` and
`useAssetManagement.prepareGenerationAsset` forwards that same object into
`TimelineProvisionedAsset.mediaSelection` at
`src/tools/video-editor/hooks/useAssetManagement.ts:210-261`.

For the selected canonical occurrence, App2 would consume exactly this
source-backed tuple after the existing parent/session passthrough is present:

```ts
{
  ownerRef: `occurrence:${canonicalOccurrence.occurrenceId}`,
  row: serializedPlannedChild,
  media: preparedAsset.mediaSelection,
}
```

The occurrence is the explicit selected `canonicalOccurrence` already carried
by `ShotEditorView`/`ShotTimelinePreview`; no display ID, first occurrence, or
latest metadata is consulted. The track and placement come from the original
drop context and existing planner:

1. `TimelineDropPosition.trackId` and `.time` are passed to
   `planAssetDropTarget` (`src/tools/video-editor/lib/timeline-asset-plans.ts:237-310`),
   which selects an existing compatible visual track from the popup's current
   `TimelineData` or refuses/creates the already-planned target.
2. `buildAssetDropEdit` at
   `src/tools/video-editor/lib/timeline-asset-plans.ts:321-427` is called once
   with that planned track, the prepared asset key/entry, the snapped time, the
   existing clip-span policy, and its returned reserved `clipId`.
3. The existing plan is materialized, without inventing another authority, by
   passing its rows/meta/order through `rowsToConfig`:

```ts
const config = rowsToConfig(
  plan.rows,
  { ...current.meta, ...plan.metaUpdates },
  current.output,
  plan.clipOrderOverride,
  current.tracks,
  current.config.pinnedShotGroups,
  current.config,
);
const serializedPlannedChild = config.clips.find((clip) => clip.id === plan.clipId);
```

This is a source-only witness of the proposed mapping, not a new exported
function. The exact field flow in the existing serializer is:

| Planned Main value | `rowsToConfig` output | Agent birth field |
| --- | --- | --- |
| `plan.clipId` / action `id` | `clip.id` | `row.id` (reserved before capture) |
| action `start` | rounded `clip.at` | `row.at` |
| `track.id` / `ClipMeta.track` | `clip.track` | `row.track` |
| `ClipMeta.asset` | `clip.asset` | `row.asset` (must equal `media.asset`) |
| `ClipMeta.clipType` | `clip.clipType` | `row.clipType` |
| image `ClipMeta.hold` | rounded `clip.hold` | positive `row.hold` |
| video `ClipMeta.from/to/speed` | `clip.from/to/speed` | video source window plus positive `row.hold` |

The approved Agent capture signature is
`capture_occurrence_add_media(bundle, owner, row, media, *, verified_media,
consumed=())` (`/home/user/work/agent/astrid/sdk/timeline/native_occurrence_media_commands.py:263-270`).
The current App-side equivalent is exactly
`captureOccurrenceAddMedia(bundle: AuthoredBundle, ownerRef: string, row: Row,
media: MediaSelection, inputs: readonly VerifiedMedia[]): OccurrenceMediaBasis`
at `src/tools/video-editor/commands/occurrenceMediaCapture.ts:348-355`.
Its raw-row validator requires explicit `id`, `track`, `clipType`, `asset`,
literal `at`, positive `hold`, and for video `from/to/speed`; it also requires
the selected occurrence's active visual child track and bounded local timing.
The App port must pass this row unchanged after the exact verified-media read,
then finish and submit.

The Agent design fixture agrees with this shape: the approved auto-placement
contract specifies video `{from, to, hold, speed}` and a visual image/video
clip kind (`/home/user/work/agent/docs/design/m2-auto-placement.md:25-26`),
not Main's editor-only `hold` clip type or a trim-only video row.

## Fail-closed result of the source trace

The existing conversion cannot currently produce an Agent-valid occurrence
birth row for either visual file kind without a semantic repair that this task
does not authorize:

- Image: `buildAssetDropEdit` creates `clipType: 'hold'` and `hold: 5` at
  `timeline-asset-plans.ts:383-395`. `rowsToConfig` preserves that value at
  `timeline-data.ts:321-355`. Agent `validateClip` accepts only `media` or the
  verified kind (`image`/`video`) at `occurrenceMediaCapture.ts:211-250`, so
  `clipType: 'hold'` is refused.
- Video: `buildAssetDropEdit` creates `clipType: 'media'`, `from: 0`, `to`, and
  `speed: 1` at `timeline-asset-plans.ts:397-410`. `rowsToConfig` emits the
  source window at `timeline-data.ts:367-376` but does not emit `hold` in this
  branch. Agent requires positive `hold` and checks `to - from === hold`, so
  the serialized row is refused before capture.

`createCanonicalTimeline` does not repair either mismatch. The exact missing
raw semantics are therefore `clipType: 'image'` for an image birth and
`hold = to - from` for a video birth (with the existing planned `at`, track,
ID, and source window retained). App2 must not synthesize those fields from a
display projection or a second planner. Until Main supplies a callback result
that is already compatible with the approved raw-row contract—or the shared
existing conversion is explicitly corrected by its owner—the File-import
occurrence branch must refuse and preserve the draft.

The smallest existing callback handoff is the existing `handleAssetDrop`
signature in `UseAssetManagementResult`:
`handleAssetDrop(assetKey, trackId, time, forceNewTrack, insertAtTop,
preparedAsset, removeClipId)`. Its already-qualified `preparedAsset` preserves
the original selection, while `trackId`/`time` preserve the original drop
context. It does **not** return a raw child row; that is the exact missing
input, not permission to synthesize one in App2. No new store, writer, public
DTO, latest-media lookup, or owner inference is proposed. The r78 parent-port
passthrough remains separately owned and is not edited here.

## Reciprocal boundary for App2

App2 is asked to agree to exactly one bounded consumer contract:

- activate only when the selected canonical occurrence, original
  five-field File-import selection, and an Agent-valid raw child row are all
  present;
- call capture, await the exact verified-media result, finish, and submit in
  that order; report success only after submit;
- refuse on missing selection, missing/incompatible row, missing port, stale
  basis, unsupported track/timing, gallery/no-selection, or unsupported shape;
- never fall back to ordinary parent placement for an explicit occurrence
  attempt, and keep transient placeholder cleanup limited to a still-transient
  `uploading-*` row.

This request is intentionally blocked on the two exact serializer semantics
above. It does not ask App2 to infer or normalize a row locally.

