# App M2 scalar-ingress implementation brief

Status: docs-only handoff, based on App `tl/integration` at `ea3461e0c` and the
frozen App scalar-session candidate `dc6caeb3f`. The candidate is not yet the
owner-binding fix and is not treated as integrated. The bounded first slice is:

1. explicit parent transition clear (`None`/`Remove`), and
2. occurrence-scoped asset clear plus hold, using the preserved original
   journeys as the behavior contract.

The next worker should compose the native `clip.set@1` session seam and the
owner-binding validation first, then wire only these scalar UI actions through
the same `clipScalarPort`. Do not make the existing snapshot writer a scalar
fallback.

## Native meaning and operation boundary

The wire operation is `clip.set`, schema/version `1`, addressed only by an
explicit `parent/clip:<RAW_ID>` or `occurrence:<OCCURRENCE_ID>/clip:<RAW_ID>`
selector. Its `args` must contain at least one of `values` or `clear`.

| App intent | Native request | Meaning and limit |
| --- | --- | --- |
| authored hold value | `values: {hold: positive finite number}` | SOURCE seconds, not projected timeline pixels/frames or row duration; do not include `at`, `speed`, `from`, or `to` |
| clear asset | `clear: ["asset"]` | removes the authored asset field while retaining clip identity, clip type, registry, and unrelated leaves; this is not media swap |
| transition `None`/`Remove` | `clear: ["transition"]` | removes the canonical incoming transition; no successor/predecessor lookup and no transition SET |

`clear` means authored ABSENT. `undefined`/omitted is a partial-update omission,
not an explicit clear; `null`, empty strings, booleans, non-finite values, and
unknown/duplicate/disjoint fields are invalid for this operation. A hold clear
needs the explicit positive authored window required by the Agent helper; it is
not inferred from a compiled/default value. Compound scalar fields may share
one command only when they are one atomic authored gesture. Hold must not be
combined with trim/source-window changes, `from`/`to`, or speed changes. Those
need a separate Agent operation. Hold-after-move also requires the Agent
successor that updates agreeing `for` leaves; this App brief must not emulate it.

Transition SET, transition duration/params edits, asset SET, add-media, and
media swap are outside this native slice. In particular, `swap` or
`occurrence.swap-media` must never be invented as “asset clear”.

## Actual App ingress map

These are the current paths on the integration base, not proposed APIs.

| Surface | Current path and current meaning | M2 action |
| --- | --- | --- |
| Hold control | `src/tools/video-editor/components/PropertiesPanel/ClipPanelBody.tsx:130-160,317-375` calls `onChange({hold: value})`; `PropertiesPanelBody.tsx:542-557` supplies `handleSelectedClipChange`; `useClipEditing.ts:235-283` turns it into `applyRowsEdit`; `timeline-data.ts:270-414` reconstructs a broad config and can rewrite hold/source fields; persistence eventually reaches `useTimelinePersistence.ts:399-405` → `saveTimelineAtHead`/`saveTimeline`. | Capture authored presence before a control default is materialized; preview and submit a scalar hold through `clipScalarPort`. A committed hold is one native command, not a rows/config replacement. |
| Transition None/Remove | `ClipTransitionSection.tsx:100-105,130-147,264-275` currently calls `onChange({transition: undefined})`; the same selected-clip path becomes a broad rows edit. Selecting a transition, changing duration, or resetting defaults currently constructs a transition SET/patch. | Translate only explicit `None`/`Remove` to `clear: ["transition"]`. Keep transition SET/duration/params on a refused or legacy path until an Agent transition operation exists; do not send `undefined` or `null` as native clear. |
| Asset controls | The ordinary Properties panel has variant/update controls (`PropertiesPanelBody.tsx:578-586`) but no current core “clear asset” control. Add-media/swap code is in `commands/media.ts:213-292`; `useTimelineState.ts:982-995` builds local `add-media`/`swap` commands. | The first asset-clear UI action must be explicit and call the same scalar port with the occurrence owner. Do not reuse local `swap`, `updateClip`, or resolved-config replacement. Asset SET remains a separate Agent media operation. |
| Public command facade | `useTimelineCommandsService.ts:604-656` `updateClip` merges into the resolved clip and calls `applyValidatedMutation`; `setClipParams` (`:990-1003`) delegates to it. | Do not route scalar fields through these broad methods. Keep them only for still-unmigrated non-scalar behavior. |
| Generic SDK patch host | `useTimelineOps.ts:250-283` validates a broad patch, compiles it, and calls `commitData(..., {save:true})`. Its consumers include `source-map-runtime.ts:171,191` and extension/dev contexts. | Do not turn `useTimelineOps.apply` into the scalar port. Migrate only the concrete scalar producers and leave generic consumers intact until their own migration. |
| Popup/shot editor | `src/tools/travel-between-images/components/shotTimelineDataProvider.ts:435-590` `saveTimeline` computes and publishes a whole canonical graph through `shotCompositionAdapter.publish`, while retaining recovery drafts. | No scalar fallback through `saveTimeline`. A popup scalar action may use the same port only after it has an explicit occurrence binding. Keep draft recovery as outbox recovery. Delete the whole-graph popup writer only after native popup add/swap coverage exists; the selected-media Runtime read is still a known gap. |
| Placement | `src/shared/lib/placement/placementService.ts:119-238` uses document mutation/CAS. | Separate concern; do not claim scalar `clip.set` covers placement. |

