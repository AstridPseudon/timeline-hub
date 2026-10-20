# Agent local-history review — current

Reviewed `tl/agt-m2-local-history-cut` at `88dd38f13137f274e8a02aa1d9e65ebe39cbf531` against `c456b328`. Read PLAN, repository AGENTS.md, the worker report, its detailed report embedded in log.txt (the report.md was subsequently replaced by its short final response), all seven changed files, and the surrounding publish/store/outbox/sheet/CLI paths.

**Verdict: approve the native publication entrypoints; request changes before claiming the local-history boundary guarantee complete.** The patch is a useful bounded improvement and introduces no regression in the exercised existing positives. Two reproducible boundary gaps remain within the guarantee it claims. A third recovery issue is inherited. This is not a rejection for the separately documented, unmigrated writers, and is not evidence that the native inverse can directly rewind Runtime accepted history.

## Findings

1. **P2 — Revision equality does not identify an accepted-head boundary.** Reviewed `astrid/sdk/timeline/checkout.py:272–279`, with `publish.py:96–102`. `_restore_draft` compares only `base_parent`, whose canonical shape is revision ID plus content digest (`astrid/core/timeline/authoring_bundle.py:464`), without publication identity. `_reset_base(record=False)` preserves the old step files and inserts no boundary. Reproduction: save two draft edits on base A; accept/reset to B; reset to the retained A closure after a later accepted restore. Without any new unsent edit, `undo()` succeeds and restores the intermediate old A draft. This passes the new comparison even though those steps precede the accepted transition. Runtime restore/inverse can reuse a retained revision while recording a new publication: `timeline/commit.py:306–319` explicitly reuses revision IDs; Runtime's restore retains that closure. This is not hypothetical hash collision or an illicit modification of step files. The review probe uses mocked exact head reads/reset, not real HTTP restore. The same predicate in `timeline_sheet.py:630,649` cannot distinguish such generations either. Invalidate consumed stacks across acknowledged publication/reset boundaries; a revision-only comparison is insufficient. Keep newly authored unsent intent reversible.

2. **P2 — Successful publication followed by failed head reread leaves published steps locally undoable.** Reviewed `checkout.py:272–279`, existing `publish.py:76–93`. Reproduction calls public `Checkout.publish()` with successful publication and an injected failure only in the subsequent head reread. Publication returns its new head, `_reset_base` notes the failure and leaves the old base and old snapshots in place; `undo()` then succeeds without a publication ID. Loading the draft again cannot discover a durable boundary because none was written. The warning does not make these now-published snapshots unsent intent. The reset-write failure path has the same stale-base fallback. Record/invalidate the consumed local history when acceptance is known, even when refreshing the detached file fails; do not require an available renderer. This finding does not propose blocking independent unsent drafts merely because a peer advanced the Runtime head.

3. **P2, inherited recovery follow-up — Failed draft write consumes undo sources before committing the restore.** Reviewed `checkout.py:287–292`. Inject failure in `Path.write_text` only for the target draft after two saved edits, then call `undo(2)`. The draft bytes remain unchanged but both original history files have been removed. The reverse stack contains the later states, not the earliest source state; subsequent retry cannot recover the original undo operation. A partial write or process death can also expose a torn target because this path uses an in-place write instead of save's temporary-file replacement. The file lock does not address this ordering. Stage/replace the restored draft before retiring its recovery sources, with a recoverable stack transition. This is pre-existing, not a new regression from consolidation.

Baseline comparison: the same four review probes on `c456b328` give **4 failed**; candidate gives **3 failed, 1 passed**. The newly passing positive proves that many-step undo stops at a genuinely different base and that the new unsent edit still round-trips. Thus findings 1–3 are demonstrated residual holes, not attributed as newly introduced bugs. Findings 1–2 prevent certifying the stated boundary guarantee; finding 3 is a separate inherited recovery follow-up.

## What passes review

- `Checkout.undo(publications=...)` and `redo(publications=...)` both call `TimelineSession.undo`, which submits `timeline.inverse` through Runtime's guarded commit path. No local snapshot is used to choose the accepted result. Redo correctly names the **undo publication**. Detached checkout bytes remain unchanged.
- In independent positive probes, both undo and redo survive an accepted-but-lost acknowledgement plus handle reload: persisted flight body and key are exactly reused, accepted state is correct, and pending/flight clear after acknowledgement. The original sync tests also exercise concurrency, refusals, identity and retry fencing.
- CLI `redo --publication` uses the accepted undo dispatch, preserving a disjoint edit. Commit options require publication selection; draft/step options cannot be combined with publication undo/redo. Dry run/key/JSON handling is inherited from the native dispatcher. No JSON/whole-candidate fallback was added to these entrypoints.
- Sheet retained-basis lookup uses Runtime history and `Checkout.open(..., revision_id=row["revision_id"])`; it does not select the current shot/internal heads. Existing `store.fetch_bundle` and pinned closure reads retain revision references. The real-service test compares the entire recovered document with the original, including provenance/pins. Lookup returns a detached merge basis; it does not publish or restore accepted history. A distinct media-head-rollover case was not independently added.
- Renderer-off acceptance/readback/inverse is covered by the existing M1 tripwire and new real-service test. The tripwire blocks scene imports/evaluation; this is not a claim that every renderer process on the machine was shut down.
- Existing test expectations are unchanged: the diff adds tests, with no removed assertions, skips, xfails or converted passing expectations. The broad targeted positive set below passes.

