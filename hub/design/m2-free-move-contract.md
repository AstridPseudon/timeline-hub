# Parent free multi-clip move — review candidate, not a freeze

Worker `agt-m2-free-move-set`, base `8fe7a42f`, 2026-10-20.
This contract is implemented on the worker branch only. Agent manager review,
official Runtime artifact generation, coordinated pins and actual App integration
proof are still required. PLAN M1 must be recorded before any M2 merge. All three
preserved App `it.fails` remain unchanged. No live-release claim.

## Closed command

Operation `clip.move-set`, version `"1"`, `schema_version: 1`, `select: "parent"`.
Exact args (all three keys required; no unknown keys):

```json
{
  "members": [
    {"clip": "parent/clip:clip-2", "track": "parent/track:V3"},
    {"clip": "parent/clip:clip-1", "track": "parent/track:V2"}
  ],
  "anchor": "parent/clip:clip-2",
  "on": 3
}
```

`members` is a nonempty ordered array of closed `{clip, track}` objects. Each
clip ref must be unique and parent-scoped; each destination track ref is explicit
and parent-scoped. IDs cannot contain `/` or `::`. Anchor must equal one member's
clip ref. `on` is a finite nonnegative number in absolute timeline seconds; zero
is supported. Null, boolean, nonfinite, relative, implicit-track and mixed-owner
forms refuse. Arg membership and order are retained byte-for-byte in accepted
commands. `resolved` is the clip-ref vector in exactly that argument order.

Effective intent is exactly
`{"ripple":"none","anchor":"fixed","position":"absolute"}`. Omission or a
matching subset is accepted and normalized to this value. Unknown intentions,
shared/occurrence ownership, follow, trim and ripple overrides refuse. Ordinary
EditCommand metadata (`group_id`, `rationale`) and verified recorder claims use
the existing envelope. No new command, history or Runtime DTO fields.

## Capture and track creation

Python builder:
`astrid.sdk.timeline._move_set.capture_move_set(bundle, members, anchor, on)`.
It uses authoritative `commands.execute` and returns the sealed captured command;
no frontend read-footprint table. Capture from an immutable pointerdown bundle.
For a new track, allocate its ID once, capture the existing `track.create` on that
basis, execute that exact command on a detached copy, and capture the move-set on
that staged copy. Submit BOTH sealed commands in the SAME commit, with the same
`group_id`. Do not refresh source claims from a later ACK or preview-mutated view.
A new target track is never created implicitly by move-set and allocates no IDs.

Exact original App example batch before adding recorder claims:

```json
[
  {"schema_version":1,"op":"track.create","version":"1","select":"parent",
   "args":{"row":{"id":"V3","kind":"visual"}},"intent":{},"group_id":"free-drag-1"},
  {"schema_version":1,"op":"clip.move-set","version":"1","select":"parent",
   "args":{"members":[{"clip":"parent/clip:clip-2","track":"parent/track:V3"},
                      {"clip":"parent/clip:clip-1","track":"parent/track:V2"}],
           "anchor":"parent/clip:clip-2","on":3},
   "intent":{"ripple":"none","anchor":"fixed","position":"absolute"},"group_id":"free-drag-1"}
]
```

The portable golden is the exact machine-readable capture, not this abbreviated
example. It contains input CanonicalDocument, both complete sealed commands,
authoritative records and output CanonicalDocument:

`/home/user/work/wt/agt-m2-free-move-set/tests/editing_conformance/fixtures/recipe_m2_free_move_set.json`

Its permanent check is
`tests/editing_conformance/test_recipe_free_move_set.py::test_exact_app_drag_golden_selection_order_and_created_track_are_one_unit`.
`portable_golden()` in the same module reconstructs it through native execution.
The file lives at the same repository-relative path after integration; it is not
a Runtime generated artifact. No opaque process token or WeakMap state is needed.

## Exact observation and write rules

All observations precede move-set writes. Recorder claims are generated and
verified through existing primitives, with exact ordered JSON in the golden:

- `selection.clips`, query version 1, owner `parent`: intersection of the explicit
  stable member identities with the authored parent clip array, in authored array
  order. It detects missing/duplicate identities and relative authored-order
  changes. This authored-order proof is distinct from the retained UI selection
  order in `args.members` / `resolved`; no sorting of either vector occurs.
- `lane.members`, query version 1, owner the explicit destination track ref:
  complete parent clip refs in authored order whose raw `track` equals the lane,
  followed by canonical occurrence refs on that lane in placement-array order.
  Inactive rows are included, so their activity is a guarded read rather than an
  unobserved exclusion. All selections have `members == order == boundaries` and
  `policy: "guard-membership"`. Empty lane results are recorded. Query inputs use
  existing owner/members carriers, with no added context field.
- Every moved member reuses M1 `CLIP_FIELDS`, source registry fields, intent
  containers and `RELATIONS` capture through `capture.clip_inputs`. In addition,
  all `RELATIONS`, `anchor`, `standin`, `standin_intent` paths on the raw row and
  both app scopes are read to refuse follows. Present `for` must be a positive
  finite number; present `fixed_start` must be true. Source registry dependencies retain
  M1's exact consumed source tuple; opaque fields are preserved without broad
  whole-row reads. Duration and start codecs use M1's shared primitives.
