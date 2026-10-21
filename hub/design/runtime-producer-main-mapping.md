# Runtime producer/Main mapping

Status: source-only mapping for the Main producer question. No Runtime/App
consumer, schema, pin, release, or production change is made here.

## Reviewed identities

- Agent producer source: `57af3fffe192ad369c4282d9ab3a67efd57dc51c`
  (`57af3ff`), and literal-position source:
  `f2a2cfbb58926b7c9d47d206ae294acf376b0c2e` (`f2a2cf`). The supplied
  handoff is `design/peer-agent-to-runtime-app2-producer-position-source.md`.
- App/Main witness: commit
  `1557c312b999ddc0a21c1728acbc64052ef6491f`, tree
  `cf94daef960fe1426f6f50e4000b00c0fc42867e`. Its transcript and source-map
  blobs are identical at the inspected witness, App `origin/main`, and App
  `tl/integration`; the witness is an ancestor, not either branch head.
  App `origin/main` is `860d43b331fb4422b16bc0dbd7b08666a0c766a0`; App
  `tl/integration` is `968bbad09449f419ab63782fca49cad805068333`.
- Runtime inspected at `tl/integration` `b92d3e7a05eec65c142294ef4873edd059e9b31d`.

## Field mapping

| Main witness field | Existing canonical carrier | Units / authority | Finding |
| --- | --- | --- | --- |
| `duration` | `clip.set.values.hold` | Source seconds; `hold/speed` is timeline duration | **Resolved in this caller.** `captionDurationSeconds()` computes the source value at `extension.ts:85-93`; `outputValue.duration` is the fingerprint/source-map surface at `:394-402`; the emitted operation already writes `hold: duration` at `:435-447`. Agent schema describes `hold` as positive finite source seconds (`edit-command.schema.json:2101-2105`). No separate `duration` command value should be invented. |
| `clip.update` | `clip.set` for authored scalar/producer leaves; separate position `clip.set` for geometry | `mode: 'merge'` is not an Agent command argument | **Bounded consumer gap.** Main emits a `TimelinePatch` operation, not an `EditCommand`. The existing App native capture recognizes `clip.update` only when payload is `{values, clear}` (`genericPatchCapture.ts:55-83`); the witness payload is direct fields plus `mode` (`extension.ts:435-447`) and therefore falls through to the legacy patch compiler, not native `clip.set`. |
| `track` | `clip.add` row for a new parent clip; no exact existing destination-track `clip.move` mapping found | Main patch field is a track ID | **Unresolved.** Main's compiler explicitly excludes `track` and `at` from existing-clip merge writes (`timeline-patch.ts:1272-1288`), so `clip.update` does not move an existing clip. Agent `clip.move` v1 has only `args.on` (`edit-command.schema.json:451-464`), binds the current track (`capture.py:143-152`), and writes only timing (`capture.py:223-233`). Do not put a destination track into `clip.set`; a retrack consumer decision is required if track can differ. |
| `at` | Existing `clip.move` with `args.on`; `clip.add.row.at` for a new parent clip | Absolute timeline seconds; Agent move is fixed-start/non-ripple | **Resolved for time, but must be split.** The Main field is not carried in producer `clip.set`; it belongs to the placement operation. Agent's exact move capture is `capture.py:253-256`. |
| `x`, `y`, `width`, `height` | Separate position `clip.set.values` leaves | Raw composition-canvas pixels; no display-scale conversion, clamping, or normalization | **Resolved by Agent position source.** App stores flat leaves (`timeline-data.ts:44-61`) and the Agent position contract accepts the same eight flat leaves (`f2a2` schema change and `docs/design/m2-position-contract.md:18-30`). |
| `cropTop`, `cropBottom`, `cropLeft`, `cropRight` | Separate position `clip.set.values` leaves, or `clear` for reset | Raw edge fractions; reset is explicit absence | **Resolved by source contract.** App reset removes all eight leaves (`useClipPositioning.ts:16-31`); Agent position source makes set/clear closed and disjoint. |
| `text` | Producer `clip.set.values.text` | Known leaves only: `content`, `fontSize`, `color`, `bold`, `align` | Agent writes each incoming known leaf (`57af3ff` `_clip_scalar_commands.py:49-58`), preserving unmentioned text siblings. The Main compiler's direct `text` assignment is a shallow replacement, so it is not a lossless consumer mapping. |
| `label` | Producer `clip.set.values.label` | Literal string | Agent producer source accepts the top-level leaf; omit `mode`. |
| `app.__generated__` | Producer `clip.set.values.app.__generated__` as the complete generated-metadata leaf | Existing managed owner; fixed identity fields must remain unchanged | Main creates the metadata at `sourceMap.ts:251-285` and emits it at `extension.ts:445`. Agent requires an existing managed clip and preserves identity/fixed fields (`57af3ff` `_clip_scalar_commands.py:19-46`), then writes leaf paths (`:154-162`). The consumer must not replace the whole `app` object or filter provenance/opaque siblings. |

