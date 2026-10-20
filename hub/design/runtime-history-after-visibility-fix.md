# Runtime history after catalog visibility

Completed worker rt-m2-history-after-catalog-visibility. Runtime base601d533d91e3726c4f7ae74723e8eff4adbe2f90; final qualified source tree345a58f9b43d3162f83617189ed6f147b132eb7a. Worktree /home/user/work/wt/rt-m2-history-after-catalog-visibility. The harness assigns the commit after worker exit.

## Exact regression and root cause

Read Agent's report at /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-recover-real-catalog-gate/report.md and its exact probe tests/sdk/test_timeline_checkout_history_runtime.py::test_catalog_recover_uses_real_http_and_preserves_closure_before_revision_restore from tl/agt-m2-recover-real-catalog-gate, source afcb326c8bfb216e404502c1ff4a08bde5c735ca.

Real commit/archive/recover succeeds and preserves canonical head/closure, but the next history call fails409 history_unavailable, “timeline has untracked writes.” TimelineCommitStore.head allowed only timeline.renamed after the head's accepted receipt. Authenticated archive/recover therefore looked like untracked film writes. 601 fixed recover replay provenance, not this check. Legacy baseline installation independently rejected the later events/scoped receipts.

## Minimal diff

- Extract the existing _timeline_resource projection unchanged into runtime_protocol/timeline_catalog.py. Writer and verifier share exactly one state representation.
- Reuse full timeline hash-chain/project validation. Account for archive/recover only through a unique matching receipt at the exact stream position: timeline/aggregate/event identity, ordered project sequence, strict event shape/version, normal request hash, full result/project/head association, contiguous catalog versions and final live visibility/version must agree.
- Compare catalog results with live film projections, and flat shot/reference state with its retained legacy snapshot. Reuse immutable closure validation, accepted-document equality and existing shot/text guards so genuine catalog receipts cannot launder earlier untracked film writes.
- Permit only those proven receipt IDs through baseline's existing scoped-ledger guard. Unknown events, historical recover target_version facts, missing/malformed/ambiguous receipts and projection changes still refuse. Existing display-only rename policy remains. Preserve head's CommitRejected contract.

Product delta:104 net lines, including the unchanged projection extraction. Permanent tests:168 lines, exactly two nodes. No provider execution, scene evaluation, new film-history edge, DTO, table, journal, ledger or backfill. Reads do not write.

Reads and catalog mutations hold the existing store mutex; acceptance rechecks the same proof in its existing SQLite transaction. Existing single-admitted-writer/realm-lock assumptions apply. Ledger-first exact accepted retries are unchanged.

## Old records and remaining limits

Verification reads retained results without time-bounded response replay. Existing expired result hashes are checked against the same exact projection with event version/visibility. A proven legacy publication may have had a null publication ID when its catalog receipt was issued; only that verified legacy case permits the null field, preserving the immutable revision and all other state.

An expired catalog result followed by a rename can lose the old display name needed to prove its exact hash. It stays fail-closed; no guessed name, state upgrade or reevaluation. Receiptless/unknown facts and requests outside the normal archive/recover body forms remain unproven. Ordinary expiry/restart is covered by the service probe; no extra permanent matrix was added.

## Final proof and sources

Final central request rt-m2-history-after-catalog-visibility-catalog-history-agentafcb-integration-1020193826-760: **2 passed in6.83s**, exit0, source tree345a58f9b43d3162f83617189ed6f147b132eb7a.

Uses immutable clean Agent afcb326c8bfb216e404502c1ff4a08bde5c735ca at /home/user/work/wt/agt-pin-afcb326c; normal generated client0.2.13/schema sha256:8de823011a121359b9ad021e283b45afb6baeabc8a154a02bd086d1260a8b8f4. Tests assert actual startup RuntimeCommitService and matching client/server metadata; no overrides/dependency changes.

The positive reuses Runtime's precut film fixture and Agent's original normal authenticated daemon.endpoint /v1 connection. Real SDK Session.move -> archive/recover -> exact unchanged film rows/CAS/history -> restart/exact catalog receipts -> fresh Session.restore. The negative follows an accepted closure's shot_id to a populated project_shots.name, proves the stored value changed before genuine catalog receipts, then requires409 history_unavailable/unaccounted_shot_projection and no accepted writes. No accepted history/receipts are fabricated with SQL or a fake provider.

Local main guard suites:128 passed/1 existing integration node deselected. Selected service cases:37 passed/14 HTTP cases deselected. The same-film real-service probe also passes ordinary catalog visibility, exact history, expired catalog hashes/restart and the populated shot-projection negative. Exact commands/results are in the worker report.

## Qualification corrections and next owner

Original queued17928 was cancelled before execution. Executed3733 failed both nodes on worker fixture mistakes: the added browser transport's /api/runtime/v1/timelines/film/archive is outside door policy (classify=None ->404), and the capture has no timeline_shots rows. Normal server.py already serves authenticated /v1/timelines/film/archive. No route/auth/schema/ID changes were made. Preflight found project_shots3/head3 and shot_items0; the final negative uses an existing referenced project_shots field. Manager explicitly authorized the final rerun of only those failed nodes. Product was unchanged throughout fixture repair.

Agent's high-level recover facade independently refuses an old catalog version before HTTP, including exact retry. Runtime's retry check uses the existing generated transport with original body/key and unchanged result/no-write assertions. That does not qualify facade retry: the Agent-owned case stays OPEN and its original assertion is retained.

No full/all-M1/renderer/browser/private/integration-wide gates claimed. Runtime manager reviews the harness-assigned fixed SHA; Agent then owns only its original failing catalog/restore node retry. This is not a foundation-gate completion claim.
