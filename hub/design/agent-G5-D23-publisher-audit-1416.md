# G5 D23 ordinary publisher audit

## Disposition

**PASS for the bounded ordinary publisher/helper source path; G5 remains DRAFT and
P1 remains NO-GO.** This is not cumulative migration qualification and does not
authorize deletion before the P1 GO gate. D23's child-word decision is recorded
below as a deferred, visible failing test.

Audited tree: Agent HEAD `74b92b2a9` (`tl/agt-G5-anchored-helper-fixture-1317`),
with cumulative G5 drafts `34d00031f` and the earlier normal publisher/helper
commits in its ancestry. The working tree was clean before this evidence-only
change.

## Source trace and production caller

- `astrid/sdk/timeline/publish.py:90-157` is the production `_PublishMixin.publish`
  caller. It rejects `force`, runs the core validator, commits the ordinary path,
  performs narration/transcript follow-up, resets the working copy to the new
  head, and returns the Runtime receipt.
- `publish.py:159-291` is the ordinary `_commit_document` path. It opens the
  durable `TimelineSession` at `:171`, reads the authenticated history/base pair,
  refuses closure/provenance changes, and calls
  `emit_document_commands(base, candidate)` at `:255`. A valid helper journal
  replaces those commands only after `journal.helper_batch` replay verification
  at `:256`.
- `publish.py:283-291` submits through `TimelineSession.submit` with the full v2
  request shape: exact base pair, commands, label, merge mode, request/step
  reads, steps, expected outbox state, idempotency key, and evaluation digest.
  The helper path uses `fields` plus sequential per-helper steps; untracked
  ordinary changes use conservative `atomic` and a timeline read.
- `astrid/sdk/timeline/journal.py:113-169` captures nudge inputs, including the
  original clip row and retime/anchor consulted fields. `:223-286` replays every
  saved operation against the authenticated base, checks before/after digests,
  and emits contiguous command ordinals, patch changes, and step-local reads.
  Tampered/forged journal facts therefore do not become authority.
- `publish.py:396-420` re-reads and flattens the accepted head, clears the local
  journal, and preserves a recoverable note if the post-commit local reset fails.
  `:422+` keeps narration binding as a separate durable text-binding commit,
  with retry identity owned by the Runtime flight/history.
- Current ordinary callers include `astrid/packs/timeline/cli.py:2983`,
  `astrid/packs/timeline/cli_working.py:493`, and Python `Checkout.publish` callers.
  The facade remains `astrid/sdk/timeline_checkout.py`; its public `Checkout`
  and `TimelineSession` imports resolve to the new homes.

## Contract comparison and exact bounds

Against C0 `design/commit-v2.md` §§1/2/3/5, the source preserves the required
scope, exact base pair, commands, label, steps (`intent`, `tags`, ordinals,
patch, reads), merge/read declarations, idempotency key, `dry_run`/source/
rationale/group annotations where supplied by the session, and canonical
accepted/merged Runtime receipts. The provider-owned reply surface remains
Runtime-owned: receipt/records/bindings/effects/dependencies/history/undo steps,
preview/required/would-status, and structured invalid/conflict code/path/head/
hint/command fields are not fabricated by this publisher.

Positive nondeferred dispositions:

- **PASS — ordinary publication:** `_PublishMixin` reaches the durable session,
  not the old whole-candidate writer, and refuses ambiguous base or closure
  changes before submission.
- **PASS — helper semantic capture:** operation-time capture, authenticated
  replay, exact before/after digests, sequential steps, and declared reads are
  present. Parent-target anchor capture retains the existing native exact
  transcript/document pin and stable-word binding; no child alias is inferred.
- **PASS — facade/reset/narration source review:** facade imports and mixin
  wrapping are intact; reset is post-acceptance and non-destructive to the
  durable commit; narration retries through its own durable session identity.
- **PASS — bounded controls:** 22 selected nodes passed (see report.md). This
  includes genuine parent anchor scope/base-pair capture, missing/forged anchor
  no-write controls, ordinary helper merge/conflict/tamper/lost-ACK controls,
  one non-moved-head sequential helper case, literal parent cut cases, and
  ordinary facade controls.

Remaining nondeferred requirements / gate bounds:

- **FAIL / gate not met — P1:** no P1 GO exists, so G5 retirement/deletion is
  not complete. The legacy definitions/imports remain visible in
  `astrid/sdk/timeline/document_diff.py`, `astrid/sdk/timeline/store.py`
  (`three_way`, `publish_bundle`), `astrid/sdk/timeline_checkout.py`, and the
  CLI `commands-file` route. Do not delete them in this audit; the orchestrator
  owns the P1 gate and retirement timing.
- **DEFERRED, unchanged and visibly failing — child-clip word anchors
  (relational timing):** the retained child-on-second positive remains in
  `tests/sdk/test_timeline_helper_capture.py::test_cut_nudge_restart_merges_other_cut["second"]`.
  It is unchanged, unskipped, and visibly fails at the existing missing exact
  child word binding boundary. This is D23's deferred relational-timing case,
  alongside the two D14 cases. No guard, schema, API, tuple, or source author
  was added.
- **UNVERIFIED here:** moved-head sequential helper rebase and the original
  process/browser/full body were intentionally not rerun. Existing R1-private
  `1403` staged source is an active owner path, not a reason for a second source
  author or body rerun.

Required final join files when the gate is revisited: `publish.py`,
`journal.py`, `emitter.py`, `sync.py`, `checkout.py`, `document_diff.py`,
`store.py`, `timeline_checkout.py`, `astrid/packs/timeline/cli.py`,
`astrid/packs/timeline/cli_working.py`, and the unchanged helper controls in
`tests/sdk/test_timeline_helper_capture.py` plus the relevant P1 fixtures.

## Exact source hashes

```text
5cc64370edee54737c837bde61c09fa4e5ca5c145b14d9df1b6f6a5c55e5aefd  astrid/sdk/timeline/publish.py
f59a74dd3c477a3f8d86b06a61363986d2b33a8a9f63baf7e86edd37f4cef1ad  astrid/sdk/timeline/journal.py
ca09ea41f41b598ce78d9083b4b46993867891b67ca586896baefa99edce5ee7  astrid/sdk/timeline/emitter.py
3e9ccf0aafa1b7fe0718fcd8c05b35d50fc137d2a81b7ec6ff709943b0100a7f  astrid/sdk/timeline/sync.py
4250a41f14b95e2640fbae85390bb68e3120ba6d2d5c250f0342868cedfa158a  astrid/sdk/timeline/checkout.py
9a156686486811cc8017bed44d461dd81b7281cbfa24caa91e7cd9f69f9f107f  astrid/sdk/timeline/document_diff.py
476b9ba69f860a857bf88707590c9b61a5eba80805fa1d3ca2602952b1775bf4  astrid/sdk/timeline/store.py
```

