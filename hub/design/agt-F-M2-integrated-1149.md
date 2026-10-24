# Report

- Queue and merge gates complete: `merge-agt-F-M2-media-fixtures-1132` → `44cc5f6b34`.
- Actual Agent home clean at SHA `44cc5f6b34`, tree `18588f42…`.
- All six reviewed `bb95236ec1` blobs match exactly.
- Runtime clean at `becfe6db88`, tree `7edc08e3…`.
- Production Agent inverse/provider/commit and Runtime `timeline_commit*.py` hashes unchanged before/after.

Command run on actual home:

```text
ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime PYTHONPATH=/home/user/work/agent:/home/user/work/runtime PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --timeout=45 --tb=short tests/editing_conformance/test_recipe_m2_shot_pool.py tests/editing_conformance/test_recipe_m2_shared_auto_placement.py tests/editing_conformance/test_recipe_m2_video_unplace.py tests/editing_conformance/test_recipe_m2_placement_create_unplace.py tests/editing_conformance/test_recipe_occurrence_fork.py --junitxml=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-M2-integrated-1149/evidence/integrated.xml
```

Result: **200 passed in 68.17s**. JUnit: 200 tests, 0 failures/errors/skips; SHA-256 `7b15b482…`.

Before/after trees, imports, source hashes, AST hashes, and clean statuses are identical. Reused exact reviewed Ruff/mypy results because all six blobs matched. Public-session `50dd` remains separate and its prior home proof was PASS42; it was not rerun.

No files were edited, and no full/gate/HTTP/ABA/child/original-267 suite was run. Evidence is retained under the required worker `evidence/` path. DONE marker and commit message were created.