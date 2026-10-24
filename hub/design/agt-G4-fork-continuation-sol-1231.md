**BLOCKED: execution continuity is fixed; publication still fails during reservation replay.**

Changed `_command_state.py` to authenticate fork item IDs through existing native `_CopiedShot` provenance. Added one focused parametrized test. Original tests remain unchanged.

The production caller now passes command execution, then fails in `commit.py::_check_reservations.scan`: replaying the recorded birth loses `_CopiedShot` provenance. That file is outside ownership. The [exact unapplied companion hunk](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-G4-fork-continuation-sol-1231/evidence/unapplied-reservation-fork.patch) passes `git apply --check`; its behavior is untested.

Using venv-agent with Runtime `becfe6db…`:

- `python -m pytest -q tests/timeline/test_authoring_shared_alias_commit.py tests/timeline/test_authoring_semantic_continuation.py -k 'not duplicate'` — **4 failed, 19 passed**, both before and after; failures moved to reservation replay.
- `python -m pytest -q tests/timeline/test_native_fork_item_continuation.py` — **8 passed**, including seven forgery negatives.
- `python -m pytest -q tests/editing_conformance/test_occurrence_fork_source_baseline.py tests/editing_conformance/test_recipe_occurrence_duplicate.py` — **79 passed**, one integration test deselected by default configuration.
- Scoped Ruff, mypy, vendor lock, artifact manifest and diff checks — **PASS**.

[Exact commands, intermediate results and XML locations](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-G4-fork-continuation-sol-1231/evidence/commands.txt) are saved. Commit message and `BLOCKED` marker are written.

Next: assign the companion hunk to the `commit.py` owner and rerun publication acceptance. **Do not merge this as completed G4 qualification.**