- Source and destination track predicates are exactly `id`, `kind`, `role`,
  `enabled`, `active`, `disabled`, `hidden`, `deleted`. Both lanes must be active,
  compatible `visual` or `audio` output tracks. Absent role means output; explicit
  null/source roles refuse. Source track refs are fixed `move.member:i.track`
  bindings; destination refs are fixed `move.destination:i` bindings. Members are
  fixed `move.member:i` bindings. Source dependencies are `move.member:i.source`.
- Parent `config.output.fps` and tagged `config.pinnedShotGroups` are read. Fps
  retains M1's rational/default admission. Absent/null/empty legacy-group input is
  permitted; populated or malformed input refuses. Dependency `move.quantization`
  retains the rational rate and half-toward-positive-infinity rule; `move.images`
  retains M1's source-image provenance. Compile-input DocumentPins use the existing
  retained-input seam unchanged.
- Every active unselected parent clip on a destination lane gets the same timing,
  source and free-shape capture, bound as `move.blocker:<full ref>`. Inactive rows
  get `CLIP_FIELDS` reads and do not block. An occurrence on a destination lane is
  an explicit unsupported-shape refusal in this bounded slice, even if distant;
  occurrence placement and group movement belong to the other worker.
- `track.create` keeps its existing complete track-order query, absent-root read,
  full row write and created-ID record. Move-set creates nothing. Rebase/inverse
  check query predicates through the shared collection overlap layer, including
  root and property writes entering/leaving a lane and membership ABA. Opaque or
  timing edits to excluded rows on disjoint lanes remain independent. Whole
  collection replacements conservatively conflict; this slice does not merge
  arbitrary array replacement writes.

Compute `Q(on) = floor(on * fps + 0.5) / fps` through M1's quantization helper.
The one delta is `Q(on) - original_anchor_start`; apply it to each original start.
Individual members are NOT independently rounded. Preserve all source windows,
source-unit holds, speed, relative offsets, opaque JSON and authored array order.
Compute all candidate intervals before any writes. Moving members' old locations
are excluded from blockers. Intervals are half-open: exact contact passes, actual
intersection refuses. New overlap between members originally on different lanes
refuses; translation may preserve existing same-lane internal overlap. Negative
candidate starts refuse. No shorten/clamp/trim behavior.

Writes reuse M1 `write_move`: preserve the admitted at/at_ms spelling (write both
when both were present), create app containers with tagged presence when needed,
clear `on`, `until`, `until_film_end` in both supported app scopes, set
`app.astrid.fixed_start = true` and `app.astrid.for = timeline_duration`, then write
each member's raw `track` ID. Record unchanged assignments and clears. Source
windows, holds and all unrelated properties survive. Mirrors remain derived.
Original follow/map/child/group shapes are refused before any writes; the command
does not detach a group or convert a follow into fixed timing.

## Outcome and history

The golden starts with V1/V2, clip-1 V1@0 hold2 and clip-2 V2@2 hold2. It ends with
V1/V2/V3, clip-1 V2@1 hold2 and clip-2 V3@3 hold2. Selection remains
`[clip-2, clip-1]`; there is no pinned group. App can derive its existing read-side
preview shape, but only the captured EditCommands are persisted.

Undo/redo use the existing staged guarded inverse with no per-operation inverse.
Own moves reverse before deleting the batch-created track. Surviving dependents,
intervening writes including equal-state ABA, changed sources/lanes/order and
occupied created IDs refuse atomically. Redo restores the same V3 identity.
The normal accepted-history reservation mechanism remains unchanged. Detached
unit conformance proves these behaviors; real Runtime acceptance, lost-ACK
restart, official artifacts and the three preserved App tests remain integration
work, not claims of this candidate.

# M2 free multi-clip move: Runtime proof

Status: reviewed Agent/runtime acceptance proof; App TypeScript integration remains out of scope for this change.

The real-daemon acceptance test is [test_commit_runtime_free_move_set.py](../../tests/editing_conformance/test_commit_runtime_free_move_set.py). It seeds a normal authenticated Runtime project through registered `track.create` and `clip.add` commands, then proves the reviewed App geometry:

- `V1`, `V2`, `V3`; `clip-1` -> `V2 @ 1`, hold `2`; `clip-2` -> `V3 @ 3`, hold `2`;
- ordered selection `clip-2`, `clip-1`, with no `pinnedShotGroups`;
- `track.create(V3)` plus the sealed `clip.move-set` in one `/v1` publication;
- exact canonical reload, accepted history command captures, and opaque clip/app fields;
- durable lost-ACK retry after Runtime restart with the same request body, idempotency key, and receipt;
- guarded undo (moves restored before the created track is removed), redo with the same authored IDs, and refusal when a later clip depends on `V3`;
- disjoint-lane server rebase, and refusal after relevant lane-entry membership changes A -> B -> A.

This is evidence for the Python/Runtime command contract only. It does not claim an official generated TypeScript consumer or App artifact: the App-side gesture producer, generated-client consumption, and shipped artifact scope still require their own integration proof.
