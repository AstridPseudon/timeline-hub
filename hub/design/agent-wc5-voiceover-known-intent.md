# Agent WC5: known draft voiceover intent

The Agent branch `tl/agt-m2-wc5-voiceover-known-intent` migrates only the
new-child insertion branch of `draft_voiceover` to the settled producer
proposal/requester path. It captures the existing native commands in this
order when an occurrence has no audio lane:

1. `track.create` in `occurrence:<id>` scope, when needed;
2. `occurrence.add-media` with the exact `{asset,generation_id,variant_id,object_id,catalog_digest}` selection and raw managed WAV metadata;
3. `text-binding.set` only for a registered, frozen UTF-8 `voiceover_script` binding that passes the normal capture guards.

The proposal uses the existing closed shape (`schema_version`, producer pin,
admitted revision/publication pair, commands, rationale, and digest), then
queues it through `TimelineSession`'s durable outbox. The requester does not
receive renderer credentials or publish a candidate bundle. Missing tuple,
producer, WAV metadata, scope, or text evidence returns `proposal_open` with a
concrete gap.

The known proposal also refuses `ripple` timing: placement/parent retiming has
no native command in this branch, so it is surfaced as a concrete gap rather
than omitted from or compiled into a whole-candidate diff.

The existing-clip regeneration branch remains on `TargetBound.publish`; this
is deliberate because WC5 retires the old writer only for the proven branch.
`TargetBound.publish` and its deletion-ledger row remain visibly held. No
ledger row was marked deleted.

Evidence is in the targeted voiceover and native-command tests, including
command ordering, exact media selection/raw metadata, producer pin, proposal
shape, missing selection/media type, and negative text provenance/mime guards.
