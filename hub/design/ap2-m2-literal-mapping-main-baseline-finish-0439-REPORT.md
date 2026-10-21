# App M2 literal-position mapping: imported Main evidence

## Bounded result

I inspected the exact imported Main object `860d43b331fb4422b16bc0dbd7b08666a0c766a0` (tree `ea4eabb8eb469df63fd1d515f84982d85b2f14cc`) directly. The Main serializer still carries the eight Agent literal-position leaves as flat, optional clip fields, with the same names and absence shape used by the Agent `clip.set` source. The live Main UI remains snapshot-based: it emits `ClipMeta` patches, rebuilds rows, and serializes through `rowsToConfig`; it does not use the native `clip.set` consumer.

The earlier mapping table needs three bounded corrections from this exact Main source:

1. Main has a live preview crop-drag UI. It stores crop values as edge fractions, clamps and normalizes them for the gesture, and writes zero crop values as `undefined` (omission).
2. Main preview move/resize writes stored x/y/width/height through inverse track-scale conversion. The property-panel single-clip controls write their numeric values directly, while the bulk controls explicitly clamp width and height to the composition bounds.
3. Main reset paths use `undefined` snapshot fields, and the serializer omits undefined fields. The equivalent Agent command representation remains an explicit `clear` list, not null, an empty value, or a default geometry write.

Therefore the Agent field names and flat serializer shape are unchanged-compatible, but Main UI lowering is not raw/unbounded for every gesture. This is bounded source and serializer compatibility evidence only; it is not native qualification, activation, or a decision to widen a consumer.

No App product files or live callers were changed.

## Immutable source identities and missing-ref history

- Agent source commit: `f2a2cfbb58926b7c9d47d206ae294acf376b0c2e`.
- Agent source tree: `8c5674a5e329ab8dc5dcb4711251268a61b81847`.
- Agent schema identity: `b06d49c1` (full SHA-256 `b06d49c1be645ec6631bad109963697a3e5eb956786953751fd57b650be19836`) for `astrid/core/timeline/schema/edit-command.schema.json` at that commit.
- Imported Main commit read directly: `860d43b331fb4422b16bc0dbd7b08666a0c766a0`.
- Imported Main tree: `ea4eabb8eb469df63fd1d515f84982d85b2f14cc`.

The requested App `origin/main` remote/ref is absent in this checkout. I did not fetch, substitute current code, or treat the integration worktree as upstream Main. The exact imported Main object above is the source for all Main file:line evidence in this report. The missing-ref condition did not change any settled plan decision.

## Agent contract compared with exact Main

The Agent schema at `edit-command.schema.json:2106-2137` defines `x`, `y`, `width`, and `height` as finite raw canvas pixels with no bounds or conversion. It defines `cropTop`, `cropBottom`, `cropLeft`, and `cropRight` as finite raw edge fractions with no clamping or normalization. The clear enum includes all eight leaves at `2141-2155`; `values` and `clear` are required at `2161-2163`.

The existing command mapping remains:

```text
set:   values: {x|y|width|height|cropTop|cropBottom|cropLeft|cropRight: number}, clear: []
clear: values: {}, clear: [the leaf or leaves]
```

The exact Main comparison is:

| Leaf | Exact Main UI evidence | Main unit and absence behavior | Comparison with Agent `f2a2cfbb` |
| --- | --- | --- | --- |
| `x` | `components/PropertiesPanel/ClipPanelBody.tsx:416-418` sends `onChange({ x: value })`; preview move writes via `OverlayEditor.tsx:357-360, 457-460`. | Numeric canvas/composition pixels in the property panel. Preview drag stores track-local values after inverse scale at `OverlayEditor.tsx:147-158`; an absent field falls back to `0` when a position override exists at `160-185`, otherwise the clip-type default box is used. | Field name and flat numeric leaf are unchanged. The “no scale conversion” wording was too broad: it is true for the property-panel patch, not the preview drag path. Agent source itself remains raw/unconverted. |
| `y` | `ClipPanelBody.tsx:419-422`; preview move path as for `x` at `OverlayEditor.tsx:357-360, 457-460`. | Same pixel and absence rules as `x`. | Same exact difference as `x`. |
| `width` | `ClipPanelBody.tsx:423-426` sends the numeric patch and declares `min=0`, `max=compositionWidth`. Bulk path `BulkClipPanelBody.tsx:273-281` explicitly clamps to `[0, compositionWidth]`. Preview resize uses `OverlayEditor.tsx:414-431` and writes through inverse track scale at `457-460`. | Numeric pixels. Main has real UI/gesture bounds in these paths; serializer absence is omission. | Flat field and unit match, but Main UI is bounded in places while Agent `clip.set` accepts any finite raw number, including negative values. Do not silently add those UI clamps to the Agent command contract. |
| `height` | `ClipPanelBody.tsx:427-430` declares `min=0`, `max=compositionHeight`; bulk path `BulkClipPanelBody.tsx:279-284` explicitly clamps to `[0, compositionHeight]`; preview resize is `OverlayEditor.tsx:414-431, 457-460`. | Numeric pixels, with the same Main bounds and omission behavior as `width`. | Same exact difference as `width`. |
| `cropTop` | Preview crop gesture calculates a fraction from pointer delta at `OverlayEditor.tsx:392-397`, then clamps/normalizes at `400`; it writes `nextCropValues.cropTop || undefined` at `448-455`. | Edge fraction, not a display percentage in the stored field. Zero is omitted by the gesture; nonzero values are stored. Render uses the fraction as a CSS percentage at `VisualClip.tsx:235-242`. | Field name and fraction unit match. Main gesture clamping/normalization and zero omission differ from Agent’s raw finite/no-clamp contract. |
| `cropBottom` | `OverlayEditor.tsx:385-391` computes the fraction, `400` normalizes, and `452` writes zero as `undefined`. | Same edge-fraction and absence behavior as `cropTop`. | Same exact difference as `cropTop`. |
| `cropLeft` | `OverlayEditor.tsx:378-383` computes the fraction, `400` normalizes, and `453` writes zero as `undefined`. | Same edge-fraction and absence behavior as `cropTop`. | Same exact difference as `cropTop`. |
| `cropRight` | `OverlayEditor.tsx:371-376` computes the fraction, `400` normalizes, and `454` writes zero as `undefined`. | Same edge-fraction and absence behavior as `cropTop`. | Same exact difference as `cropTop`. |