## Remaining authority and scope

AG01/AG03/WC7/WC8 must remain open. These are documented, pre-existing migration work, not independent reasons to reject the native entrypoints:

- `timeline/publish.py:27,77–82,108–117` and `store.publish_bundle` still publish whole candidates, perform client-side merge/CAS, reset drafts and append local `publish` journal records. This accepted-publication bookkeeping/reset is the remaining actor relevant to findings 1–2.
- `Checkout.log` (reviewed checkout.py:436) and `packs/timeline/cli_log.py:39–73` still serve local journal records, including publication-labelled records. They are not a complete Runtime acceptance history. Native publication undo does not consult them.
- `timeline_sheet.py` still merges/applies detached documents directly; CLI `_cmd_apply` does not pass its available client, so CLI cannot use the new retained-basis fallback. This limitation is disclosed by the worker and is not a complete sheet migration.
- `Checkout._merge_writer`, `store.three_way`, narration publication and the other sheet/checkout producers remain. Removing them requires preserving their current positive behaviors through command producers; this review does not certify their retirement.

No ledger changes, product edits, dependency changes, pushes or integration-tree edits were made.

## Exact validation

Used private `git archive` copies under the review worker directory, never checked out another branch. `candidate` was extracted from `88dd38f1`; `baseline` from `c456b328`. Both archives were removed after validation. Commands below ran with the indicated archive as cwd.

Candidate:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/sdk/test_timeline_checkout_history.py tests/sdk/test_timeline_checkout.py tests/sdk/test_timeline_sheet.py tests/sdk/test_timeline_sync.py tests/sdk/test_timeline_sync_native.py tests/sdk/test_timeline_transaction.py tests/sdk/test_timeline_journal.py tests/packs/timeline/test_cli_commit_move.py tests/packs/timeline/test_cli_edit_flags.py tests/packs/timeline/test_verbs_working_copy.py tests/sdk/test_undo_a1_legacy_open.py tests/packs/timeline/test_cli_parity.py tests/sdk/test_timeline_checkout_facade.py
```

**375 passed, 17 deselected, 4 existing Pillow warnings, 23.43s.** Integration/lane deselections are not green claims.

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider ../test_review_publication_retry.py
```

**2 passed, 1.55s**: parameterized undo/redo lost-ACK identity probes.

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider ../test_review_boundaries.py
```

Candidate: **3 failed, 1 passed, 0.93s**. Baseline: **4 failed, 0.55s**. Failures correspond exactly to findings 1–3; baseline additionally crosses the distinct-base boundary. Review-only probe sources are retained under `workers/agt-review-local-history/`; no product test was changed.

Central HTTP verification (only the service launched sockets):

```sh
$ORCH/bin/request-test agt-review-local-history targeted --files test_review_local_history_service.py
$ORCH/bin/wait-test agt-review-local-history-targeted-1020093902-2453 1
```

**PASS, outer wrapper 1 passed, 38.81s, exit 0.** Its exact child command, run in the candidate archive:

```sh
ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider -m integration tests/editing_conformance/test_commit_runtime_m1.py tests/sdk/test_timeline_checkout_history_runtime.py
```

The wrapper asserts the child exits zero; passing child stdout is captured by outer pytest, so the fresh service summary counts the wrapper, not three individual cases. The existing worker service result `agt-m2-local-history-cut-commit-integration-1020092855-26871` was also inspected: explicitly **3 passed, 22.14s**, source tree `45bf98980f1ab2386f37d6f5302e2612bc6bce5d`. The new module selects the locked Runtime `94114269d1ce23ab3224d7eca5a85138ce2b5fed` using the normal helper at collection; these results do not qualify the currently drifting Runtime/client integration pair.

Initial review-service request `agt-review-local-history-targeted-1020093804-10420` was rejected before running because absolute test paths are disallowed. The corrected request used a temporary relative-path wrapper in this assigned worktree; it is removed, with its source retained in the worker directory. No full suite was requested or run. No make check/lint/typecheck gate was run for this read-only review. `git diff --check c456b328 tl/agt-m2-local-history-cut`: **exit 0**.

Next: retain the native entrypoint work, close the two boundary holes with positive regression coverage for new unsent edits, address the inherited write-failure recovery separately, and continue the documented writer/journal migration. Do not mark AG01/AG03/WC7/WC8 deleted on this evidence.
