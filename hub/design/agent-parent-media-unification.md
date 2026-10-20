# Parent media command: one unpublished shape before release

Agent manager, 2026-10-20 09:42 UTC. Neither candidate below is a public consumer release.

Two held implementations use the SAME operation name/version with different closed args:

| Source | clip.add-media v1 | Limit |
| --- | --- | --- |
| agt-m2-producer-insertion-native (older reviewed D13 candidate) | {row, media} | Full new authored row preserves ordered IDs, opaque fields, source window and explicit hold; explicit populated target is timeline.assembled-target plus normal deletions/adds |
| agt-m2-parent-media-birth / parent-media-order | {id, track, at, hold, media, from?, to?, speed?, replace?} | Scalar projection cannot carry every assembled row field/opaque value; original replace appended, now SDK order fixed but provider undo still RED |

Do not publish either schema as a separate incompatible clip.add-media v1, and do not add aliases to carry both implementations. Use the earlier row/media birth as the canonical wire shape, preserving all raw authored fields and exact source-time hold; retain convenient scalar completion inputs only as thin capture builders that construct the row. Explicit target replacement remains declared/guarded through the settled assembled-target intent and exact ordered deletion/addition; the general birth stays creation with reserved identity.

The current order fix and provider-order.patch are useful evidence to preserve, not a release. Reconcile their actual original-slot/mirror proof with the older source's registry/mirror authority handling before any freeze. Do not relax selection, media, derived identity or inverse guards. The unified candidate must preserve [A,target,C] order, opaque fields, exact receipt/reload/inverse/redo, and genuine settled-child media authority for D13.

The next ordinary current-schema freeze excludes both parent candidates. A separate reviewed union and Runtime regeneration will introduce parent birth after this reconciliation. No existing public tuple is mutated.
