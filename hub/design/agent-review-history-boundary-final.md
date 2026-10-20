# Agent history boundary final review

**REQUEST CHANGES: one concrete P2 remains in the local restore crash window.** The acknowledged-publication boundary fixes and native publication undo/redo pass review. This finding concerns the requested restore recovery guarantee, not the separately unmigrated AG01/AG03/WC7–8 writers.

Reviewed `tl/agt-m2-history-boundary-finish` at `3f1ac9828a75d8c4507ac5b2ad17eb9970c25b1e` (tree `932e2b9591a4a13830e23236d15afb6b2a7097b7`), its exact successor diff from `88dd38f1`, the predecessor diff from `c456b328`, prior review `design/agent-review-local-history-current.md`, PLAN, source tests, worker log and central result metadata. Current integration port target was `e2ad59584addc892f1a6dd9fd644c75f80a2e28f`; its worktree was clean when checked.

**P2: draft replacement commits before reverse-stack recovery becomes visible.** In `astrid/sdk/timeline/checkout.py:308`, the target is replaced; reverse steps are promoted only at line 317, outside the exception handler. Injecting `OSError` at the first reverse promotion leaves the target changed, original source files byte-for-byte intact, and both reverse states present only as hidden `.*.tmp` files. A process death at the same point leaves the same on-disk state. `Checkout.load` does not reconcile these files, and `_restore_draft` reads only `*.json`. Reopening and applying the opposite operation therefore raises “no unsent draft edit” instead of restoring the pre-operation draft. This reproduces for both undo and redo.

For undo, save x=40 then x=99; call `undo(2)` with `os.replace` failing only when its destination is inside the redo folder. The target has moved to the original state. After `Checkout.load`, `redo(2)` is unavailable. For redo, first complete `undo(2)`, then interrupt `redo(2)` at promotion into history; reopening exposes no undo. The probe asserts the original source bytes and two staged reverse files still exist before checking public recovery, so it does not mistake a target-write failure for this later window.

The reverse state is initially recoverable by manual inspection of hidden files; it has not already vanished. However, the existing helper is not a recovery protocol: `store._discard_half_written` simply deletes temporary history files, and the next changed save deletes the redo folder. No public operation reconciles an interrupted restore first. The candidate's four write/replace fault cases stop at temporary-target writing or replacement (`test_timeline_checkout_history_boundaries.py:119–127`); they never reach this post-replacement promotion. Early write failures are fixed, but the requested crash-window handling is incomplete.

Recommended correction: finish or safely reconcile the local staged stack transition using the existing local store/locking helpers before exposing the stacks or discarding their temporary files, and add normal post-replacement interruption regressions for both directions. Keep this bounded to local draft storage; no accepted-history journal, coordinator, new contract, or renderer dependency is needed. I made no source change.

**What is verified.** `_retire_draft_history` removes both consumed stacks and the in-memory journal/export cache. It runs immediately after publication returns successfully, before narration/transcript/head-refresh work, and at the start of `_reset_base`. Consequently the consumed steps cannot reopen when Runtime returns to retained revision A with a different publication generation. Failed head reads and failed reset saves leave consumed steps fenced across reload. `_reset_base` no longer reinstates the old edit journal on a failed write. A newly saved unsent edit still round-trips after these paths. The nine boundary cases and two independent lost-ACK probes pass in this review.

Native `undo(publications=...)` and `redo(publications=...)` still dispatch to `TimelineSession.undo`, constructing `timeline.inverse` and using the durable outbox. No snapshot determines an accepted result. The lost-ACK probes compare the retry body and key with the persisted flight, reload the checkout handle, check accepted state, leave detached bytes unchanged, and assert pending/flight clear after acknowledgement. The strict inverse/provider/ancestry code and command contracts are unchanged by both commits. Existing real-service M1 cases retain the disjoint-edit undo, touched-basis conflict, restart and exact-retry assertions.

Sheet retained-basis lookup still uses Runtime history revision IDs and `Checkout.open(revision_id=...)`, hence `open_bundle`'s complete pinned closure. Its service assertion compares the entire recovered document with the original, including provenance and pins; it never selects today's shot/internal heads. This is read-side basis recovery, not accepted snapshot rewind. There is no separately added media-head-rollover fixture, so I do not claim one.

Across the combined test diff, no pre-existing test lines or positive assertions were removed or changed; additions only. No skip/xfail or contract loosening was introduced. The initial failed service attempt changed only the new restore test's invocation to the existing generated restore endpoint with expected revision/publication guards, preserving its positive assertions.

**Exact validation performed by this review.** Cwd for direct tests was `/home/user/work/wt/agt-review-history-boundary-final`; `ORCH` below denotes the scratchpad/orch path containing this report. Review-only probe source is `workers/agt-review-history-boundary-final/test_review_restore_interruption.py` and its final stdout is `workers/agt-review-history-boundary-final/notes/restore-interruption.log`.

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/sdk/test_timeline_checkout_history_boundaries.py tests/sdk/test_timeline_checkout_publication_retry.py $ORCH/workers/agt-review-history-boundary-final/test_review_restore_interruption.py
```

First probe revision (undo only): **1 failed, 11 passed in 2.79s**, exit 1. Final parameterized probe (undo and redo): **2 failed, 11 passed in 3.44s**, exit 1. Both failures are the post-replacement inverse-recovery check described above. All nine shipped boundary/fault cases and both lost-ACK cases pass. The second run added the symmetric redo case; no product or original test was edited.

```sh
git diff --check c456b328 3f1ac982
git diff --check 88dd38f1 3f1ac982
```

Both **exit 0**. Read-only inspection used `git show`, `git diff`, `rg`, and the central result files; no checkout or branch mutation.

**Existing evidence inspected, not rerun.** Worker log contains the actual command and pytest summary (not only its final report):

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/sdk/test_timeline_checkout_history_boundaries.py tests/sdk/test_timeline_checkout_history.py tests/sdk/test_timeline_checkout.py tests/sdk/test_timeline_sheet.py tests/sdk/test_timeline_sync.py tests/sdk/test_timeline_sync_native.py tests/sdk/test_timeline_transaction.py tests/sdk/test_timeline_journal.py tests/packs/timeline/test_cli_commit_move.py tests/packs/timeline/test_cli_edit_flags.py tests/packs/timeline/test_verbs_working_copy.py tests/sdk/test_undo_a1_legacy_open.py tests/packs/timeline/test_cli_parity.py tests/sdk/test_timeline_checkout_facade.py tests/sdk/test_timeline_checkout_publication_retry.py
```

