# M2 opacity `clip.set` contract

Status: Agent candidate, based on `tl/agt-m2-bundle2-final-qualify`.
M2 integration remains held; this document does not change the frozen R4 or
Bundle2 references.

## Scope

Opacity is the first ordinary visual property admitted to the existing native
`clip.set` operation. It adds no operation, endpoint, DTO, renderer behavior,
or fallback writer. The operation remains singleton and accepts only stable
raw clip references:

```text
parent/clip:<raw-id>
occurrence:<occurrence-id>/clip:<raw-id>
```

The owner is explicit in the selector. Shared-shot display rows are not
selectors, and a root/whole-clip replacement is not a valid spelling.

## Closed shape and units

`clip.set@1` keeps required `args.values` and `args.clear` fields. `values`
allows only the existing `hold` field plus:

```json
{"opacity": 0.4}
```

Opacity is the raw canonical fraction in the inclusive range `0..1`, exactly
as the existing main timeline schema and UI use it. Values are JSON numbers;
booleans, strings (including `"40%"`), empty strings, null, NaN, infinity,
and out-of-range numbers are refused. There is no percent conversion,
clamping, default insertion, or normalization.

The only clear spelling is:

```json
{"values": {}, "clear": ["opacity"]}
```

Clear removes the `opacity` leaf. It does not write null or an empty value.
ABSENT, present-null historical data, and present `0` remain distinct in
recorded before-state and generic inverse/redo. A same-value SET is still an
explicit write and remains guarded for ABA-safe undo.

## Capture and guards

The existing capture is the public Agent seam:

```python
from astrid.sdk.timeline._clip_scalar_commands import capture_clip_set

capture_clip_set(bundle, "occurrence:occ-1/clip:picture-1",
                 values={"opacity": 0.4})
capture_clip_set(bundle, "parent/clip:direct", clear=["opacity"])
```

Capture records the original opacity leaf as an exact tagged state and keeps
the existing parent/occurrence identity, source, and media guards. The handler
writes only `clip["opacity"]`; it does not read or replace `params`, arrays,
the root clip, nested namespaces, or unrelated occurrences. Existing
hold/asset/transition-clear captures and their goldens are unchanged.

The generic recorder supplies exact inverse/redo, disjoint-property rebase,
reload portability, and intervening-write/A→B→A refusal. Unknown opaque and
dynamic values survive an opacity clear and undo because no container is
rewritten.

## App handoff

The reviewed App producer is `updateClip` in
`src/tools/video-editor/hooks/useTimelineCommandsService.ts`; its opacity
input is a shallow numeric raw field. The migration target is one `clip.set`
command with the original leaf expectation above. App must preserve the
captured command through the existing commit session and must not send the
legacy `clip.set-look`, whole-row patch, or snapshot replacement for this
field. Transition SET, effects, position, and percent-facing controls remain
separate candidates.

## Evidence

Agent conformance covers the closed schema, UI-shaped SET capture, parent and
occurrence isolation, absent/null/zero distinction, same-value writes,
exact inverse/redo, disjoint parameter rebase, and ABA refusal. The existing
`recipe_m2_app_clip_scalar_fields.json` fixture is intentionally not rewritten.
