# Same-batch strict inverse guard

Implemented on Agent base `4ef1391c`, public S2 unchanged. This closes F1 from
`agent-review-selected-param-authority.md` and the 2026-10-20 13:27 escalation.

An accepted unchanged `clip.set-element(P1)` publication T could previously be
reversed in `[clip.set-element(P2), inverse(T)]`: the inverse checked accepted
intervening history but never saw the first command's recorded write. Equal JSON
does not remove authored write intent under PLAN section 4.1.

`commands.execute` now passes its finished earlier batch records to
`apply_inverse` through an internal keyword argument. After checking accepted
intervening history, `apply_inverse` checks that staged suffix with the existing
`check_intervening` implementation and current stage state. These records remain
separate from the inverse target records. They are never coalesced into the undo
group, assigned a publication, or exposed through new recorder/DTO fields.

The target `AcceptedRecords` object, verified boundary loader, ordered restoration,
within-inverse scratch stages, and schema resolver/cache behavior are unchanged.
Unavailable accepted history still refuses. Normal forward replay keeps its
existing equal-state ABA policy. Later explicit commands retain their ordinary
execution order.

Product diff: 4 added / 2 removed lines across `commands.py` and `inverse.py`
(net +2). No schema, generated client, Runtime pin, provider, or Runtime DTO
changes. S2 SHA256 remains
`a6f1aaa9dfcc31828bd04c908158fd7fd9a825df6c9f88f79b81779273a190ef`.

Permanent native regressions use real pack admission, the ordinary startup-loaded
Agent provider, RuntimeService, and RequestCommitPort. Both same-pin and new-pin
unchanged staged selections now produce `409 intervening_write`. Tests compare
the complete head/publication pair, canonical closure, accepted history, SQLite
dump, and every CAS object's path and bytes, and assert SQLite `total_changes`
does not increase. The original accepted request still retries from the ledger
while semantic execution is forbidden.

Native positives cover a disjoint staged track label before a one-target or
multi-publication inverse, exact canonical restoration with opaque params, and
`[inverse, explicit selection, PARAM]` with the staged pin in the PARAM record.
Three additional native-command scalar cases cover unchanged/ABA writes, later
explicit writes, replay, and reversing a composed batch.

Qualification: 541 targeted command/provider/conformance tests, 29 native Runtime
tests using immutable Runtime `b748ae723b51c6d578ba7a393209ce37d6e2b0c3`, and 9
numeric native tests using their own official Runtime pin
`2c4ac180c2220bdad966bc01e95ad230e99ce26a`, all passed. Ruff and diff whitespace
checks passed. No existing positive was changed or xfailed. No full, browser,
socket, or renderer suite was run or requested.

Exact commands, development diagnostics, and scope limits are recorded in
`workers/agt-m2-inverse-staged-write-guard/notes/report.md`. This result closes the
core inverse gap; it does not qualify the private PARAM resolver or its separate
legacy-alias compatibility issue.
