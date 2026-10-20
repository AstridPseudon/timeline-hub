# Agent history reconciliation review

**APPROVE the minimal source port. No blocking defect found in the reviewed local restore transition.** The prior P2 is reproducibly fixed, including equal-value/ABA drafts and interruption on either side of reverse promotion. This approves the bounded local recovery change and its required boundary predecessors, not closure of the remaining Timeline writer migrations.

Reviewed source `tl/agt-m2-history-crash-reconcile` **7e502fe267abe357ad7c10cf12f867cc5987d7f4**, tree **66c41e41d8fafb816913b6cca7ab41bc45dc7c19**; ancestors `88dd38f1` and `3f1ac982`; PLAN; supplied AGENTS; `design/agent-review-history-boundary-final.md`; and the original two review probes. My assigned checkout stayed at `43d567f9d972386dc4cf585fbacc3ad9afc56bdd`, clean and unmodified. No Git mutation was performed.

Integration moved during review. The private port snapshot is **73d8a237bc235aa9606b4f2a84e534aa9fa5f6b6**, tree **ce98abe7a536916b314fa5c80861083bf2fd5f4d**. Final integration checked was **86405964ecb713ad42a375f9de7960b3f9dc259b**: none of the twelve port paths changed between these commits. These are pinned observations, not a qualification of future integration changes.

## Source findings

The successor changes exactly `astrid/sdk/timeline/checkout.py`, `astrid/sdk/timeline/store.py`, and the new `tests/sdk/test_timeline_checkout_restore_recovery.py`. Product change is +73/-9 lines, 64 net; tests add 337 lines. There is one pending marker per local checkout stack move. It holds only direction, local filenames and the prepared target device/inode; it is removed on cancellation or completion. It contains no accepted revisions, publication authority, request identities, accepted-history rows, or alternate coordinator. Existing local narration/log machinery is unchanged. There is no second accepted journal.

Ordering is correct under the existing checkout lock:

1. Stage reverse states and the replacement target, then atomically install the transition marker before replacing the target.
2. Classify replacement using target file identity, preserving unchanged-value and A→B→A transitions without guessing from JSON equality.
3. After replacement, promote every reverse state before deleting any source state; remove the marker last. Already-promoted steps and already-removed sources make restart reconciliation repeatable.
4. Before replacement, reconciliation cancels staged files and preserves the original source chain. Staging exceptions remove partial files. An exception raised after a successful target replacement retains the marker and reverse states.
5. Public load reconciles before reading; save reconciles before merging, discarding temporary history, or clearing redo; undo/redo reconcile before selecting steps. `_save_locked` callers hold the same lock. The only `_reload` caller is locked restore, so `_load_locked` avoids acquiring that lock twice.

Independent probes verify actual Linux flock exclusion during reconciliation and marker staging, repeat failure during first/second recovery promotion, retry after final marker-removal failure, and both KeyboardInterrupt and real child exit immediately AFTER successful first/second reverse promotions. These supplement the permanent 42 cases, whose child-exit hooks cover preparation, target replacement, and entry into first/second promotion. Original sources remain byte-identical until reverse promotion is complete; recovery through normal reload and the public inverse restores the exact prior file bytes.

Publication fences from `3f1ac982` remain in place: known acceptance retires consumed stacks and in-memory journal/exported basis before narration or head refresh, and `_reset_base` retires before failed reads/writes can retain a stale base. The new code also retires the pending local marker, preventing later reconciliation from recreating consumed stacks. Existing positive tests cover retained revision A→B→A, failed reread/reset save, and subsequent new unsent undo/redo. Native `publications=` undo/redo still calls `TimelineSession.undo` through the existing guarded inverse and durable outbox. Lost ACK probes compare exact persisted body/key on retry, accepted content, untouched detached bytes, and cleared pending/flight after acknowledgement. No inverse/provider/ancestry, command contract, or accepted-history implementation was changed.

The permanent original probe function is AST-identical to the supplied review probe. Across all combined test changes since `c456b328`, every original test line remains: additions only, no skip/xfail, refusal rewrite, or weakened assertion.

## Direct validation and exact commands

All test code ran from private `git archive` snapshots in my worker directory using shared dependencies read-only. No checkout, branch mutation, editable install, shared cache, localhost service, or browser was used. In the commands below:

```sh
ORCH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
W=$ORCH/workers/agt-review-history-reconcile-current
```

For each `TREE` in `$W/source` and `$W/integration-port`, cwd was that directory:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$TREE /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/sdk/test_timeline_checkout_restore_recovery.py tests/sdk/test_timeline_checkout_history_boundaries.py tests/sdk/test_timeline_checkout_publication_retry.py tests/sdk/test_timeline_checkout_history.py tests/sdk/test_timeline_checkout.py tests/sdk/test_timeline_transaction.py tests/sdk/test_timeline_journal.py $W/test_review_restore_interruption.py
```

- Exact source: **184 passed, 17 deselected, 4 warnings in 9.66s; exit 0**.
- Private integration port: **184 passed, 17 deselected, 4 warnings in 7.57s; exit 0**.

These include all 42 permanent recovery cases, both unchanged original probes, publication boundaries/retries, ordinary local history, checkout, transactions and journal neighbours. Deselections follow the existing lane; they are not integration passes. Four warnings are the existing Pillow Image.getdata deprecation in the real-ffmpeg frame-selection test.

Final guard command, again in each TREE:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$TREE /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/sdk/test_timeline_checkout_restore_recovery.py $W/test_review_reconcile_guards.py
```

