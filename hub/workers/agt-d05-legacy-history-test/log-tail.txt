## D05 replacement test: done

The new test passes, and the D05 ledger row is marked DELETED, conditional on `tl/agt-m2-delete-core-inverse` merging. No current behaviour was wrong, so no product code changed.

### What I did
- **Test added:** `tests/sdk/test_timeline_commit_provider.py::test_legacy_history_undo_and_restore_use_revisions_or_refuse_visibly`, inserted before `test_moves_do_not_scan_reservation_history`. It uses the existing `DetachedRealm` fake and the real `commit` / `inverse` / `restore` helpers.
  - It builds a legacy prefix of 10 entries, one per kind: `clip.retimed`, `clip.swapped`, `clip.text_set`, `clip.annotated`, `effect.tuned`, `theme.overridden`, `pool.asset_scored`, `arrangement.replaced`, `timeline.config_replaced`, `timeline.reverted`. Each is marked `intent="legacy_unknown"` with `records=None`, following the pattern already used in the file.
  - It asserts the kinds are members of the real `TimelineEventKind` schema literal.
  - Undo spanning the legacy prefix is refused with `history_unavailable`, and head, entries and accepted writes are unchanged.
  - Undo of a post-upgrade recorded edit succeeds through the revision path and restores the pre-edit payload.
  - Restore of the legacy revision succeeds, and the legacy rows keep their intent and `records=None`.
  - `importlib.util.find_spec("astrid.core.timeline.inverses") is None` confirms the legacy inverse code is not importable.
- **Caveat on the fixture:** the SDK never reads pre-upgrade kinds. The kinds are stored only as `receipt.command_kind` labels on the legacy rows, and the test's comment says so. I did not claim anything about how the Runtime stores them.
- **Ledger:** `design/deletion-ledger.agent.md` row D05 is now DELETED. Evidence names the new test and the three command-level tests. I corrected the ABA test's path to `tests/sdk/test_timeline_commit_provider.py`, and added `test_inverse_rebases_only_over_proven_disjoint_new_writes` at line 579. The ledger file lives in the orch scratchpad, outside the repo.
- **Commit message:** written to `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-d05-legacy-history-test/commit-msg`. I left out the `Co-Authored-By` model line because your brief said no model names. I kept the `Claude-Session` line.
- **DONE** marker created.

### Commands and results
- Baseline before my edit: `/home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/sdk/test_timeline_commit_provider.py tests/editing_conformance/test_recipe_m1_commands.py` → 134 passed.
- New test alone: `... tests/sdk/test_timeline_commit_provider.py -k legacy_history` → 3 passed (the new test plus two existing parametrized legacy-boundary tests).
- Targeted via the central service (`request-test ... targeted --files "tests/sdk/test_timeline_commit_provider.py tests/editing_conformance/test_recipe_m1_commands.py tests/sdk/test_timeline_sync.py"`) → **196 passed**, exit 0, agent tree `6a30ada3`.
- No full suite was requested.

### Not verified or left undone
- **Lint not run.** `ruff check` and `ruff format --check` were both blocked by the approval gate, so the edit has not been linted or format-checked.
- **Stray build output.** `tests/__pycache__` and other `__pycache__` directories from my test runs are still in the worktree (git-ignored). My request to remove them was denied, so I left them. They should be removed before handing off.
- **Retired self-test mapping.** The ledger's caveat about judging retired event-planner self-tests against `workers/agt-m2-review-retirements/notes/report.md` still applies. I did not re-check that mapping.
