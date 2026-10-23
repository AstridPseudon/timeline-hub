# PASS — P4 staged-path execution eligibility

Reviewed exact Agent source `246f92507f15ac16c3bb559b7ce1576a608c86d8`, tree
`1358a918b2d20413e86c4cd56031a5b92e9b8842`. This is the reviewed current P4
source (`38b724…`) plus the exact two-file public facade donor delta
(`9fbb84…`). The five P4 donor blobs remain exact:
`05f7aa2b`, `fd248182`, `85218e8e`, `80c15e29`, `1ed257c4`.

The original node
`tests/editing_conformance/test_p4_cli_sheet_v2_runtime.py::test_cli_sheet_v2_runtime_preserves_document_and_reads_back`
is eligible: exact integration collection collected one test; scoped Ruff,
private mypy, vendor-lock, artifact-manifest, and diff checks passed. It uses
the real CLI parser → native sheet/session/outbox → generated Runtime commit
route and real `show`/`history`, asserting accepted canonical document,
head/digest/receipt/step/history fields. Its semantic sheet route is
`clip.move`; the current G3 emitter remains present for free-document edits but
is not invoked by this native-sheet node.

Canonical schema SHA-256 is approved `d106dfe8…`; the two approved schema-floor
blobs are exact (`f2521256…` source). Normal producer is Runtime
`34eac0041b0891e9011966b39bcbd26053fde5bc`, tree
`9853574865f25e08284e82ffb26c0bdecaa16a30`; lock and artifacts are current.
Public `TimelineSession.undo(..., steps=...)` and `Timeline.undo` dispatch are
real; the target test has no cast or alternate API. Existing exact
SDK-15/public-107/local-2 facade evidence is reused.

`ccc521b7811231984564f07ea50e9eb710466b1a` is explicitly unqualified and is
not used as a reviewed base. No HTTP body, socket, browser, full suite,
renderer/native14, G4, whole-P4, H3, or public-adoption credit is claimed.

Later Proof may run exactly one existing-service body node with the owner-join
command recorded in the worker report, using the matching Runtime checkout and
the exact staged source.