- Exact source: **60 passed in 8.16s; exit 0**.
- Private integration port: **60 passed in 5.47s; exit 0**.

This is 42 permanent cases plus 18 independent review cases. The earlier version of this command, before the eight post-successful-promotion cases were added, passed **52 in 2.68s** on source and **52 in 3.34s** on port. No product changes followed either run.

To verify the original defect, cwd `$W/ancestor-3f1ac982`:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$W/ancestor-3f1ac982 /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider $W/test_review_restore_interruption.py
```

**2 failed in 0.50s; exit 1**, as expected: public inverse after reopening reports no unsent draft edit for both undo and redo. The preceding source-byte, two-hidden-step and changed-target assertions all pass. This is deliberately recorded as a failing ancestor reproduction, not green evidence.

Static checks:

```sh
git diff --check c456b328 tl/agt-m2-history-crash-reconcile
git diff --check 3f1ac982 tl/agt-m2-history-crash-reconcile
```

Both **exit 0**. In source:

```sh
/home/user/work/venv-agent/bin/ruff check --no-cache --output-format concise astrid/sdk/timeline/checkout.py astrid/sdk/timeline/store.py tests/sdk/test_timeline_checkout_restore_recovery.py
```

**Exit 1, exactly three inherited diagnostics**: checkout I001, store I001 and store E731. Same command on the ancestor checkout/store files, omitting the absent new test file, reproduces the same three diagnostics (exit 1; E731 line offset changes). No diagnostic is in the new test. No whole-repo lint/typecheck/make-check result is claimed.

Machine-readable commands, cwd, env, exits and stdout are retained in `notes/targeted-results.json`, `notes/guard-results-final.json`, `notes/guard-results.json`, and `notes/static-checks.json`. Full pytest logs are beside them. Original and independent review probes are retained in this worker directory. The temporary source snapshots were removed after validation.

## Existing actual-Runtime evidence inspected, not rerun

Inspected `summary`, `snap`, and `log.txt` of `$ORCH/tests/agt-m2-history-crash-reconcile-commit-integration-1020103038-1379`. Snapshot tree is exactly **66c41e41d8fafb816913b6cca7ab41bc45dc7c19**, matching reviewed source. Recorded child command:

```sh
env ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -m integration tests/editing_conformance/test_commit_runtime_m1.py tests/sdk/test_timeline_checkout_history_runtime.py
```

**4 passed in 34.29s, service exit 0 (45s elapsed)**. Source inspection confirms renderer import/evaluation tripwires, M1 restart/exact retry, guarded publication inverse/redo, retained A→B→A with distinct publication identity, consumed local stack refusal, new local round-trip, and entire retained sheet basis equality including provenance/pins. The module selects `use_runtime(vendored_runtime_commit())`: **Runtime 94114269d1ce23ab3224d7eca5a85138ce2b5fed** from runtime.lock.json. This is prior evidence for that exact locked source pair, not a fresh service run or qualification of current drifting Runtime integration. No machine-wide renderer shutdown or independent media-head-rollover fixture is claimed.

## Safe port and next step

Integration lacks the predecessor boundary edits. In a private complete archive of integration, the combined binary diff **c456b328..7e502fe2**, restricted to its twelve changed paths, passes `git apply --check --verbose -` **exit 0, no conflicts or offset warnings**, then `git apply -` **exit 0**. Actual integration was untouched. Exact patch and apply metadata remain in `notes/combined-source.patch` and `notes/snapshots.json`. This private applied tree is what the second set of targeted runs tested.

Port these path-scoped changes together; do not replace source branch trees or whole current files:

- astrid/packs/timeline/cli.py
- astrid/sdk/timeline/checkout.py
- astrid/sdk/timeline/publish.py
- astrid/sdk/timeline/store.py
- astrid/sdk/timeline_sheet.py
- docs/timeline-editing-guide.md
- tests/packs/timeline/test_cli_commit_move.py
- tests/sdk/test_timeline_checkout_history.py
- tests/sdk/test_timeline_checkout_history_boundaries.py
- tests/sdk/test_timeline_checkout_history_runtime.py
- tests/sdk/test_timeline_checkout_publication_retry.py
- tests/sdk/test_timeline_checkout_restore_recovery.py

Only the product guide overlaps integration changes since c456b328, and its patch applies cleanly alongside them. Preserve all integration-native command/schema, bridge, timing, viewing and dependency work. If the orchestrator first ports the two predecessor units, the successor-only change is the three paths described above. Qualification after the actual port remains the integrating owner's responsibility.

No decisions were changed, no blocker remains, and no repository/process documentation was added. AG01/AG03/WC7/WC8 remain open: whole-candidate publication/client merge/CAS/narration, local publication-labelled log records, detached sheet merge/apply, CLI apply client forwarding, and local `_merge_writer`/`three_way` are separate migration work. This review does not declare them complete.

No full/full* suite was requested or run. No new central service request was needed. Power-loss durability/fsync, macOS, filesystem transplantation, external replacement outside the lock, and recovery of pre-marker artifacts left by an older binary are unverified. Retirement I/O failure/process-death during the acceptance fence itself was not fault-injected; tested publication failures are downstream head-read/reset-write failures. Shared dependency folders, integration and other workers' worktrees, refs and Git metadata were not modified. Recommend the minimal combined source port followed by the applicable targeted/locked-provider checks; no new accepted-history framework is warranted.
