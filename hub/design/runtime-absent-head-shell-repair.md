# Runtime absent-parent empty-shell repair

Implemented on Runtime `2cb9bb62c88d91fdab03df230ef0b2a3bd81f513`, central snapshot tree `d97b20693d801f6b7889867620f2b51856521147`. Ready for independent review before merge. No public generation, release, pin, App writer retirement, or full suite.

Same-ID create with a new repair key now handles an existing genuinely empty resource whose parent head row is absent or has a null revision. The existing service admission, project/name/archive checks, mutex and transaction remain authoritative. `TimelineCommitStore.adopt_empty_shell` reuses `timeline_scope_is_empty` (F2) and then calls the existing strict `bootstrap`; it introduces no endpoint, DTO, table, alternate publisher or authored root replacement. The existing unpublished-empty-parent adoption remains intact.

The missing-parent branch refuses retained parent revisions, publication events/receipts, headed/publication-bearing or foreign head rows, nonempty hidden legacy documents, timeline scope/dependencies and historical nonempty snapshots. Normal no-provider create also retains an immutable empty legacy internal projection (`shots:[]`, `references:[]`); that exact canonical image is allowed only with the correct project and digest. Any other internal bytes, digest corruption or foreign identity refuse. No authored bytes are normalized or renamed. Bootstrap still installs the exact empty canonical parent; App output/name/slug/tracks require the separate explicit approved Agent init.

Repair records its create receipt in the same outer transaction as the bootstrap publication and history. A crash before the repair receipt rolls everything back. The original create receipt stays unchanged. Exact retries of either create key return its original envelope before adoption; changed payload with a reused key refuses. Real-provider tests prove repair-key retry after initialization, later editing, inverse, direct init undo and restart does not rerun bootstrap or semantics. Init inverse after intervening edit/inverse remains guarded and refuses.

Evidence:

- Bounded service/bootstrap/headless/F1 neighbors: **157 passed, 1 deselected** (actual-provider F1 case reserved for central).
- Private normal-generated full S2 plus approved init schema and local init/repair durability: **94 passed, 1 deselected** (real Door reserved for central).
- Central targeted `rt-m2-absent-head-shell-repair-targeted-1020122347-16578`: **32 child tests passed**, including all **9 commit integration cases**, authenticated generated-client Door/restart, F1 actual-provider regression, the unchanged original missing-positive under `--runxfail`, and absent/null-head repair durability. No xfails.
- Private generator/floor check, artifact check, Ruff and diff check passed.

Approved Agent source is the retained complete archive of `487ca1e0d74edf4aecdd2b4e045294ab089fc273`. Private contract/client remains the previously normal-generated `0.2.14` qualification source: 49 definitions/23 operation conditions, full S2 48/22 plus only init, raw schema SHA-256 `e29c4542a79e5c2098251ac3ff80a47883d08878b79592aa920f1e3321274159`. The private overlay copies those existing generated artifacts onto this current Runtime snapshot; it does not regenerate or patch a provider contract. The original init test file is byte-identical to the archive. Successful no-head history is built by real create/bootstrap/init APIs. SQL in the null-head positive only represents an empty nullable head row; it seeds no revision, publication, receipt or successful history.

Exact commands, limitations, source archive and hashes: [/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-m2-absent-head-shell-repair/DetailedReport.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-m2-absent-head-shell-repair/DetailedReport.md).

Next: obtain independent code review before merge, then qualify App's replacement workflow separately. This proves the missing Runtime capability, not App UI/outbox behavior or a public artifact release.
