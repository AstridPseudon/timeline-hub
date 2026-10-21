# Agent WC1/AG01 known-proposal caller frontier

Current status (2026-10-21): OPEN. Source `255192793` and merged fix
`566307478` restore the existing TimelineSession/Outbox seam for the explicit
parent and occurrence media-swap branch. Direct checks passed: 8 in
`tests/test_timeline_clip_replacement.py` and 97 in
`tests/sdk/test_timeline_sync.py tests/sdk/test_timeline_sync_native.py`;
independent data-safety review `agt-review-wc1-restored-outbox-data-safety-0838`
was APPROVE. The authenticated `0806` attempt reached the first durable accept
but then found no outbox entry, so it is not a lifecycle pass. Actual worker
`agt-m2-wc1-restored-current-one-http-proof-0844` owns only the two original
cases after preflight; its result and the caller-cut predicates remain pending.
No whole WC1/AG01/history/outbox deletion claim is made from the fix alone.

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
