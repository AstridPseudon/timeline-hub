# D141 targeted pristine-15 candidate

This private candidate is a disjoint normal-service row derived from the exact
reviewed full-d141-pristine row. It has only three scoped changes:

1. suite identity: full-d141-pristine-targeted15;
2. the exact 15 upstream-present node IDs from the independently reviewed D141
   census;
3. durable output name: runtime-targeted15.xml.

The source/tree/clean guards, Agent origin, pytest -q -n3 settings,
D66_OUTPUT_DIR creation and disk/exit/KEEP records are unchanged from the
qualified row. The existing full-d141-pristine row remains registered
byte-for-byte for queued request 8912. validate-row.sh substitutes only its
private harmless Python stub; it never imports Runtime or Agent and never
submits a service request.

The row is a candidate for the normal request-test caller after reviewed
receipt-based admission is available. The caller target is the genuine Runtime
worker rt-pin-fa9cd546, whose checkout and source guard are fa9cd546/tree
124e10db; it is not installed here and does not replace the queued 8912
request or create a request ID.