The broad rows path is especially unsafe for this slice: `rowsToConfig` snaps
timeline positions to the project frame grid and serializes/deserializes
`asset`, source windows, hold, and transitions together. It cannot preserve the
raw authored ABSENT-vs-present distinction required by clear.

## Required native seam and owner binding

Use the frozen candidate’s narrow seam, not a new App framework:

- `src/tools/video-editor/commands/clipScalarGesture.ts` provides capture,
  finish, and submit around a `ClipScalarCapturePort`.
- `src/tools/video-editor/commands/commitSession.ts` owns the durable command,
  original authored bundle, generation/identity guards, ACK/retry, and outbox.
- `src/tools/video-editor/hooks/useTimelineCommandSession.ts` exposes the
  scalar port and applies the existing legacy-clean gate.
- `src/tools/video-editor/lib/clip-scalar-preview.ts` applies a leaf-level
  local preview without the lossy rows serializer; `timeline-patch.ts` keeps
  the explicit `clear` validation.

Before capture, bind the selected display clip to production projection data
from `src/tools/video-editor/data/shotCompositionProjection.ts:44-66,326-434`.
Use the canonical identity’s `projectId`, `parentDocumentId`, `occurrenceId`,
`rawClipId`, `ownerRef`, and `clipRef`; then validate the same selector against
the original authored bundle. The projection explicitly says `rawClipId` is
the authored ID and that `clipRef` is null for missing, duplicate, or
unaddressable identities. Never infer ownership from a display ID or trust an
opaque/stale `app.canonical.clipRef` alone.

Reject without preview or outbox append when the binding is missing, stale,
duplicated, forged, unaddressable, or does not match the selected projected
row. Parent rows bind the parent raw row; occurrence rows bind the explicit
occurrence and raw clip. This is the required follow-up to the candidate
`dc6caeb3f` capture path, which currently accepts a cast `clipRef` too broadly.

Capture the original authored bundle and guards before the first UI mutation.
Retain that exact command basis and prepared body through ACK; do not recapture
from the resolved projection after an ACK or use a snapshot save to recover.
For a partial/compound UI edit, all targeted scalar commands need stable
bindings and an atomic user-visible result: either all requested targets are
accepted, or the operation refuses visibly and retains the draft. A later
local edit must remain queued against its own original basis rather than being
silently folded into an earlier command.

## Concrete first implementation

1. Land the owner-binding correction in `commitSession.ts` and its permanent
   cross-owner, stale, wrong-raw-ID, duplicate, unaddressable, valid-parent,
   and valid-occurrence tests. Preserve the native goldens from the candidate
   helper; do not widen selectors or add a fallback.
2. Wire `ClipPanelBody` hold commit/blur to the scalar session. The adapter
   must capture authored presence (not a default hold or compiled duration),
   preview the hold in SOURCE seconds, and finish once per committed gesture.
3. Wire `ClipTransitionSection` `None` and `Remove` to the same session as an
   explicit transition clear. Preserve the existing positive UI tests for
   transition SET/duration; those actions remain unsupported by this native
   slice and must not be rewritten as if SET were valid.
4. Add the smallest explicit occurrence asset-clear affordance only where its
   canonical occurrence binding is available. It emits `clear: ["asset"]` and
   leaves registry/media metadata untouched. Do not add popup media swap here:
   that still needs the Runtime-owned selected-media read and a separate media
   command.
5. If bulk selection is exposed, issue separately bound scalar commands (or a
   deliberately atomic batch with equivalent all-or-nothing semantics). Never
   send one display-ID patch whose targets are inferred from row IDs.

## Tests and deletion gates

Preserve and extend the actual behavior nodes, especially:

- `tests/e2e/local/three-products.spec.ts:452-500,519-543,565+` for the
  original hold/asset-clear/transition-clear concurrent journey and retained
  drafts. Keep its positive expectations; do not “fix” a missing native path by
  rewriting them to expect refusal.
- `src/tools/video-editor/components/PropertiesPanel/ClipPanel.transition.test.tsx`
  for explicit `None`/Remove and the still-positive SET/duration UI behavior.
- Candidate scalar conformance/session/preview nodes:
  `tests/editing_conformance/test_recipe_clip_scalar_fields.py`,
  `tests/sdk/test_timeline_clip_scalar_provider.py`,
  `tests/editing_conformance/test_commit_runtime_clip_scalar_fields.py`, and
  the App candidate tests for `clipScalarGesture`, `commitSession`,
  `useTimelineCommandSession`, `clip-scalar-preview`, and `timeline-patch`.
  These are reference test nodes, not evidence that the candidate is already
  integrated.

The deletion gate is zero legacy traffic for migrated producers: no
`saveTimeline`, `saveTimelineAtHead`, `publishParentComposition`,
`config-replaced`, or old Astrid/save route during scalar capture, refusal,
preview, submit, ACK, or retry. Only after popup add/swap has its own native
commands and preserved recovery tests may `shotTimelineDataProvider.saveTimeline`
and `shotCompositionAdapter.publish` be removed. Do not delete generic
`useTimelineOps`, draft recovery, or unrelated snapshot producers early.

No tests/build/typecheck were run for this docs-only task, per the task
instruction. The next worker should run the targeted App tests after the
owner-binding and first-slice changes; a full/browser suite remains for the
central test service.
