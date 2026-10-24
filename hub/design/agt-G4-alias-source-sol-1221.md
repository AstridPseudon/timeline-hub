**BLOCKED: the required repair exceeds file ownership.** Added [focused positive regressions](tests/timeline/test_authoring_semantic_continuation.py); no production changes retained.

The fork planner experiment emitted an identical request. Production execution still fails at `commands.execute → _doc_patch.patch → Recording.read → State.shot_item_map`. Fixing that needs authenticated continuation for engine-created shots outside `authoring_commit.py`; the strict guard remains unchanged.

The duplicate seam is `timeline_editing.py:564–583`: `duplicate_authoring_shot()` delegates to detached mutation without retaining an explicit source-occurrence command reservation. That must connect to `capture_occurrence_duplicate()` before the authoring membership guard.

Using venv-agent with `PYTHONPATH="$PWD:/home/user/work/runtime"`, `ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime`, Runtime `becfe6db…`:

- `python -m pytest -q tests/timeline/test_authoring_shared_alias_commit.py tests/timeline/test_authoring_feedback_residual.py tests/timeline/test_authoring_publication_migrations.py` — **3 failed, 39 passed**.
- Same command plus `tests/timeline/test_authoring_semantic_continuation.py` — **6 failed, 40 passed**. Three new reproductions remain RED; the reopened-boundary reference succeeds.
- `python -m pytest -q tests/editing_conformance/test_occurrence_fork_source_baseline.py tests/editing_conformance/test_recipe_occurrence_duplicate.py` — **79 passed, 1 integration test deselected by default lane configuration**.
- Scoped `python -m ruff check` and `python -m mypy --cache-dir "$TMPDIR/mypy-cache"` on both owned files — **PASS**.
- `python scripts/vendor_lock.py check runtime.lock.json`, `python scripts/artifact_manifest.py --check`, `git diff --check` — **PASS**. Requested vendor `--check` spelling is unsupported.

Original test hashes and production source are unchanged. Durable XML/logs, task-named commit message and `BLOCKED` marker are in the assigned worker directory.

Recommend expanding ownership for the authenticated provider continuation and duplicate helper seams. **No newGREEN or production qualification claimed.** No full/gate, HTTP or new-realm run.