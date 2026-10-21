# RT03 Agent recipe / Runtime projection fit

Status: **one exact Runtime incompatibility found; Agent source ACKed, Runtime
projection remains the smallest implementation prerequisite** (2026-10-21).

This document supersedes runtime-rt03-original-native-proof-plan.md as the
source-review prerequisite. That older plan predates the Agent handoff and is
not a blocker for reviewing the actual Agent source. The original strict
owned positive remains unchanged and unqualified until the paired acceptance
probe is implemented and run.

## Verdict

The Agent recipe is compatible with the approved f53 raw-media carrier and is
the sole semantic recorder for the authored reference and asset births. There
is one exact incompatibility in Runtime f53:

> Runtime accepts and persists the canonical parent payload, but does not
> project parent_revision.payload.config.app.astrid.timeline_references into
> the existing timeline_references table or its
> timeline_revisions.references_json snapshot.

Therefore the accepted Agent reference is durable in the canonical parent
closure but invisible through Runtime's existing timeline-reference read
model. The existing placed-occurrence provenance projector cannot satisfy
this case: this command is parent-scoped and deliberately has no occurrence,
shot, clip, track, placement, catalog row, generation, or managed selection.

## Reciprocal source review

Reviewed the exact Agent commit/tree d1f5f7824a5ede5587088735fad6e6870f0b95db /
ca825c4bf900400487f9a1ca6b8c1651d63d5a68 against Runtime f53
f53bf588bf70b090ce8e0bed5ccb7d91157771b6.

Agent astrid/sdk/timeline/native_parent_reference_commands.py:

- validates select == "parent", role source, and exactly
  {media_id, content_digest} with equal lowercase SHA-256 digests;
- calls the already-captured Runtime result through _raw_verified, requiring
  media_info.object_id == pin.media_id and valid MIME/positive size;
- reads the parent asset collection, parent/asset:<reference_id>, and the
  namespaced reference leaf before writing;
- records one existing parent asset birth with the exact pin, writes only
  config.app.astrid.timeline_references[reference_id], records
  dependency("reference.media", "media", pin), and binds the owner to
  parent; and
- leaves placement and occurrence state empty. Its recorded writes/reads,
  created identity, dependency, and owner binding are the inputs to existing
  rebase and guarded inverse machinery.

The Agent provider (astrid/sdk/timeline/commit.py) validates the command,
calls port.raw_media_info for the exact declared args.media pin, and passes
only the private result as verified_media into semantic execution.
document_from_bundle then carries the authored parent config/registry and the
same media pin into the normal canonical_document; it does not create a
second reference authority.

Runtime f53 has the matching custody boundary:

- RequestCommitPort.raw_media_info requires an exact declared
  MediaManifestEntry, same-project managed ownership, and the private
  request memo;
- RequestCommitPort.validate requires the captured pin in the candidate
  dependency manifest, re-reads the raw descriptor, checks object identity,
  and adds only that captured object to the authorized-media set; and
- _validate_closure verifies every manifest media pin against managed project
  custody and CAS bytes before persistence.

Those paths are source-compatible. The missing behavior is after that
validation: TimelineCommitStore.accept calls _persist_closure, _publish, and
the text-binding projector. _persist_closure stores the parent payload,
occurrences, and dependency rows, but has no parent-reference projector.
timeline_catalog.timeline_resource still reads timeline_references, and
verify_catalog_tail compares that live resource with the latest
timeline_revisions.references_json; neither table is populated from the
accepted parent config.

## Exact normal accepted-closure carrier

The only carrier for this unplaced operation is:

prepared["canonical_document"]
  ["parent_revision"]["payload"]
  ["config"]["app"]["astrid"]["timeline_references"]
  [reference_id]

The leaf has the exact authored shape:

{
  "version": 1,
  "reference_id": "<reference_id>",
  "role": "source",
  "media": {
    "media_id": "sha256:<64 lowercase hex>",
    "content_digest": "sha256:<same digest>"
  }
}

