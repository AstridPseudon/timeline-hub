`occurrence.duplicate` v1 is implemented as an independent copy with explicit reserved IDs. Targeted tests pass, with one strict xfail left open on a real App blocker. The commit message and report are written. Cleanup of caches and scratch scripts was denied by the permission system, so those are still on disk.

## What changed

- `astrid/sdk/timeline/native_occurrence_duplicate.py` (new, 54 lines): the handler and `capture_occurrence_duplicate(bundle, owner, occurrence_id, shot_id)`.
- `astrid/core/timeline/schema/edit-command.schema.json`: closed `OccurrenceDuplicateArgs` plus one dispatch entry.
- `astrid/sdk/timeline/commands.py`: registration.
- `astrid/sdk/timeline/_command_state.py`: `occurrence:<id>/shot` with path `["payload"]` returns the source-published payload. This is the same hunk as `tl/agt-m2-occurrence-delete`.
- `tests/editing_conformance/test_recipe_occurrence_duplicate.py` (new) and `fixtures/recipe_m2_occurrence_duplicate.json` (golden).

About 118 net product lines, under the 200 target.

The old worktree had no WIP and no commits beyond base, so I started from base.

## Decisions

- **Independent copy, not source-bound reuse.** App's `handleDuplicateDocumentShotGroup` is the only live canonical duplicate caller, and it calls `duplicateIndependentShot`. `duplicateLinkedOccurrence` has no non-test caller.
- **Two creates only.** The op creates `shot:<shot_id>` and `occurrence:<occurrence_id>`. It writes no source rows and no parent array.
- **Tracks and clips need no reservation.** They live in the copied internal timeline, which is scoped to the new shot.
- **Inverse needed no correction.** Undo and redo were exact on the first run, unlike the delete branch.

## Tests

All run with `/home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider`:

| Command | Result |
|---|---|
| `tests/editing_conformance/test_recipe_occurrence_duplicate.py` | 32 passed, 1 strict xfail |
| `tests/editing_conformance tests/timeline` | 1642 passed, 4 skipped, exit 0 |
| `tests/sdk -k timeline` | 935 passed, 2 skipped |

Gates:
- `ruff` on changed files: clean.
- `mypy` on the new module alone: clean.
- Structure, import-cycles, and doc-refs gates: pass.
- `compare_mypy_baseline` fails before checking, on yaml stubs and numpy stubs. This is environmental, not from this change, so it is unverified.

No full suite was requested.

## Blocker

App writes `stable_deep_link` and `output_identity` onto each occurrence row, and both embed the occurrence ID. The op copies them verbatim, so the copy carries the source's values. The Agent cannot derive replacements without inventing authority. This is pinned as the strict xfail `test_copy_does_not_carry_source_derived_identity_fields`. App needs to supply reserved replacements, or the contract needs an args extension. Decision needed before adoption.

## Other decisions for you

- **Ordinary-replay ABA.** Equal-value `shot_id` and shot-payload ABA is admitted on ordinary replay, because replay checks values on the final head. Inverse refuses all source ABA. If M2 requires ordinary replay to refuse it too, that means changing the engine's `identities_only` policy.
- **Commit attribution.** Per the orchestrator rule, I left out the Co-Authored-By model line and kept only the `Claude-Session` trailer.

## Not done

- **Cleanup.** My `rm` commands were denied. The worktree still has `.mypy_cache`, `.ruff_cache`, and `__pycache__` directories, which are gitignored. Four scratch scripts are still in the scratchpad.
- **Runtime schema pins.** `cli-surface.json`, `runtime.lock.json`, and `astrid_runtime_client` are not regenerated. That is for normal Runtime generation.

## Files written

- Report: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-occurrence-duplicate-b/notes/report.md`
- Commit message: `.../workers/agt-m2-occurrence-duplicate-b/commit-msg` and `commit-msg.txt`
- Design doc: `.../scratchpad/orch/design/m2-occurrence-duplicate.md`
- App INBOX note appended: `.../scratchpad/orch/managers/app/INBOX.md`
