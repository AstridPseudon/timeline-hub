`tl/agt-m2-occurrence-delete-sync` is now just the occurrence-delete delta on top of current `tl/integration` (`d1c56c6f`). The targeted suite passes with one behaviour change to flag: ordinary replay no longer refuses an equal-value ABA write below an occurrence. I wrote `commit-msg` and created `DONE`. Nothing is committed or pushed.

**Net diff vs integration** (tracked files, new fixture files not counted): 12 files changed, about 5.1k insertions, and it is small apart from one generated golden:

| File | Lines |
|---|---|
| `recipe_m2_occurrence_delete.json` golden | ~4.5k |
| New tests (`test_recipe_occurrence_delete.py`, `test_timeline_occurrence_delete_provider.py`) | ~390 |
| Source (`edit-command.schema.json`, `_root_inverse.py`, `inverse.py`, `commit.py`, `_command_state.py`, `commands.py`, `native_occurrence_delete.py`) | ~230 |

- `git diff` shows the `recipe_m2_clip_set_element` fixture and test as deletions only because those files are untracked in this worktree. They are integration's own files (see "Merge" below).
- `artifacts.json` and `cli-surface.json` were regenerated with `scripts/artifact_manifest.py` and `scripts/gen_cli_surface.py`; neither differs from integration.

**Merge**
- `merge-forward` brought in integration `408f3ba3` and left three conflicts: `edit-command.schema.json`, `_command_state.py` and `commands.py`.
- In `edit-command.schema.json`, I kept integration's `occurrence.duplicate` entry and added an `occurrence.delete` branch and an `OccurrenceDeleteArgs` definition next to it.
- In `commands.py`, both `occurrence.delete` and `occurrence.duplicate` are registered, with a single shared `OCCURRENCE_INTENT` import.
- In `_command_state.py`, I took integration's `get` for the shot payload.
- Integration then advanced to `d1c56c6f` (clip-set-element) while I was working. I applied that increment with `git apply` of `git diff 408f3ba3 d1c56c6f` (it applied cleanly) instead of re-merging, so the commit has no second merge parent.
- I removed `notes/report.md`, a draft worker note that doesn't belong in the repo.

**Test result:** `bin/request-test agt-m2-occurrence-delete-sync targeted --files "tests/editing_conformance tests/timeline tests/test_artifact_manifest.py tests/reshape/test_repo_hygiene.py"` gave 1762 passed, 4 skipped, 137 deselected, 6 xfailed, 173 subtests passed, with no failures.

The first run on the 408f3ba3 merge had 4 failures, in two groups:
- **Equal-value ABA replay (3 failures):** integration's `rebase.replay` is now identity-only for ordinary commands. A same-value rewrite of `shot_id`, a clip `asset` or the shot payload below an occurrence therefore no longer blocks replay. I kept the original expectation, moved it into a separate `@pytest.mark.xfail(strict=True)` test (`test_equal_state_and_aba_publication_history_refuses_replay`), and left the inverse refusal as a normal test; I checked it still refuses.
- **Golden fixture (1 failure):** integration no longer strips `internal_timeline_revision_id` from the shot payload read, so I regenerated the delete golden. The fixture changed by 3 lines, all adding that field.

**Decision for you:** restoring the strict replay refusal for `occurrence.delete` would need a per-op rule in `replay`, which I did not add because it overrides integration's replay policy. I think identity-only is acceptable for delete, since the value guards still run at execution, but I haven't confirmed that.

The 6 xfails are the 3 new ones plus 3 that were already there; I didn't touch those. The App test `useClipEditing.test.ts:261` was not run, since this was an Agent-only task.