**386 passed, 17 deselected, 4 warnings in 43.29s.** This preserves the original 375 positives and adds nine boundary/fault cases plus two lost-ACK cases. The existing lane deselections are not passing integration evidence. The broad run preceded the final correction to the new integration-only restore invocation; product code and its selected direct tests did not change afterward.

Central provider evidence:

```sh
$ORCH/bin/request-test agt-m2-history-boundary-finish commit-integration --files tests/sdk/test_timeline_checkout_history_runtime.py
$ORCH/bin/wait-test agt-m2-history-boundary-finish-commit-integration-1020095840-26533 1
```

Its recorded child command:

```sh
env ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -m integration tests/editing_conformance/test_commit_runtime_m1.py tests/sdk/test_timeline_checkout_history_runtime.py
```

**4 passed in 30.16s, exit 0** (service elapsed 37s). `request`, `summary`, `snap`, `ext`, `exit`, and test stdout were inspected. The snapshot tree is **exactly** the reviewed commit tree `932e2b9591a4a13830e23236d15afb6b2a7097b7`. Includes actual retained A→B→A restore with a different receipt, refusal of consumed local undo/redo after reload, new unsent round-trip, retained sheet closure, native inverse/redo, and M1 restart/lost ACK. Renderer imports/evaluation are blocked by the existing tripwire; no machine-wide renderer shutdown is claimed.

The earlier service result `agt-m2-history-boundary-finish-commit-integration-1020095654-5221` was **1 failed, 3 passed in 42.46s**, tree `cbbacf3930efc9fca61192690ddb4796fe403f5a`: the new test tried unregistered `timeline.restore` via native command ingress. Its correction uses the existing generated restore operation; no producer contract was relaxed. The final service metadata records external Runtime `c0dcd387...`, App `18becfb...`, Composition `e80c46ba...`, but the test's `use_runtime(vendored_runtime_commit())` archives Runtime **`94114269d1ce23ab3224d7eca5a85138ce2b5fed`** from `runtime.lock.json`. Therefore this qualifies that locked pair, not current drifting Runtime/client integration.

No full suite, socket/browser suite, make check, lint, or typecheck was run or requested by this review. The worker's prior Ruff exact-count baseline and mypy gates remain unqualified (Ruff count 2212 vs baseline 2220; missing YAML stubs/NumPy target-syntax problem). Shared dependencies were not touched.

**Safe port paths and conflicts against current root.** In a private temporary directory, populated only with the ten affected files from current integration `e2ad5958`, I ran `git apply --check --verbose -` with the binary diff `git diff --binary c456b328 3f1ac982 -- <the ten paths below>` as stdin: **exit 0, no conflicts or offset warnings**. The temporary copy was removed. Exact metadata/output is `workers/agt-review-history-boundary-final/notes/port-check.json`.

- `astrid/packs/timeline/cli.py`
- `astrid/sdk/timeline/checkout.py`
- `astrid/sdk/timeline/publish.py`
- `astrid/sdk/timeline_sheet.py`
- `docs/timeline-editing-guide.md`
- `tests/packs/timeline/test_cli_commit_move.py`
- `tests/sdk/test_timeline_checkout_history.py`
- `tests/sdk/test_timeline_checkout_history_boundaries.py`
- `tests/sdk/test_timeline_checkout_history_runtime.py`
- `tests/sdk/test_timeline_checkout_publication_retry.py`

The root lacks `88dd38f1`. A successor-only `88dd38f1..3f1ac982` apply check **exits 1**: checkout context depends on the predecessor and the Runtime history test file does not yet exist. Preserve both units' path-scoped changes, or use their combined diff after fixing the remaining recovery issue. Only `docs/timeline-editing-guide.md` overlaps root's changes since `c456b328`; its new accepted-history section applies cleanly alongside D07's later retime-helper removals. Preserve the root's native commands/schema, pool eligibility guards, equal-state delete positives, public Composition 0.0.12 artifacts/package locks, and viewing/audio work. None is in these ten paths except the nonconflicting guide. Do not replace whole root files or port the older branch tree wholesale. Clean patch application is not a post-port test qualification.

**Remaining scope and next step.** AG01/AG03/WC7/WC8 stay open: whole-candidate `publish_bundle`/client merge/CAS/narration publication, local publication-labelled log records, detached sheet merge/apply, CLI apply not forwarding the client, and `_merge_writer`/`three_way` are unchanged migration work. They are not reasons for this verdict. Retain the approved publication entrypoints and acknowledged-boundary correction; finish the single local restore transition issue with permanent positive recovery assertions, then narrow-port and run the applicable targeted/provider lanes. No task blocker: this read-only review is complete. No source, ledger, integration, dependency, Git metadata or refs were modified, and nothing was pushed.
