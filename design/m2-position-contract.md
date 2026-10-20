# Position leaf contract (M2 held)

Published at `/home/user/work/wt/agt-m2-position-set/design/m2-position-contract.md`.

## Actual App mapping

App `src/tools/video-editor/components/PropertiesPanel/ClipPanelBody.tsx`
passes `onChange({ x: value })`, likewise `y`, `width`, `height`.
`hooks/clip-editing/useClipPositioning.ts` resets those four plus `cropTop`,
`cropBottom`, `cropLeft`, `cropRight` by removing their presence.
`lib/timeline-data.ts` copies these exact flat raw clip fields to/from ClipMeta.
`hooks/useTimelineCommandsService.ts#updateClip` spreads `input.patch` onto
the existing clip through `lib/editor-utils.ts#updateClipInConfig`, which updates
only the matching clip ID. Its special rounding applies only to timing `at`.
There is **no nested `position` object**. The raw Agent/main
`astrid/core/timeline/schema/timeline-config.schema.json#/definitions/TimelineClip`
declares all eight as numbers, without ranges. The panel's opacity slider is a
separate ordinary property, outside this position/reset family.

`x`, `y`, `width`, `height` are composition canvas pixels (top-left origin).
Crop fields are fractions of the full box on the named edge: App
`lib/render-bounds.ts#getVisibleBoundsFromCrop` multiplies them by width/height.
Render/display normalization is not a save rule. Negative/offscreen coordinates,
zero/negative sizes and crop fractions outside [0,1] remain finite raw numbers;
this command adds no bounds, clamping, rounding, defaults or unit conversion.

## Command and exports

Extend existing version-1 `clip.set`, no new operation/DTO/endpoint:

```json
{"schema_version":1,"op":"clip.set","version":"1",
 "select":"parent/clip:f2-app-clip",
 "args":{"values":{"x":-120.5,"y":64,"width":1280,"height":720},"clear":[]}}
```

Explicit reset: `args={"values":{},"clear":["x","y","width","height",
"cropTop","cropBottom","cropLeft","cropRight"]}`. Only named leaves are
removed; null/empty are never reset encodings. New SET accepts finite JSON
numbers only, no booleans/strings/null/expressions. Existing expressions, null,
opaque values or absence are preserved verbatim unless that leaf is requested;
undo restores their exact tagged old state.

Existing exports: Python
`astrid.sdk.timeline._clip_scalar_commands.capture_clip_set(bundle, select,
values=..., clear=...)`; native `operations()['clip.set'].parameters` and
`astrid/core/timeline/schema/edit-command.schema.json#/$defs/ClipSetArgs`.
Values/clear remain closed and a strict superset of the published ordinary args.
The Runtime-owned generated client is untouched; its next normal schema generation
must consume the widened canonical schema.

## Guards and portable goldens

Stable parent/occurrence clip/owner and existing media/type basis are retained.
Recorder writes/guards are flat leaf paths (`["x"]`, `["y"]`, etc.). Disjoint
leaves/properties rebase independently; changed same-leaf captures refuse.
Same-value writes still count for inverse history: later writes and A→B→A refuse
old undo, while equal-state forward replay retains existing semantics.
No timing dependencies, evaluator, renderer, sourceNode or client recapture.

New portable fixture:
`tests/editing_conformance/fixtures/recipe_m2_app_clip_position.json` contains the
actual App seedThreeProducts parent/child rows, a panel-shaped box update,
one crop update and reset, commands, records and resulting bundle. Existing
hold/clear/golden fixtures remain byte-identical. Conformance additionally checks
shared occurrence isolation, exact inverse/redo, opaque namespaces and rational fps.
