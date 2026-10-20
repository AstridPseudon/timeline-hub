Fixed the P2 recovery window in `checkout.py` and local store helpers. A bounded transition marker enables locked recovery before load, save, or undo/redo. File identity preserves unchanged-value/ABA cases; the approved publication fences remain intact.

Added 42 permanent recovery cases, including both original probes. Exact final focused command:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/sdk/test_timeline_checkout_restore_recovery.py tests/sdk/test_timeline_checkout_history_boundaries.py tests/sdk/test_timeline_checkout_history.py tests/sdk/test_timeline_checkout.py tests/sdk/test_timeline_sheet.py tests/sdk/test_timeline_sync.py tests/sdk/test_timeline_sync_native.py tests/sdk/test_timeline_transaction.py tests/sdk/test_timeline_journal.py tests/packs/timeline/test_cli_commit_move.py tests/packs/timeline/test_cli_edit_flags.py tests/packs/timeline/test_verbs_working_copy.py tests/sdk/test_undo_a1_legacy_open.py tests/packs/timeline/test_cli_parity.py tests/sdk/test_timeline_checkout_facade.py tests/sdk/test_timeline_checkout_publication_retry.py
```

**428 passed, 17 deselected, 4 warnings.**

The central service ran:

```sh
env ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -m integration tests/editing_conformance/test_commit_runtime_m1.py tests/sdk/test_timeline_checkout_history_runtime.py
```

**4 passed**, retaining renderer tripwires. This qualifies the locked Runtime history pair, not current drifting integration.

`git diff --check` and new-test Ruff pass. Product Ruff retains three verified baseline diagnostics. No full suite ran.

No blockers. AG01/AG03/WC7/WC8 remain open. Recommend reviewing and narrow-porting the three changed paths.

[Detailed report and exact evidence](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-history-crash-reconcile/notes/report.md). `commit-msg` and `DONE` are written.