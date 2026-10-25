# D134 managed-edge cluster A setup proof

## Result

UNAPPLIED. The source remains byte-identical because no existing registered semantic caller can reproduce the declared complete child closure from the empty timeline.

## Reproduction

The fixture authorizes a semantic `occurrence.create`, accepts that birth, and then restores the declared internal, shot, and parent payloads. The first current refusal is the shot root patch: the semantic birth has `items: []`, while the declared authored shot contains `item-1`. Retaining `internal_timeline_revision_id` from the semantic birth removes only the managed-edge refusal, but the state recorder then rejects the item-set change as `shot item correspondence changed`.

The parent occurrence replacement is also a managed-edge setup mutation. Its authored row includes the provider-owned occurrence/shot revision topology and cannot be installed as a generic closure replacement.

## Existing caller boundary

`occurrence.create` creates an empty child closure. `occurrence.add-media` can create an occurrence-owned raw clip and asset binding, but it does not create the shot item correspondence required by the declared payload. `occurrence.duplicate` and `occurrence.fork` require an existing authenticated source occurrence. `occurrence.place-shared` requires an existing authenticated local source or a foreign source reference. `timeline.duplicate` requires an authenticated foreign source closure. None is available in this empty bootstrap without trusted seeding or a new API.

Dropping `item-1`, opaque fields, or any managed link would change authored input/topology and is expressly disallowed. No seed, fabricated accepted record, mapping repair, guard change, or new API was used.
