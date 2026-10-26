# A3/P2 D141j independent source visibility review

## FAIL — D141J-VIS-001

The active-occurrences observer obtains `acceptedReadHeadRevisionId` from
`getAcceptedReadHeadRevisionId()`, which returns the first accepted-read event
in the collector snapshot. It does not correlate the active occurrence array
with the accepted read that produced that array. The mounted control performs
one accepted read and one render only, so it cannot detect a later accepted
read/render. If a later read changes `activeCanonicalOccurrences`, the retained
active event can still carry the old first head and the checker can pass.

This is a source-observation qualification failure, not a product-cause claim.
Cause remains UNKNOWN. The author manifest's base-valued `working_tree_commit`
is also inconsistent with the authenticated candidate terminal, but the review
manifest records the independently verified candidate identity.
