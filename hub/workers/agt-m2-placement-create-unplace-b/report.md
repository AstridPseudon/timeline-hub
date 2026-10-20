## Report: agt-m2-placement-create-unplace-b

**Outcome:** `placement.create` and `placement.unplace` are implemented as separate occurrence-owned, closed, versioned ops. The Agent-side targeted and lane tests pass. Nothing is committed; the harness commits on exit.

### Carry-over
The old worktree `/home/user/work/wt/agt-m2-placement-create-unplace` had no uncommitted WIP, no ignored files, and no commits beyond base. Nothing to carry over, so I started fresh from the brief.

### What changed
- `astrid/sdk/timeline/native_placement_commands.py`: handlers and capture exports. `placement.move` is untouched.
- `astrid/sdk/timeline/commands.py`: registers both ops.
- `astrid/sdk/timeline/commit.py`: one token. `placement.create` fetches `selected_media` like `occurrence.add-media`. Without it the provider can't verify the image pin.
- `astrid/core/timeline/schema/edit-command.schema.json`: `PlacementCreateArgs`, `PlacementUnplaceArgs`, and their branches.
- New test file and golden fixture under `tests/editing_conformance/`.
- Size: net +198 lines including schema JSON (Python about 97), under the 200 bound.

### Tests and commands
Run from the worktree with `/home/user/work/venv-agent/bin/python -m pytest -q … -p no:cacheprovider`:

| Scope | Result |
|---|---|
| Focused: new file + `test_recipe_m2_placement`, `test_recipe_occurrence_media`, `test_recipe_clip_delete`, `test_commit_runtime_occurrence_media` | 204 passed, 48 deselected |
| `tests/editing_conformance` + `test_timeline_composed_schema` + `test_timeline_commit_graph_roots` + `tests/timeline` | 1681 passed, 4 skipped, 137 deselected |
| Baseline before my change (three placement/media/delete files) | 169 passed |
| `ruff check` on changed Python | passed |

The deselections come from pytest's default lane filter in `pyproject.toml`; I didn't change it. No full suite was requested or run, and no central-service suite was used.

A `ruff format --check` on the base versions of `commands.py`, `commit.py`, and `native_placement_commands.py` already fails, so the repo doesn't enforce it. I didn't reformat.

### Decisions I made
1. **Image media only.** Video needs a source window that the App placement doesn't carry, so non-image pins refuse.
2. **`hold` is caller-supplied.** No hidden 4 s default. The App passes 4.
3. **No auto-position, pooling, collision shifting, or `keepAsPooled`.** The App's legacy behaviors are not reproduced.
4. **Exclusive owner required.** A shot shared with another occurrence refuses on every lane, as in `placement.move`.
5. **Unplace keeps the registry binding.** This matches legacy `unplaceGeneration`. The binding is guarded at its raw path, so ABA changes block replay and undo.
6. **Commit message omits the model co-author line.** Your brief says "no model names", which conflicts with the session's attribution reminder. I kept the `Claude-Session:` trailer. Please confirm.

### Findings to review
- **Undo after create → unplace → undo(unplace) is refused.** Undoing the create hits the intervening-write ABA guard, because the removal and its undo both wrote the created clip. Single-step undo and redo are exact. The Runtime/history owner should decide whether that is acceptable before App uses it as an undo stack.
- The Runtime pinned schema copy (`contract/schemas/edit-command.json`) is older and has no `occurrence.*` ops either. Runtime owns that refresh, and Runtime's port must supply `selected_media` for `placement.create`.

### Not done (by rule or denial)
- **Deletion-ledger row not written.** The ledger file is manager-owned. The proposed row is in the report.
- **Worktree cleanup denied.** My `rm` of scratch files and `__pycache__` was denied, so I didn't retry. The scratch scripts sit in the scratchpad, outside the worktree. `__pycache__` in the worktree is gitignored and won't be committed, but it is build output I was asked to leave out.

### Written paths
- Commit message: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-placement-create-unplace-b/commit-msg` (and `commit-msg.txt`)
- Report: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-placement-create-unplace-b/notes/report.md`
- Design: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/m2-placement-create-unplace.md`
- App INBOX entry appended to `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/app/INBOX.md`

### Next steps
1. Manager: decide whether single-step undo is enough for M2, or whether a multi-step rule is needed.
2. Runtime: refresh the pinned edit-command schema and provide `selected_media` for `placement.create`.
3. App: wire create/unplace only after an accepted reload/undo parity test.
