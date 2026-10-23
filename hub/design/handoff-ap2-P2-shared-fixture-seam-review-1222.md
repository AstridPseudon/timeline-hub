# Handoff: ap2-P2-shared-fixture-seam-review-1222

**FAIL (confirmedgap).** Independent Agent source audit confirms the 1219
BLOCKED result. No existing public/native call can add a second occurrence
with the source occurrence's same authoritative shot/internal physical
identity.

The concrete caller remains App
`tests/e2e/local/three-products.p2-popup.spec.ts:209-272`: it preserves the
genuine imported media and source row, but the setup still POSTs retired
`composition-revisions` because the required edge cannot be authored through
the current Agent API.

Audited seams and disposition:

- `doc.patch`/`emit_document_commands`: managed occurrence membership and
  shot/revision edges are explicitly refused.
- `occurrence.create`: fresh shot plus occurrence.
- `occurrence.duplicate`: fresh isolated shot/occurrence.
- `occurrence.fork`: fresh shot and rehomes one existing occurrence.
- `timeline.duplicate`: empty-destination whole-timeline copy with fresh
  injective identity maps.
- authenticated public closure/private `_runtime_document`: source-image
  reuse only after an occurrence binding exists; no edge authorization.
- staged G5 `timeline.restructure`/normal publisher: not integrated and
  allocates/recreates chapter identities; no automatic adoption.

Smallest need is Agent-owned: qualify one semantic carrier that allocates
only the new occurrence placement against the authenticated source and lets
the existing Runtime/provider derive managed edges and revision IDs. It must
use the current v2 `TimelineSession.submit`/outbox path, not a patch,
fabricated authority, direct store write, clone, or rehome. Existing
`occurrence.fork` does not own this behavior.

Evidence, exact source lines, attempted command and limits are in:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-P2-shared-fixture-seam-review-1222/report.md`
