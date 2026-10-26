# D141p new-head and pristine unit recipe

Status: `NOT_READY`; no Vitest, Node phase, browser, or service command ran in
this preparation.

After the qualified new App head is received, use the existing central service
for exactly one full run on each source kind:

1. The qualified new App checkout, identified by `repo=app` and its exact
   full commit/tree and clean-source receipt.
2. A pristine receiver pinned to
   `d822d2f5d2bd05187b4ff5b6071c3e13945d4747` / tree
   `2af40a015057779ceb4e4b37cad62e1469aa7e36`, with clean status. This is not
   substituted by `request-test integration:app`.

Use the existing commands, with worker names supplied only after the source
receipts exist:

```text
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test <qualified-new-app-worker> full)
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"

R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test <pristine-d822-receiver> full)
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
```

The two full runs stay separate by source and environment kind, with their own
request/status/exit/summary/log/`KEEP` artifacts. If Vitest fails or
short-circuits, run the exact existing standalone `npm run test:node` phase on
each head through the service. Do not invent a Node-only row, change the npm
script, add counts, or classify without a matching environment kind.

The full pair is followed by the controller's placement-first D66 reproof and
the remaining P2/P1/P3 bodies. No body, preflight, checkout, registration, or
test execution is part of this packet.

