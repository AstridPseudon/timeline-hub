# D134 protected review findings

## Source-first result

PASS. The candidate is one test-file change from the declared Agent base. The
change replaces the old in-process `RuntimeService` and manual provider
registration with `new_runtime_daemon(..., authoring_profile="astrid")`, and
opens an authenticated `AstridClient` against that daemon. The existing seed
helper receives that client; no provider, history, item, media, mapping,
counter, or client record is synthesized.

The ordinary-sheet file is unchanged and its four detached preflight cases
remain the declared UNAPPLIED dependency. No assertion, authored input,
fixture topology, source pin, selected-media predicate, inverse, retry,
history, or no-write case was rewritten.

## Functional result

UNVERIFIED. The central targeted run is not functional evidence: it deselected
all five integration nodes. The one permitted live integration body was not
submitted because the central service has no exact-selector route using the
required immutable Runtime checkout. The existing matching `*-nodes` suite
references a missing `rt-pin-8ea0766f`; substituting another Runtime or running
the daemon locally would violate the brief. No retry or alternate route was
used.

## No source finding

No source-level finding requires changes to the candidate. The remaining
status is an environment/test-service prerequisite block, not a product or
test-body failure.
