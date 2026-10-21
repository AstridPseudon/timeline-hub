# RT03 raw capture peer shape

Status: source-only Runtime proposal, pending exact Agent shape ACK. This
document does not change the Runtime source, public contract, generated
clients, schema, tables, tests, or integration state.

## Decision and boundary

The smallest Runtime addition is one internal, request-scoped raw-media
capture on the existing `RuntimeCommitPort`. It is separate from the existing
base-only `media_info`; that method and its base-closure restriction remain
unchanged. It is also separate from `selected_media`: `VerifiedMedia` is the
five-field managed selection result and cannot be the raw-reference carrier.

The proposed private method is:

```python
raw_media_info(pin: dto.MediaManifestEntry) -> MediaInfo
```

where the existing pin is exactly:

```json
{"media_id": "sha256:<64 lowercase hex>",
 "content_digest": "sha256:<same digest>"}
```

and the existing private `MediaInfo` result is exactly the descriptor shape
already used by the reviewed raw-media seam: `object_id`, `media_type`, and
`size`, with only the existing optional intrinsic fields (`duration_seconds`,
`width`, `height`). It is not a new DTO and is not exposed through HTTP or a
generated client. The source shape is recorded by `runtime_protocol/timeline_commit.py`
and the reviewed `MediaReads.media_info` implementation in the private
raw-media seam (`dcac221`/`b731391`); `runtime_protocol/timeline_commit_types.py:78-99`
confirms the two-field `MediaManifestEntry` and the distinct `VerifiedMedia`.

## Capture and acceptance rules

`RequestCommitPort.raw_media_info` is optional at runtime for compatibility
with an older provider. The Agent command must call it only when the exact pin
is present in the explicitly declared command object (`RequestCommitPort`'s
`__declared`, populated from `request["commands"]`); a pin appearing only in a
candidate manifest is not declared. If the method is absent or not callable,
the command fails closed with the existing dependency-unavailable refusal. No
fallback to `media_info`, `selected_media`, a public object API, a catalog
lookup, or caller-supplied metadata is allowed.

The read is narrowly scoped to the authenticated request project and one
pin. It must, while holding the existing Runtime mutex:

1. require the exact two-key canonical pin and no inline authority beyond its
   digest;
2. require an `objects` row joined to this project's
   `project_objects(relation='managed')` row;
3. read the object through one opened CAS descriptor, verifying regular-file
   identity, size, and SHA-256 with the existing descriptor verifier, and
   return the stored MIME plus size in `MediaInfo`; and
4. memoize that descriptor result in this request only.

If the project association, object row, CAS file, size, digest, or descriptor
metadata is missing or disagrees, refuse. Optional WAV/intrinsic parsing may
reuse the existing result fields only if the same descriptor is rechecked
after parsing; reopening the path is not a second authority.

`RequestCommitPort.validate` must re-run the same scoped raw read for every
captured pin inside `TimelineCommitStore.accept`'s existing transaction, before
`_persist_closure` and any projection write (`runtime_protocol/timeline_commit_store.py:712-741`).
The captured pin/result must be unchanged, and the exact pin must be present in
the candidate dependency manifest. Only then may the existing closure gate
(`timeline_commit_store.py:437-547`) authorize the raw registry birth. A raw
pin captured by this method may be added to the port's authorized media set;
unrelated manifest media remains refused. `_persist_closure` remains the
registry/parent storage seam; it does not gain a new store or CAS reader.

## Agent/Runtime split and proof

Agent owns the one closed `timeline.reference` recipe, exact asset birth and
reference leaf, absent-destination guard, and recorded exact media dependency.
Runtime owns only the scoped raw read/recheck and the existing projection to
`timeline_references` plus `timeline_revisions.references_json`; those rows
remain project/timeline scoped (`canonical_schema.py:135-176`,
`timeline_catalog.py:12-25`). No occurrence, shot, clip, placement, catalog
role, managed-generation tuple, or raw-trim guard is introduced or weakened.

The peer pair may implement only after Agent ACKs this carrier shape in the
shared design and hub. The acceptance witness must retain the original strict
positive and additionally prove: owned raw object from an empty parent
succeeds with no placement; unowned and missing objects refuse; the exact
same-key retry survives restart; changed payload and occupied `reference_id`
refuse without writes; and no shot/occurrence/clip/pixels are added. The
original strict positive is never rewritten as a refusal or weakened.