The parent registry birth is retained in the same canonical payload, at the
existing effective parent registry path (parent.registry.assets or
parent.config.registry.assets according to the Agent's existing registry
shape). It is an authored identity/undo guard, not a replacement source for
the reference projection. The projection must take object_id from the leaf's
exact media.media_id, after the normal manifest/custody checks; it must not
resolve a catalog, invent an alias, or call selected_media.

## Smallest required Runtime result

Add one acceptance-transaction helper owned by Runtime, invoked for the
accepted canonical parent document and its immediately previous accepted
closure. It should:

1. validate the closed v1 leaf shape and require its media pin in the
   accepted dependency_manifest.media (the existing closure/raw custody
   checks remain authoritative);
2. derive deterministic legacy rows
   {reference_id, object_id: media.media_id, role: "source"} from the
   namespaced map, sorted by reference_id;
3. project those rows into timeline_references for the authenticated
   project/timeline, preserving unrelated legacy rows and refusing a global
   id already occupied by another timeline or by a non-matching source;
4. update the corresponding timeline_revisions.references_json snapshot in
   the same acceptance transaction, alongside the resulting existing legacy
   shots projection and new timeline version; and
5. use the previous accepted parent carrier to identify removals. Delete a
   live row only when it is the exact prior projection of this carrier;
   otherwise refuse rather than deleting or overwriting an unrelated row.

This is a derived SQL read-model projection only. It must not write the Agent
config leaf, parent registry, dependency manifest, or any new table/DTO/
endpoint. It must not use occurrence provenance as a fallback.

## Data-safety consequences

| Case | Required result |
| --- | --- |
| Exact managed raw object | Existing f53 raw capture and acceptance-time recheck pass; projection occurs only after closure validation and before transaction commit. |
| Missing, foreign, unowned, malformed, or changed raw object | Existing raw_media_info/manifest checks refuse before persistence; no parent revision, legacy row, snapshot, head, or receipt write. |
| Occupied reference_id | Refuse before any projection write unless the row is the exact projection of the immediately previous accepted carrier. Never overwrite a row from another timeline or an unrelated legacy writer, even when bytes happen to match. |
| Exact retry after restart | Ledger lookup remains first. It returns the original receipt without provider execution, raw reread, or a second projection. Durable row and snapshot must already match the accepted carrier. |
| Guarded inverse | Agent's existing inverse removes/restores the authored leaf and parent asset birth. Runtime projects the resulting accepted carrier; it removes only its exact prior derived row and refuses on an intervening/unrelated occupant. |
| Rebase / concurrent edit | Agent read/identity/order guards remain authoritative. Runtime must project only the accepted result in the same transaction and preserve unrelated reference IDs. |

The original strict positive and the unowned refusal remain as-is. No old
6ba validator, catalog-only observation, or occurrence-provenance result can
qualify this new operation.

## Next qualification result

The next implementation worker should add the minimal Runtime projector and
one paired normal commit-path test covering: empty parent -> one reference
row/snapshot, managed custody, occupied refusal with unchanged DB/head, exact
retry after close/reopen, and inverse removal/restoration. Keep the existing
strict owned positive and unowned refusal expectations unchanged. No schema
generation, endpoint/client change, pin/adoption, placement, generation,
catalog-authority, or managed-five-field selection is part of this prerequisite.

## Evidence and limits

Source review commands used:

git -C /home/user/peteromallet/astrid-agent show d1f5f7824a5ede5587088735fad6e6870f0b95db:astrid/sdk/timeline/native_parent_reference_commands.py
git -C /home/user/peteromallet/astrid-agent show d1f5f7824a5ede5587088735fad6e6870f0b95db:astrid/sdk/timeline/commit.py
rg -n 'timeline_references|references_json|_persist_closure|raw_media_info' runtime_protocol tests

No unchanged Agent 67+6 run, full/socket/browser suite, schema generation,
pin, or adoption was run. No Runtime code was changed in this review.
