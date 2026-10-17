# Overhang to last-frame hold

`clip.overhang-to-hold` is one atomic OpCall on the existing SDK command,
compiler, semantic commit and publication-inverse path. It implements the W44
video-editor conversion; App adoption belongs to the consumer. It does not
introduce a save endpoint, selection store or history owner.

Select an exact `parent/clip:<id>` or `occurrence:<id>/clip:<id>`. Arguments:

| Argument | Captured intent |
| --- | --- |
| `child` | Exactly one caller-allocated clip ScopedId in the source owner. `created`, if supplied, must be exactly `[child]`. |
| `source_duration` | Positive finite duration from the selected asset registry entry. |
| `frame_rate` | That entry's FPS; absent, null or invalid values use 30, as in the caller. A valid conflicting FPS is refused. |
| `out_s` | The caller's clamped source out point. |
| `kind` | Explicitly `"hold"`. |
| `hold_from`, `hold_to` | `[max(0, source_duration - 1 / safe_fps), source_duration]`. |
| `hold_duration` | The original timeline duration minus the playable timeline duration. Must exceed the caller's 0.0001-second epsilon. |
| `relation_choices` | Existing explicit start/end/sequence choices for every affected authored relation, when any exist. |
| `group_choices` | For every affected pinned group, `{group: <semantic group identity>, choice: "keep"}` in captured group order. Group membership and snapshots stay intact. |
| `relation_inventory` | Required captured `{authored, groups, beds}`; use empty collections when none exist and preserve it unchanged on replay. |

The caller must supply tagged expectations under `expect` for the complete
source (`<source>::`), complete owner clip permutation
(`<source>::clip_order`), source track (`<scope>/track:<track>::`), and selected
asset entry. The asset path is `parent::registry.assets["<asset>"]` for parent
clips and `occurrence:<id>/registry::assets["<asset>"]` for occurrence clips.
Occurrence inputs also require complete expectations for `occurrence:<id>::`,
`occurrence:<id>/shot::` and `occurrence:<id>/source::` (the pinned source tuple).
Every affected relation target also requires its complete tagged source expectation.
Use the same tagged present/absent states as all other OpCalls. Replay retains
these expectations, the complete relation inventory and the child identity;
it never recaptures a new base to repair a conflict.

Playable duration is `max(0.05, max(0, source_duration - from) / speed)`.
The producer validates every supplied derived value against the captured source.
The caller's 0.05-second minimum can place the clamped out point beyond an
extremely short remaining source interval; this is deliberate caller parity.
An existing media `hold` is updated in SDK source-second units so it cannot
mask the clamp. The source's other fields remain intact.

The new child starts at the source's new end. It has the same asset and track,
`clipType: "hold"`, explicit last-frame `from`/`to`, timeline `hold`, speed 1
and volume 0. It retains `opacity`, `x`, `y`, `width`, `height`, `cropTop`,
`cropBottom`, `cropLeft` and `cropRight`, including null/absence. It does not
inherit unrelated source app metadata, anchors or animation declarations.
The canonical owner clip array inserts it immediately after the source;
App derives both action order and `clipOrder` from that array. The returned
created identity is the consumer's selection target.
It appears in `change.commands[*].created`; unchanged identities need not have
an `id_map` entry.

Source formulas/loops/orphan timing and a source owned by a music-bed projection
are refused rather than creating a competing timing/projection owner. Dependent
bed and sequence relations use the existing explicit relation-choice machinery.
Choices that contradict the requested clamp/hold geometry refuse the complete
transaction. Existing pinned snapshot identity reservations also apply.

The real Plan/CommitResult contains source `to` (and changed media `hold` or
authored duration), the complete absent-to-present child root, and any explicit
relation writes. Detaching a start or sequence also directly authors the frozen
absolute start, so its inverse retains the original clock literal even when
numeric equality hides a change such as `7` to `7.0`.
Aggregate storage arrays remain consequences. Ordinary
`timeline.inverse` owns Undo/Redo and guards later edits to the child. The
focused SDK tests cover synthetic acceptance, saved publication retry/reload,
exact content Undo/Redo and atomic refusals. They do not establish mounted
App, Host, installed Runtime or release acceptance.

The inverse recorder preserves `timeline.inverse.writes` as literal JSON,
including integral floats, negative zero, opaque nested values and tagged
absence/null states. Strict serialized witnesses compare the complete detached
document and the publication's authored content on Undo/Redo and replay. This
does not preserve arbitrary input-file whitespace or key ordering, which are
not part of the document model. Ordinary command numeric arguments still use
the existing canonical normalization; operation and idempotency digest
functions retain their existing encoding and identity rules.
