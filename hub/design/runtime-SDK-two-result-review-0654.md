## F-SDK-three-originals result review

- Exact result: **FAIL** — both assigned selectors fail before scenario actions.
- No-weakening review: **PASS** — original bodies, assertions, predicates, and fixtures were unchanged.

Command executed by prior worker:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" \
ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime \
/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider \
'tests/sdk/test_timeline_persistence.py::test_restart_a_fresh_process_sees_every_edit_and_the_undo_history' \
'tests/sdk/test_timeline_persistence.py::test_two_writers_in_separate_processes_merge_different_clips_and_refuse_the_same_param' \
--junitxml=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-F-SDK-two-first-return-0649/evidence/sdk-persistence-two.xml
```

Result: **2 failed in 1.92s**. Both fail at initial `draft` with:

```text
AttributeError: '_FakeTimelines' object has no attribute 'history'
```

Confirmed path: `Checkout.draft()` → `store.fetch_bundle()` → `c.timelines.history(...)` at `astrid/sdk/timeline/store.py:466`. No scenario action ran.

The exact test file hash, body/function hashes, and predicate hashes match base `0b4255fd8a1c20b089093cb2508394e896f54a96`. Source-mode imports resolve to the worker checkout; Runtime is only supplied through `/home/user/work/runtime`. Worktree is clean; `git diff --check` passes.

The earlier `atomic_scope_changed` report was misattributed: it belongs to the separate stale-head publication original `test_publish_after_a_restart_merges_other_clips_onto_the_moved_head`, through `_commit_patch.py:924`; the assigned two-writer selector uses local file-backed `Checkout.save()` and does not reach that path.

Smallest faithful seam: Agent’s `_FakeTimelines` fixture needs a `history(..., cursor, limit)` response exposing `.ok` and `data["head"]` with exact revision/publication IDs, plus `open_bundle(..., publication_id=...)` support. Current owner is Agent test/fixture maintenance and qualification/count; no production defect or Runtime ownership is inferred.

No source, test, fixture, product, or schema changes made. Required commit message and `DONE` marker created.