The prior table’s statement that no ordinary crop input exists in `ClipPanelBody` is still true for that inspector, but it was incomplete: Main’s `OverlayEditor` is a live crop UI. No Agent degree/rotation leaf is present, so no degree alias is proposed. Opacity remains separate and is not part of this eight-leaf mapping.

## Main reset and crop values

Main has three relevant reset/fill behaviors:

- The inspector single-clip reset is `hooks/clip-editing/useClipPositioning.ts:16-33`. It spreads the clip and assigns all eight fields `undefined`, then calls `applyConfigEdit`.
- The bulk inspector reset is `useClipPositioning.ts:35-60`. It sends all eight fields as `undefined` in `metaUpdates` and calls `applyRowsEdit`.
- The preview reset button is `components/PreviewPanel/OverlayEditor.tsx:799-820`: it preserves x/y, sets width/height to the composition dimensions, and clears all four crops with `undefined`. The adjacent fill button at `826-842` sets x/y to `0`, sets width/height to composition dimensions, and clears all crops.

These are snapshot omissions, not Agent command clears. For a native command equivalent of the inspector reset, the bounded representation remains:

```text
values: {}
clear: [x, y, width, height, cropTop, cropBottom, cropLeft, cropRight]
```

Main’s renderer also distinguishes absence from a supplied value. `VisualClip.tsx:208-234` uses normal fit sizing when all eight geometry/crop fields are absent; when any override exists it uses absolute positioning with missing x/y defaulting to `0` and missing width/height defaulting to composition dimensions. It defaults absent crops to `0` at `235-242` and only emits a clip path when a crop is nonzero. This is render-time fallback, not a serializer write and not a reason to manufacture default authored values.

## Main serializer and live path

The exact imported Main serializer evidence is:

- `lib/timeline-data.ts:43-61` declares all eight fields as optional numeric `ClipMeta` properties.
- `lib/timeline-data.ts:163-182` copies all eight fields from the resolved clip into default metadata without changing their units.
- `lib/timeline-domain.ts:158-176` includes all eight fields in `TIMELINE_CLIP_FIELDS`.
- `lib/timeline-data.ts:312-332` copies all eight fields from each row metadata object into `nextClip`.
- `lib/timeline-data.ts:371-380` serializes a field only when `nextClip[field] !== undefined`; undefined is omitted. A runtime null would not be omitted by this check, but the typed Main UI reset paths above use undefined and do not produce null.

The live ordinary path is still snapshot-based:

1. `PropertiesPanel.tsx:545-560` connects bulk and single property-panel callbacks.
2. `ClipPanelBody.tsx:416-430` emits x/y/width/height patches; `OverlayEditor.tsx:448-460` emits preview geometry/crop patches.
3. `useClipEditing.ts:133-140` and `235-283` lower those patches to `applyRowsEdit`.
4. `useTimelineCommit.ts:304-337` calls `rowsToConfig`; the geometry values themselves are not frame-snapped or otherwise converted there.

The native seam remains an incompatibility, not a completed path: the existing `clipScalarCapture` and `clipScalarGesture` cohort does not accept these eight leaves, and these live callbacks do not call that native port. No native consumer was widened here.

## Effects, params, and opaque siblings

Main carries geometry separately from `effects`, `params`, and `app` in `timeline-data.ts:312-347`; the canonical field allow-list keeps the geometry fields separate at `timeline-domain.ts:158-197`. The bounded mapping therefore does not merge into effects/params, drop opaque siblings, or change occurrence identity. Any future native adapter must preserve that separation and use explicit clears for absence.

## Evidence and scope

No tests were run for this finish slice, as directed. The earlier mapping worker’s historical targeted evidence remains unchanged and was not replayed:

```text
3 files passed, 40 tests passed
3 files passed, 61 tests passed
```

No build, browser, full suite, live-socket, install, schema/pin, capture-activation, or product-qualification run was performed for this slice.

Required status inputs were read: the settled PLAN, app2 status at `hub/status/app2.md`, app2 manager inbox at `scratchpad/orch/managers/app2/INBOX.md`, and App status at `hub/status/app.md`.

Changed live callers: none. Product worktree: no product files changed.

Decision: keep the Agent mapping table’s names, units, flat serializer shape, and explicit-clear representation, but record the exact Main UI bounds/track-scale/crop-normalization differences above. This is the narrowest conclusion supported by the imported Main object and does not claim activation.