## Actual caller trace

1. `renderTranscriptAsCaptions()` snapshots the reader, builds the patch,
   validates it, and calls `ctx.creative.timeline.apply(patch)` at
   `src/tools/video-editor/dev/transcript-lane/extension.ts:754-774`.
2. `buildTranscriptCaptionPatch()` computes a frame-boundary-preserving
   duration from `timelineStart`, `timelineEnd`, and output fps at
   `extension.ts:85-93,352-361`. It puts that value under `duration` only in
   `outputValue` for generated-output fingerprinting (`:394-419`), then emits
   `clip.update` with `hold: duration`, `track`, `at`, geometry, text, label,
   and `app.__generated__` (`:421-449`). Thus the exact existing
   `duration -> hold` lowering is local to this producer; there is no generic
   Runtime duration conversion to rely on.
3. `TimelineOps.apply()` first enforces the local patch version, then routes a
   patch to native capture only when `classifyGenericPatch()` is not
   `unsupported` (`useTimelineOps.ts:244-275`). The generic classifier accepts
   scalar `clip.update` only in the `{values, clear}` form
   (`genericPatchCapture.ts:55-83,109-149`). The transcript direct payload is
   not that form, so the observed path is validation/compile/`commitData`, not
   native command capture (`useTimelineOps.ts:277-324`).
4. On that observed path, `compileTimelinePatch()` shallow-merges payload keys
   into the existing clip (`timeline-patch.ts:1229-1289`) and copies selected
   keys into `meta` (`:1291-1315`). It skips `track` and `at` during an
   existing-clip `clip.update`; nested `text` and `app` are assigned as whole
   values. This is not equivalent to Agent's lossless leaf capture: it can
   drop unknown text siblings and existing `app` siblings such as `managedBy`.
   The compiler then serializes rows/config (`:1936-1960`), and `apply()` calls
   the existing `commitData` path (`useTimelineOps.ts:316-324`).

`sourceMap.ts:251-285` is metadata construction, not an authority for timeline
mutation. It defines the generated-object identity/provenance shape; the
timeline mutation authority is the patch compiler in this witness and the
Agent command provider in the canonical path.

## Required atomic consumer batch

For an existing clip, the producer proposal must be lowered as one atomic
batch with these logical members:

1. placement member for `at` (`clip.move` with Agent's exact `on` argument);
2. producer `clip.set` for `hold`, `label`, known text leaves, and the
   complete existing-owner generated metadata leaf;
3. position `clip.set` for any of the eight flat position/crop leaves.

The Main `track` field must not be silently stuffed into either `clip.set` or
Agent `clip.move`: the inspected Agent v1 source has no destination-track
argument. If a differing destination track is a real producer requirement,
the required retrack carrier is a bounded GAP for the orchestrator/Agent
manager to resolve. For a new parent clip, `clip.add` remains the existing
complete-row path; Agent requires `id`, `clipType`, `track`, `at`, and positive
`hold` in that row (`_clip_commands.py:16-61`, schema `:818-854`), so the
consumer cannot forward Main's minimal `clip.add` payload unchanged.

All members must retain the original target ownership, source/type/media basis,
unknown clip fields, unknown text/app siblings, and generated metadata
identity. No partial or filtered save is supported by this finding. No native
Runtime behavior, HTTP behavior, activation, pin, or release is claimed.
