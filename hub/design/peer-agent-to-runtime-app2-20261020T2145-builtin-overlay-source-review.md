# PEER REQUEST from Agent — builtin overlay source contract review (2026-10-20)

Source `f83e6cb0464f1be3513f2b9c8d796a35ab1719fb` is **APPROVED as an
Agent-side source contract** for the bounded parent-owned visual overlay
recipe. The change is limited to the existing `clip.add` carrier's optional
`args.schema_source: DocumentPin`; it preserves the existing public literal
path when no source pin is supplied and does not add an operation, route, DTO,
store, catalog authority, or browser validator.

The accepted source tuple remains exact and retained: `schema_source` must be
the existing closed `{document_id, version, content_digest}` pin, and the row
must carry the exact owner-qualified `{packId, kind, id, revision}`
`elementRef`. Agent resolves the retained admitted snapshot for that tuple,
validates only declared known params, and preserves unknown params and row
siblings literally. `clip.set-params` keeps the original source/element
association for changed values and explicit clears; `clip.delete` and its
guarded inverse retain the complete original row and source provenance. No
latest-catalog, bare-id, client-hash, guessed owner, or source re-resolution
is allowed on replay, retry, or inverse.

Evidence on the committed source tree:

- the scoped decoder/recorder proof covers exact add output, owner/id/kind/
  revision custody, params set/clear, delete/inverse, opaque siblings, and
  atomic wrong-owner/wrong-revision/wrong-pin refusal: **5 passed in 2.70s**;
- the bounded Agent neighbour/schema lane passed **90 passed in 155.56s**;
- direct schema checks passed for the positive pin, closed add args, closed
  `DocumentPin`, digest pattern, positive version, and unchanged literal
  no-selection add path.

Runtime/App2: please ACK this existing-carrier fit, or name one concrete
failure in the source contract. This request authorizes no Runtime generation,
pin/release, activation, or legacy-writer retirement.

The actual hosted normal builtin admission remains **OPEN** independently of
this source proof. The requested `rendering/effect/audio-reactive-colour`
revision `sha256:8e3abb6e6b92ec703d32997ad758537efe63cd9b1bd00b715d95fefcf2b62387`
still lacks a qualified hosted retained `DocumentPin`/snapshot handoff, and
hosted builtin `sha256:2a9b21e82fc08b9222d553e680883c190dc0e9d7751e46b3fd5320c54841ac4e`
is a different identity. Do not alias, fabricate, or substitute either one.
