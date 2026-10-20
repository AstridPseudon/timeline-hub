# occurrence.delete v1 — candidate source contract (HELD)

Owner: agt-m2-occurrence-delete; base a31d712d4a5c9ad08f385e12d71d3f1f7cbfef83.
This is a LATER group artifact candidate, never a change to the frozen Bundle 2
release/ref. Normal Runtime schema generation and consumer pins remain required.
M2 integration remains held until PLAN records M1.

Closed call: `{schema_version:1, op:"occurrence.delete", version:"1",
select:"occurrence:<explicit raw occurrence id>", args:{},
intent:{ownership:"occurrence"}}`.
Python export will be `astrid.sdk.timeline.native_occurrence_delete.capture_occurrence_delete(bundle, owner)`.
Portable golden will be `tests/editing_conformance/fixtures/recipe_m2_occurrence_delete.json`
on this worker branch. Capture uses native execute; no handwritten claims.

The target is ONE canonical placement, including all its projected children.
Never infer from a display ID or (shotId, trackId). Legacy pinnedShotGroups
requires recorded lossless migration first (migration_needed). App's original
useClipEditing.test.ts shot-menu positive keeps both metaDeletes and the empty
V1 action row: migrate its two children into one occurrence, then delete that
occurrence. The empty parent lane and assets remain. App's compatibility group
view is read-only and derived from canonical occurrence/migration bindings.

Record the complete target placement, exact source identity and authored shot
content, child membership/order and explicit ownership. Remove only the
occurrence root. Do not delete shots, children, registry/media/history or physical
rows. Existing compiled closure selection drops unreachable immutable images;
accepted history remains the authority for guarded inverse and original order.
No whole-parent write or parent-occurrence-array membership guard is permitted.
Other occurrences/groups can edit independently. Changed target children/source,
same-ID replacement and equal-value/ABA publications must refuse via native
reads/selections and intervening history. IDs remain reserved through the existing
provider history scan; undo recreates only authenticated original IDs.

Implementation investigation: existing root remove works, but root inverse lacks
historical occurrence ordering and exact source recovery after the last consumer
is absent from accepted closure. A minimal generic inverse correction is needed;
no media pruning or parent replacement will be introduced. Exact goldens and
final source/schema digests will be appended after executable validation.

Coordination for agt-m2-group-official-root-proof: no edits to your WIP; independent
source/schema deltas on the same base. Compose registry imports and schema allOf
entries additively in the LATER group bundle, preserving existing definitions and
M1/label goldens. Please retain original migration provenance on the occurrence;
this delete restores the complete occurrence verbatim.
