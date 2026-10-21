# Position leaf contract

This is a narrow extension of the existing version-1 `clip.set` recipe. It
does not add an operation, DTO, endpoint, scene, caller pin, or selected/custom
element schema.

## Main source of truth

App's `ClipMeta` is flat (`src/tools/video-editor/lib/timeline-data.ts:43-76`).
`ClipPanelBody` writes `x`, `y`, `width`, and `height` as individual fields
(`components/PropertiesPanel/ClipPanelBody.tsx:412-445`), while
`useClipPositioning` clears those four fields plus `cropTop`, `cropBottom`,
`cropLeft`, and `cropRight` (`hooks/clip-editing/useClipPositioning.ts:16-60`).
The writer spreads the patch into clip metadata and rounds only `at`
(`hooks/useTimelineCommandsService.ts:604-655`); it does not write a nested
position object or a stored scale field.

The four geometry leaves are literal canvas pixels. Crop leaves are literal
edge fractions. All eight are finite raw numbers: negative/offscreen values,
zero or negative sizes, and crop values outside `[0,1]` remain literal. There
is no clamping, normalization, rounding, defaulting, or display-track-scale
conversion in capture.

## Command contract

`clip.set.values` accepts only the eight flat leaves in addition to its existing
fields. `clear` explicitly removes presence; absence is a no-op, and `null`,
empty strings, or other reset encodings are rejected. Set and clear may not
overlap. Opaque fields, timing, order, and unrelated occurrence/source state
remain untouched.

The existing target binding supplies parent or explicit occurrence ownership,
stable clip identity, source/type/media basis, and occurrence mapping. Writes
are guarded by the original leaf value, so stale same-leaf edits refuse while
disjoint edits rebase. Inverse and retry/ABA checks retain the same guards.

This is a source-only qualification. It makes no browser, render, physical,
live-socket, or Runtime-generated-DTO claim.
