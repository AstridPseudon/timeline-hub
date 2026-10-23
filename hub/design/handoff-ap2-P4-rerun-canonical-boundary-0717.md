# P4 rerun canonical-boundary handoff

**Result: PASS for the bounded correction.**

Changed exactly one tracked file:
`tests/editing_conformance/test_p4_note_rerun_v2_runtime.py`.

The ordinary restarted `timeline.open()` remains asserted to omit the private
`_runtime_document` cache. The test now uses the existing authenticated exact
revision/publication `open_bundle` read, verifies project/timeline/pair/current
head and canonical parent binding, proves the authenticated bundle equals the
public bundle plus only its authenticated canonical/private cache and
publication pin, and applies the unchanged full physical/shared-closure
oracle to that authenticated read. No synthetic document or cache was added.

All original conflict, peer edit, bounded callback evaluation, request/key,
structured reply, history/receipt/readback, opaque/null/absence,
source-mapping, shared-closure, restart, and outbox assertions remain. The
ten-note neighbor is unchanged (`b8876628d100897a9dcda6750fc5395a3b5b41f3`).

Source SHA/tree: `dd0bd73e2cef92cdca8213d26e175e350b484af6` /
`e762ea942c4139b97f782a1882e7de3453b42cb8`.
Rerun blob: `cbd332db227ecb9c6254e8ced0af72c3de91821e` →
`72d11a2a8f9f8915a22e325bc15f2edadbae96ff`.

Evidence: exact 2-test collection PASS (known unknown-`timeout` warning),
scoped Ruff PASS, scoped Mypy PASS, `git diff --check` PASS, and outside-file
blob equality PASS. No HTTP/body/service/socket/browser/build/full run or
test-service request was made. Live acceptance remains manager-owned.

Inherited disposition is unchanged and reported exactly: **SOURCE PASS. OPS
target-row PASS. RERUN READINESS FAIL/not ready.** The confirmed cause was the
public authenticated-cache boundary, not a product defect. Runtime evidence
remains checkout `a5d4258312c979024865ee704da2d632ca5b2730`, tree
`f74b016ea837f8148db4a602c972073a226ed177`; no allowance changed.

Manager next: run the independent live rerun, followed separately by the
original ten-note live node.
