# App M2 literal-position consumer mapping

## Bounded result

The current App model and serializer can carry the eight Agent literal-position leaves as flat clip fields. The live ordinary position UI does not use the native `clip.set` command path, however: it writes a rows/config snapshot and then lowers through `rowsToConfig`. The existing native App scalar consumer also rejects these eight fields. Therefore this is bounded serializer/model compatibility evidence only; it is not native qualification.

No App product files or live callers were changed.

## Immutable source identities

- Agent source commit: `f2a2cfbb58926b7c9d47d206ae294acf376b0c2e`.
- Agent source tree: `8c5674a5e329ab8dc5dcb4711251268a61b81847`.
- Agent schema identity: `b06d49c1` (full SHA-256: `b06d49c1be645ec6631bad109963697a3e5eb956786953751fd57b650be19836`) for `astrid/core/timeline/schema/edit-command.schema.json` at that commit.
- App evidence tree: worktree `tl/ap2-m2-main-app-literal-geometry-mapping-0433`, `HEAD 6e267027137f11288a8e20ee8cf226209be60408`, based on `hub/tl/integration`.

The requested App `origin/main` could not be inspected because this checkout has no `origin` remote/ref for the App repository. The mappings below are from the current App integration worktree. This missing ref did not change any settled plan decision.

## Exact mapping

The Agent source defines eight finite numeric, flat `clip.set.args.values` leaves. For a set, the proposed existing command shape is `values: {<leaf>: <raw number>}` with no corresponding `clear` entry. For a clear, it is `values: {}` with `clear: [<leaf>]`. The native preview shape already used by App is `clip.update` with the same flat payload and clear list.

| Real App field/source | Proposed existing command field | Canonical authored leaf | Unit and compatibility evidence |
| --- | --- | --- | --- |
| Position X, `ClipPanelBody.tsx:408-410`; `onChange({x: value})` | `clip.set.values.x = n`; clear leaf `x` | `ClipMeta.x` (`timeline-data.ts:54`), then `rowsToConfig` next clip (`timeline-data.ts:320-355`) and raw clip `x` | Literal canvas pixels. No scale, track, default, rounding, or clamp conversion. Shape is compatible; live native caller is absent. |
| Position Y, `ClipPanelBody.tsx:411-414`; `onChange({y: value})` | `clip.set.values.y = n`; clear leaf `y` | `ClipMeta.y` (`timeline-data.ts:55`), then raw clip `y` | Literal canvas pixels. Same bounded compatibility and native-path caveat. |
| Width, `ClipPanelBody.tsx:415-418`; `onChange({width: value})` | `clip.set.values.width = n`; clear leaf `width` | `ClipMeta.width` (`timeline-data.ts:56`), then raw clip `width` | Literal canvas pixels. The current control displays `min=0` and `max=compositionWidth`; those are UI control bounds, not permission to add capture clamping. Agent source requires raw finite values, including zero/negative values when supplied by the source. |
| Height, `ClipPanelBody.tsx:419-422`; `onChange({height: value})` | `clip.set.values.height = n`; clear leaf `height` | `ClipMeta.height` (`timeline-data.ts:57`), then raw clip `height` | Literal canvas pixels. The current control displays `min=0` and `max=compositionHeight`; no conversion or silent clamp belongs in the command mapping. |
| Crop top | `clip.set.values.cropTop = n`; clear leaf `cropTop` | `ClipMeta.cropTop` (`timeline-data.ts:58`), then raw clip `cropTop` | Literal edge fraction. There is no current ordinary crop input in `ClipPanelBody`; this is a serializer/command mapping, not evidence of a live crop caller. |
| Crop bottom | `clip.set.values.cropBottom = n`; clear leaf `cropBottom` | `ClipMeta.cropBottom` (`timeline-data.ts:59`), then raw clip `cropBottom` | Literal edge fraction. Preserve the raw number; do not convert from a display percentage. |
| Crop left | `clip.set.values.cropLeft = n`; clear leaf `cropLeft` | `ClipMeta.cropLeft` (`timeline-data.ts:60`), then raw clip `cropLeft` | Literal edge fraction. No current ordinary crop input was found. |
| Crop right | `clip.set.values.cropRight = n`; clear leaf `cropRight` | `ClipMeta.cropRight` (`timeline-data.ts:61`), then raw clip `cropRight` | Literal edge fraction. No current ordinary crop input was found. |

The Agent contract explicitly permits negative/offscreen/zero/negative-size values and crop values outside `[0,1]` as literal finite source values. App's `render-bounds.ts:8-45` and `overlay-bounds.ts:4-33` normalize/clamp values for derived rendering; those functions are not an authored capture conversion and must not be used to lower this source. There is no Agent degree/rotation leaf in this set, so no degree alias is proposed. App opacity remains a separate `[0,1]` field and is not part of this mapping.

## Current live App path

For the four ordinary position controls, the real call chain is:

