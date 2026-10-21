# App2 M2 selected seed current-main packet report

## Result

Prepared the reviewed main execution packet at
[run-on-main-app2-selected-seed.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/run-on-main-app2-selected-seed.md).
Prepared one owned current-source runner artifact outside the product tree:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-selected-seed-current-main-packet-1110/artifacts/run-owned-selected-final95-current-main.sh
SHA-256 dcd4bf11e178cabd63a0a450e206b7450abb098a27110a2eca6ecd085794cefc
```

The runner is a data-only rebind of approved `96629aa9…`: current App
commit/tree, current selected spec and harness hashes, and the approved
current readiness guard. The final95 graph, helper/driver scope, argv, budgets,
private paths, cleanup, and explicit partial-evidence copy returns are intact.
The shared helper was not changed.

HOME's `e5afdaed…` phase-order fix is present in the committed harness. Static
inspection confirms the selected publication retains the original payload,
`draft-1`, and its returned `new_head` becomes P1's expected head; selected
credential provisioning follows restart. The current selected case retains
the normal discovery proxy/operation-origin and case-local context path.

## Checks run

```text
git rev-parse HEAD / HEAD^{tree} / 32b ancestor                 PASS
current source file SHA-256 inventory                            PASS
runner diff against approved 96629aa9                            PASS: binding/guard hunks only
sh -n owned current runner                                      PASS
git diff --check                                                  PASS
```

No Playwright collection, browser, build, Runtime, daemon, localhost/live
socket, central service request, install, targeted product test, or full suite
was run. The packet itself contains the complete preflight and the guarded
actual command for later review.

## Decisions and limitations

- The original `a50ca4a0` / tree `92391f9a` / spec `10250fa4` source and the
  approved `96629aa9` runner remain available and are not relabelled.
- The current source is `tl/integration` at `0cc2583a` / tree `320e74a9`.
  The current spec's readiness/context delta is treated as the already
  approved retained change; no spec or harness edit was made here.
- The runner remains an owned artifact, not a product-tree file, so adding this
  packet cannot invalidate the exact main source-tree guard.
- No main execution was requested. The orchestrator must review the packet and
  run its preflight on clean main before authorizing the one actual.

Changed live callers: **NONE**.
