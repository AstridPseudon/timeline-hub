# Agent WC1/AG01 known-proposal caller frontier

The live carrier is the explicit-selection branch of
`RemoteTimelines.replace_parent_media`.

It already retains the exact five-key old/new `MediaSelection`, the exact
parent/occurrence clip target, and the expected publication/head pair. The
branch now captures the existing native `clip.swap-media` or
`occurrence.swap-media` command through `TimelineSession`, preserving the
existing verified-media, mapping, and grammar checks and the durable pending
flight retry contract. Retry matching is exact and a persisted flight keeps
its original idempotency key.

The digest-only branch is bounded NO-CARRIER: it has only a source object
digest, target locator, and expected head. It does not retain an immutable
selection, publication identity, or native proposal. Resolving a variant and
reusing its identifier as an asset alias would fabricate identity, so that
branch remains on its original exact-closure publication path. The minimum
existing seam for a future migration is the complete old/new selection pair
plus expected publication and target values, already present in the explicit
branch.
