# Runtime RT03 current6537 raw-source port

Status: bounded source result; not native acceptance or publication.

The exact raw-media custody source from Runtime `f53bf588bf70b090ce8e0bed5ccb7d91157771b6`
(tree `d82f37052847949e77c12e1704c3f27c6dd56a46`) was ported onto current
Runtime `b92d3e7a05eec65c142294ef4873edd059e9b31d` (tree
`6abc2f117391de8e7e35c0283f575a002199894d`). The port adds only the internal
`raw_media_info` protocol/read path and its reviewed custody tests.

The supported source path is exact and declared only: `MediaManifestEntry` has
equal `media_id`/`content_digest`; the project must own the digest as a managed
object; one regular CAS descriptor is opened and checked for identity, full
SHA-256, and size; the captured result is revalidated against the same pin
before acceptance writes. The accepted candidate must include that exact pin in
its manifest and authorized-media closure. Missing, foreign, unowned,
undeclared, or tampered objects refuse atomically. Exact accepted retries remain
ledger-first.

Current transcript source custody and speech behavior remain intact. Ordinary
schemas/validation, `MediaManifestEntry`, `MediaInfo`, selected-media reads,
store, HTTP, generator, projection, materialization, and public contract bytes
were not changed. No public caller, endpoint, DTO, source authority, native
acceptance, rawOLD path, pin, version, or release claim is made.

Evidence: raw custody tests `6 passed`; bounded source/neighbor suite `171
passed, 1 deselected`; `git diff --check` passed. The sandbox could not create
HTTP sockets, so the socket-dependent guard cases remain unverified.