1. `PropertiesPanelBody.tsx:567-583` passes `handleSelectedClipChange` to `ClipInspector`; `PropertiesPanel.tsx:562-573` passes the same handler to `ClipPanelBody`.
2. `ClipPanelBody.tsx:408-422` emits a flat partial `ClipMeta` patch.
3. `useClipEditing.ts:241-289` separates an optional `at` value and calls `applyRowsEdit`; `useClipEditing.ts:82-103` creates the rows mutation.
4. `useTimelineCommit.ts:479-529` merges `metaUpdates` into App's current metadata and calls `materializeData`.
5. `useTimelineCommit.ts:304-337` calls `rowsToConfig`; `timeline-data.ts:320-413` copies defined flat fields into the next clip and serializes the snapshot. Action timing is frame-snapped in `timeline-data.ts:281-323`; the geometry values themselves are not converted there.

The current reset path is also snapshot-based:

- Single reset: `useClipPositioning.ts:16-33` spreads the clip and assigns all eight fields `undefined`, then calls `applyConfigEdit`.
- Bulk reset: `useClipPositioning.ts:35-60` puts all eight fields `undefined` in `metaUpdates`, then calls `applyRowsEdit`.

That local `undefined` behavior means omission from the snapshot; it is not the Agent command representation. The equivalent native command must use an explicit clear list:

```text
values: {}
clear: [x, y, width, height, cropTop, cropBottom, cropLeft, cropRight]
```

The target must remain the existing raw clip identity/occurrence binding resolved by App's `clipScalarPort`; no alias or new DTO is implied. A reset must not turn into `null`, an empty value, or a default geometry value.

## Native consumer incompatibilities

The native seam exists but is not yet a consumer for this UI:

- `clipScalarGesture.ts:7-29` builds the existing `clip.update` preview, but its `ClipScalarArgs` clear union is only `hold | asset | transition`.
- `clipScalarCapture.ts:189-212` validates `clip.set` values only for the existing `hold | transition | elementRef` set and the same three clearable scalar fields. An x/y/width/height/crop key is rejected as an unknown change today. Its explicit-clear behavior (`clipScalarCapture.test.ts:155-172`) confirms the required absent-versus-null distinction, but only for the existing scalar cohort.
- `commitSession.ts:758-783` exposes the clip scalar port; its batch branch currently accepts only `values: {}` with `clear: ['transition']`. Ordinary geometry `onChange` and the position reset handlers do not call this port.
- The current command tests (`clipScalarCapture.test.ts:42-56`, `118-128`, `155-172`, `228-256`) preserve raw occurrence/sibling data and test explicit clear/invalid-null behavior for the existing fields. They are witnesses for the existing authority and absence rules, not native qualification of the eight new leaves.

Thus the exact incompatibility is not the flat `ClipMeta`/`rowsToConfig` shape; it is the missing App native command consumer and caller wiring. The Runtime bounded ACK and Agent source identity do not establish that missing Main/App lowering.

## Separation of effects, params, and opaque data

`timeline-data.ts:320-355` carries geometry, `effects`, `params`, `app`, and the other clip fields separately. `timeline-domain.ts:158-197` lists them as distinct `TIMELINE_CLIP_FIELDS`, while `timeline-domain.ts:274-294` clones opaque timeline extras. The snapshot path passes the current config/extras into `rowsToConfig` (`useTimelineCommit.ts:304-337`) and preserves authored fields when present (`timeline-data.ts:357-365`). The proposed geometry mapping therefore changes only one flat geometry leaf or its explicit clear; it does not merge into `effects` or `params`, drop opaque siblings, or rewrite timing/order/source occurrence data.

## Evidence and scope

Targeted tests run successfully:

```text
./node_modules/.bin/vitest run --no-cache --config config/testing/vitest.config.ts src/tools/video-editor/commands/clipScalarCapture.test.ts src/tools/video-editor/lib/render-bounds.test.ts src/tools/video-editor/lib/render-bounds.validation.test.ts
3 files passed, 40 tests passed

./node_modules/.bin/vitest run --no-cache --config config/testing/vitest.config.ts src/tools/video-editor/components/PropertiesPanel/ClipPanelBody.test.tsx src/tools/video-editor/components/PropertiesPanel/TransitionPreservation.test.tsx src/tools/video-editor/hooks/useClipEditing.test.ts
3 files passed, 61 tests passed
```

An initial attempt using `--configLoader=runner` failed during Vitest startup because the config accessed `__dirname`; the retry without that loader passed. No full, browser, live-socket, install, schema/pin, capture-activation, or product qualification run was performed.

The requested HOME STATUS file was not present in the scratchpad paths searched; the App manager STATUS/INBOX and the settled PLAN were read. This report records that missing input rather than inferring a decision from it.

Commit message path: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-main-app-literal-geometry-mapping-0433/commit-msg`.

Changed live callers: none. Product worktree status: clean.
