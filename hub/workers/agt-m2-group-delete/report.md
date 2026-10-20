## agt-m2-group-delete: blocked

I did not deliver a new commit. The draft already exists, but it can't be carried onto `tl/integration`, and my worktree is dirty from a failed attempt.

**The draft is already complete on `tl/agt-m2-occurrence-delete` (commit `1d3ead87`).**
- **Contents:** a closed `occurrence.delete` v1 (args `{}`, intent `ownership: occurrence`) with a guarded inverse that restores original order.
- **Not covered:** nonempty legacy `pinnedShotGroups` is refused with `migration_needed` until the recorded migration runs.
- **Evidence:** it ships a golden fixture, recipe and provider tests, and a contract doc at `orch/design/m2-occurrence-delete.md`. Its own report says 743 tests passed. I did not re-run them.
- **Not yet proven:** there is no real Runtime or App proof for it yet.

**Why I couldn't carry it over:**
- **Base:** `tl/integration` (`4a75f68f`) has only the M1 operations (`clip.move`, `track.create`). The draft's base `a31d712d` is not an ancestor of it.
- **Missing machinery:** `clip.delete`, `root_identity`, `AcceptedRecords` and the occurrence media and placement operations aren't on integration.
- **Conflicts:** applying the diff with `git apply -3` conflicts in `edit-command.schema.json`, `_command_state.py`, `commands.py`, `commit.py` and `inverse.py`. Porting it would mean pulling in the held Bundle2 stack, about 34k lines, so I stopped.

**My worktree is dirty, and I can't clean it.** `rm` was denied by the sandbox, and `.git` is read-only to me. I did not work around the denial.
- **Restored:** the five tracked files that conflicted now have HEAD content again, but `git status` still shows them as unmerged (`UU`).
- **Leftovers:**
  - `astrid/sdk/timeline/_root_inverse.py`
  - `astrid/sdk/timeline/native_occurrence_delete.py`
  - `tests/editing_conformance/fixtures/recipe_m2_occurrence_delete.json`
  - `tests/editing_conformance/test_recipe_occurrence_delete.py`
  - `tests/sdk/test_timeline_occurrence_delete_provider.py`
  - four `astrid/sdk/timeline/*.rej` files
- **Needed from you:** please run `git reset --hard` (or `git clean -fd`) in `/home/user/work/wt/agt-m2-group-delete` before anything commits it.

**Decision for you:** either publish `tl/agt-m2-occurrence-delete` as the group-delete candidate, to be composed in the later group bundle after the M1 gate, or name a different base for me to rebuild it on. The draft's own notes recommend the first option.

I wrote the reason to `.../workers/agt-m2-group-delete/BLOCKED`. I did not write `commit-msg` or `DONE`, and I ran no tests.
