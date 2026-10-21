# Runtime bounded carrier review — original three drag records

Date: 2026-10-21 UTC

## Verdict

**ACK generic carrier fit, bounded to the exact private Agent source contract.**
No concrete record-field mismatch was found for the three requested vectors.
This is not a Runtime generation, public-schema, native/provider, App, browser,
socket, pin, freeze, activation, or acceptance approval.

The reviewed Agent source is commit
`5672d2b7deee2bfe2ab375fd6db5fc35a192591d`, tree
`6dd13b552c4f07fff5586b1fa772bdbdf64accba`.

- Agent raw schema SHA-256: `daec2964bb589d2087409446f99b84cfe9d6fb62b0b3af25e37363a78b170514`.
- Agent private schema: **62 definitions / 36 unique closed operation clauses**.
- Current Runtime `b92d3e7a05eec65c142294ef4873edd059e9b31d` carries the ordinary
  `edit-command` resource at **55 definitions / 29 operation clauses**.
- The published Runtime95 / ordinary Agent6ba tuple therefore does **not**
  admit these group/multi operations and is not acceptance authority.

## Exact record vectors

The source records use the existing generic `CommandRecord` envelope:
`ordinal`, `command`, `writes`, `reads`, `selections`, `bindings`, `created`,
`dependencies`, and `derived_writes`. The command envelope carries the generic
`schema_version`, `op`, `version`, `select`, JSON `args`, `resolved`, `expect`,
`bindings`, `created`, `reads`, `selections`, `intent`, `authorship`, and
`group_id` fields. The generic DTOs permit every field used below.

1. **Guarded legacy migration** — `timeline.migrate-groups@1`, `select:
   parent`.

   - Typed births are `shot:new-shot` with `kind: shot, owner: null` and
     `occurrence:new-occ` with `kind: occurrence, owner: parent`.
   - `migration.groups` and collection selections preserve member/order claims;
     bindings preserve each legacy member and destination plus typed shot/group
     roots.
   - Reads/writes carry the legacy `pinnedShotGroups` source, root payloads,
     consumed member refs, and the mirrored `config.clips` derived write.
   - Document/media source pins are `AgentDependency` entries (`transcript` /
     `media`, exact policy); their pin payload is opaque JSON to the carrier.
   - Batch `id_map` is `{}`: these are explicit typed root births, not a
     materialization identity-map allocation.

2. **Parent-track birth plus grouped occurrence move** —
   `[track.create(parent/track:V3), occurrence.move]` with one shared
   `group_id` when grouped.

   - Record 0 has typed `created: [{ref: parent/track:V3, kind: track,
     owner: parent}]`, an ordered `track.create` selection, and the absent
     identity read plus root write.
   - Record 1 has no created IDs. `placement.owners`, `collection.clips`, and
     destination `lane.members` preserve membership/order. Fixed bindings carry
     the occurrence owner, destination parent track, raw child track, every
     child member, and every raw-track identity.
   - Writes carry occurrence start/timing and parent/child lane changes. The
     exact source pin is the `move.images` entity dependency containing the
     parent/source identities; rational timing is the existing exact
     `move.quantization` dependency where present.
   - Batch `id_map` is `{}`.

3. **Parent-track birth plus grouped parent `clip.move-set`** —
   `[track.create(parent/track:V3), clip.move-set]` with shared `group_id`.

   - Record 0 is the same typed parent track birth above.
   - Record 1 preserves explicit authored member order separately from resolved
     selection order, with `selection.clips` and destination `lane.members`
     selections. Fixed bindings carry each member, source/owner, and each
     destination track.
   - `writes` carry the timing, track, and intent-container updates; the
     mirrored parent/config clip update is represented as `derived_writes` with
     its integer `cause`. `move.quantization` and exact `move.images` source
     dependencies are generic dependency records, not new DTO fields.
   - Batch `id_map` is `{}`.

The exact-record probe generated all three batches from the reviewed source and
confirmed only the generic envelope fields above were used. Created owners
accept `null` or scoped strings; refs, member/order arrays, source/timing pins,
tagged before/after states, and the `id_map` string-to-string map all fit the
existing DTO/schema shapes. The private Agent source operation conditionals are
the only absent part of the current ordinary Runtime resource.

## Required private Runtime boundary

This ACK does not make the current Runtime admit the records. The group
typed-root/slot-ownership dependency is the reviewed RT08 private
materialization join, not the RT03 raw-reference work. The exact helper/seam is
`materialization_join(...)` in `runtime_protocol/timeline_materialization.py`
(the read-only source/owner/closure/item-map provenance join) together with
`_same_materialization_slot(...)` in `runtime_protocol/timeline_commit_store.py`
(the source edge, owner, output, and item-membership slot check). The reviewed
compatible private source is the C3d fixed-84fc counterpart, Runtime
`c3d26567ff6fe4e20a959476d40aff90ad23a0ca` (tree
`f3ae49d38454ce73a9c91a954bb530b3ce51c122`), with the RT08 private join carried
forward in Runtime `f8da4b6d46b0ec5ebeb7a42be47c5bf3438c5414` (tree
`8be43e13acb436120f8a63b1a178d64c49422461`). This is a source/review
reference only; it does not authorize a new source approval, generation, pin,
or native acceptance boundary.

The `f53bf588bf70b090ce8e0bed5ccb7d91157771b6` `raw_media_info` seam and
`449d13d291cc3b62ebbdd780d38d8c58732e4e1b` unplaced-reference projection are
different RT03 features. They are not dependencies of these group-drag
records. The current published Runtime95 / ordinary Agent6ba resource still
lacks the group/multi operation clauses; future full matched generation and
native qualification remain separate.

## Callers and limits

Relevant live callers: **NONE**. Outside the source operation registry and
capture implementations, the repository has no production caller for these
three records; the only other references are tests/docs and the explicit legacy
admission guard. The current published ordinary schema remains unchanged.

No product/tests were changed. No broad cohort, native group run, full,
socket/browser/render/generation/pin/schema/freeze/activation run was performed.
The source handoff's existing conformance evidence remains the behavior proof;
this review is only the bounded carrier verdict.
