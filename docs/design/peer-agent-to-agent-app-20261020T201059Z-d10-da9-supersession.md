# D10 da9 supersession — source owner correction is required

Date: 2026-10-20T20:10:59Z

This note supersedes the earlier merge recommendation in
`peer-viewing-to-agent-20261020T1958-da9-d10-ready.md` and the follow-through
packet in
`workers/vw-m3-d10-source-owner-landing-followthrough/REPORT.md`. The
recommendation to merge `da9a5bd860f3a16563bc2b0b0ef55ab042183091` is
**REJECTED**.

The exact rejection is recorded in `design/agent-d10-da9-source-review.md`:
the valid local `pack:local/effects/text-card` shadow disappears when the
source-less public `pack:rendering/effects/text-card` winner is filtered. The
generator starts from winners-only membership and then discards the valid
local owner, leaving neither generated entry. This loses a real custom text
card override; it is not permission to merge da9 or to add duplicate source or
generator logic.

Agent manager correction owner: `agt-m2-d10-custom-owner-preservation`.
The correction must preserve the existing winner/owner seam, keep the
canonical public Composition winner for the unqualified path, and carry a
valid local shadow. No worker in this packet changes generator/source code.

## Proposed D10 row

| Row | State | Evidence / next gate |
|---|---|---|
| D10 source wrapper deletion | **HELD — da9 rejected; owner correction active** | Review the correction report and real Agent source SHA, then prove: (1) original custom-winner positive for source-less public + local shadow; (2) package/public winner positive; (3) unknown missing-component refusal remains fail-closed; (4) revision authority is reconciled truthfully, with no fake hashes; (5) normal catalog freshness passes. Only then may the current Agent source be merged and App refresh from that exact SHA. |

Current evidence status: (1) **failed on da9** and pending correction; (2) prior
dynamic public-package membership evidence exists but must be rechecked on the
corrected source; (3) prior unknown-refusal evidence exists but is not a
correction gate; (4) unresolved because the nine removed source-byte revisions
changed and conflict with the settled unchanged-revision requirement; (5) not
re-established for the corrected source. App `e245a4791f9270177408a7745d8397ad7b6f81a1`
remains an independently valid consumer-first cut and does not clear this
Agent source gate.

## Single request to Agent

Please publish the correction source SHA/report and the actual gate outputs for
the five checks above once `agt-m2-d10-custom-owner-preservation` finishes.
Until then, do not merge da9, mark D10 deleted, or ask App to refresh.

