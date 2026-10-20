# Runtime history after catalog visibility

Worker: rt-m2-history-after-catalog-visibility. Runtime base: 601d533d91e3726c4f7ae74723e8eff4adbe2f90. Worktree: /home/user/work/wt/rt-m2-history-after-catalog-visibility. The harness assigns the final commit after this worker exits.

## Exact reported regression and root cause

Read Agent's report at /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-recover-real-catalog-gate/report.md and its exact probe from branch tl/agt-m2-recover-real-catalog-gate, tests/sdk/test_timeline_checkout_history_runtime.py::test_catalog_recover_uses_real_http_and_preserves_closure_before_revision_restore (source afcb326c8bfb216e404502c1ff4a08bde5c735ca).

The reported real commit/archive/recover succeeds and preserves the canonical film head/closure. The next history request fails with 409 history_unavailable, “timeline has untracked writes.” Runtime's TimelineCommitStore.head checked all events after the head's accepted receipt and allowed only timeline.renamed. Authenticated timeline.archived/timeline.recovered therefore looked like untracked film writes. 601 fixes recover replay provenance, not this history check. Legacy baseline installation also independently rejected those later events/scoped receipts.

## Minimal product change

- Extract the existing, unchanged _timeline_resource projection into runtime_protocol/timeline_catalog.py so the writer and verifier use exactly the same state representation.
- Reuse the existing full timeline hash-chain/project validation, then account for archive/recover events only through a unique matching receipt at the exact stream position. Verify timeline/aggregate identity, exact event IDs, project-sequence ordering, strict event shape/version, the normal request hash, receipt result/head/project association, contiguous catalog versions and final live visibility/version.
- Compare every catalog receipt's full film projection with live state. Compare flat shot/reference state with the retained legacy timeline snapshot as well, so a raw write made before the genuine catalog receipts cannot be laundered by them. On recorded heads, reuse immutable closure validation, accepted-document equality and existing shot/text guards before granting the exception.
- Allow only these authenticated receipt IDs through legacy baseline's existing scoped-ledger guard. Unknown events, historical recover events with target_version, missing/malformed/ambiguous receipts and projection changes still refuse. Existing display-only rename handling stays in place.
- Preserve head's existing CommitRejected failure contract. No new film history edge, provider execution, evaluator, DTO, table, journal, ledger or backfill. Reads do not write.

All current reads hold the existing store mutex, also held by catalog mutations. Acceptance rechecks the same head/proof inside its existing SQLite transaction. Ledger-first exact accepted retries are unchanged. This relies on Runtime's existing single admitted writer/realm lock; it adds no new external-writer synchronization.

## Old records and limits

Verification reads retained results without invoking time-bounded replay. Expired catalog responses can be checked using their existing exact result hash, with the event version/visibility substituted into the same projection. Proven legacy baseline publication IDs may still have been null when a catalog receipt was issued; this is allowed only on a verified legacy publication, retaining the same immutable revision and other state.

An expired catalog result followed by a rename can lose the old display name needed to reconstruct its exact hash. Such a record remains fail-closed; no guessed name or state upgrade. Receiptless operations and requests outside the normal archive/recover body forms remain unproven. No new test matrix for these limits was added. The service probe checks ordinary expired hashes and restart; the permanent regression is the exact normal HTTP lifecycle plus one raw flat-shot negative.

## Qualification scope and source

The permanent file is tests/test_timeline_catalog_history_integration.py (two nodes). It reuses Runtime's precut film fixture and normal startup-loaded Agent RuntimeCommitService. A real generated-client transport adapter uses the existing browser door; public SDK TimelineSession performs move and a fresh-session restore. Film rows/CAS and complete history are compared exactly across archive/recover and restart; exact catalog receipt retries write nothing. The negative makes a raw flat-shot mutation before genuine archive/recover and expects history_unavailable without writes. No accepted history is manufactured with SQL or a fake provider.

Manager-approved immutable Agent source: /home/user/work/wt/agt-pin-afcb326c, afcb326c8bfb216e404502c1ff4a08bde5c735ca. Normal generated client contract 0.2.13; schema digest sha256:8de823011a121359b9ad021e283b45afb6baeabc8a154a02bd086d1260a8b8f4. No metadata overrides or dependency changes. The default Agent a760ecca lacked Session.restore, caught before submission; the manager supplied the exact peer source and named lane. Composition rendering is not exercised by this task.

Central request (single, scoped):

```
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test rt-m2-history-after-catalog-visibility catalog-history-agentafcb-integration --files tests/test_timeline_catalog_history_integration.py
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test rt-m2-history-after-catalog-visibility-catalog-history-agentafcb-integration-1020191203-17928
```

The named lane uses exact clean Agent HEAD and:

```
env ASTRID_CHECKOUT=/home/user/work/wt/agt-pin-afcb326c ASTRID_RUNTIME_CHECKOUT=$PWD PYTHONPATH=$PWD:/home/user/work/wt/agt-pin-afcb326c PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider -m integration tests/test_timeline_catalog_history_integration.py
```

Final central result and exact local results are recorded in the worker report. No full, all-M1, renderer or browser suite was requested. Agent owns the subsequent retry of only its original failing node, after Runtime manager review of the harness-assigned fixed SHA. This change does not declare private, integration-wide or foundation gates complete.

The originally queued request17928 contained an added facade-level retry call. Source review caught Agent's pre-HTTP refusal of that old catalog version. Runtime manager requested cancellation before execution and authorized one corrected snapshot on 2026-10-20T19:17:19Z, changing only that retry to the existing generated transport with identical body/key/result/no-write assertions. This qualifies Runtime's idempotency boundary; the independent Agent facade case stays OPEN and its original assertion is retained. Final corrected request/tree/result follow in the report.
