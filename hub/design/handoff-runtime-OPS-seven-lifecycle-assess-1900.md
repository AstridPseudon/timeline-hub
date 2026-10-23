# Runtime handoff: OPS seven-lifecycle assessment

## Decision

**PASS for exact private proposal fidelity; FAIL/NO-GO for any current live
normal lifecycle command; UNKNOWN for HOST idleness.**

The reviewed packet is exactly seven generated registrations at
`tests/suites.conf` lines 162–168 plus seven matching env files. Its patch is
`5984d485a2840c780c00a6461e3d6cb98462cef21428e8a9bbc233d18bf18b6a`; the
source manifest is `acb5cf9d2e4f989650e9dfd6eba98f53e89d45db835eeafad1f693091f777678`.
Private flat-file cmp, JSON validation, patch dry-run/apply, and invariant
checks passed. The independent PASS certifies private patch fidelity only,
not HOST/process/lease idleness.

The seven exact names are:

1. `agent-remotion-ap2-p1-f611-1346-nodes`
2. `agent-remotion-ap2-current-8c355-1402-nodes`
3. `agent-remotion-ap2-current-8c-cfa-1415-nodes`
4. `agent-remotion-ap2-current-583-cfa-1451-nodes`
5. `agent-remotion-ap2-current-583-9ce-1513-nodes`
6. `agent-remotion-ap2-current-98ef-259-1608-nodes`
7. `agent-remotion-ap2-current-bac-d9e-1643-nodes`

The packet preserves current 1743 (`agent-remotion-ap2-current-079-2a9-1743`),
P1/P2/P3/F/template inputs, all unrelated rows, and the unrelated P3 row race
at position 36. Seven historical `REFUSE` references and nine process errors
remain STOPPED. No retry, guard waiver, cleanup, or live mutation is supported.

## Why no command is qualified now

Runtime 2a9 contains no `bench_store` implementation, and no store command is
installed. Existing `request-child-venv` and `request-runtime` enqueue legacy
maker requests. Existing `test-run` resolves and launches a command but does
not perform exact managed registration lookup or hold inheritable store lease
FDs through descendants. The missing bounded operation is the single new
bench-store transaction: content keys, latest-two-plus-leased retention,
stable flock liveness, and atomic bench/index/suite/env registration.

Ownership is already settled: core precondition 1858, creators 1850, and
leases 1850. No competing core/helper/adoption author is needed.

## Supported future sequence

After implementation and independent combined proof: use the existing
`request-child-venv`/`request-runtime` callers through `Store.ensure`; verify
exact key, ownership, final-path custody, and registration bytes; resolve the
exact current repo/suite/base-command row; acquire all managed names under one
mutex and retain flock FDs through the supervised command and descendants.
Only then may a separately reviewed managed migration/adoption or eviction
transaction be considered. Unknown legacy/unleased runs remain protected;
there is no `/proc` waiver or invented host-idle proof. Refused targets never
become deletion authority without matching new-lifecycle proof.

No product tests/typecheck/lint were applicable. Runtime remained clean at
`2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d`; full C0v2/frozen34e are unchanged.
See the worker report for the complete row/env tuple hashes, commands, and
limits.
