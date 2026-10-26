# Handoff

Verdict: `FAIL`; do not grant source qualification, current-pair admission,
REG0, gate, body, or ship credit.

The source/control packet is not delivered at its required absolute ORCH path.
Even when read from the author worktree, it only consumes an externally
provided JSON binding. It does not produce the current request, service ID,
receipt, brief, or installable rows through the existing `request-test`/
`test-run` path. The consumer's hashes and fixture negatives are useful
control checks but cannot authenticate a self-consistent invented receipt.

Smallest next action on the same branch:

1. Publish the committed packet at the exact ORCH evidence path and remove all
   operational dependence on the author worktree path.
2. Have the real existing controller call the normal request-test/test-run
   route, retain the returned service/result identity and owner brief, and
   materialize a binding whose request is the complete v2 body and whose
   receipt/row/brief/tuple/manifest hashes are tied to that same invocation.
   Strengthen only the existing consumer's checks for that authenticated
   ordering; do not add a schema, auth flag, interface, kit, or guessed
   service ID.
3. Re-run the source controls, then install the exact current rows and perform
   the one real pair dispatch at `4714564096` bytes. Keep the historical
   0638 trace gap disclosed; do not backfill it.

Protected integrated/pristine tuples and existing settings remain unchanged.
Old 19479/8912 remain held. No product, test, pin, registry, shared-env,
request, row, body, or full-suite writes were made by this review.
