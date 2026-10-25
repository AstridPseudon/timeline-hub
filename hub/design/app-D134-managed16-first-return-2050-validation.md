# D134 managed16 first return validation

## Source disposition

- Restored the exact `a30e74e901a28b39c28facba3deb00d76f186e23` blobs for the three authorized test files using `git show` followed by file copy.
- `git diff --quiet a30e74e901a28b39c28facba3deb00d76f186e23 --` passed: the complete worktree tree equals the original source tree.
- Only the three authorized paths differ from WIP `6c5c05ac8cea7bb5c9a5507a54c6d3da89ea75d4`.
- All three file SHA-256 values match their original blobs.

## Static validation

- `PYTHONPYCACHEPREFIX=/tmp/d134-managed16-first-return-2050/pycache python3.11 -m py_compile tests/editing_conformance/test_recipe_m2_shared_auto_placement.py tests/editing_conformance/test_recipe_m2_shot_pool.py tests/editing_conformance/test_recipe_occurrence_media.py` — PASS.
- `ruff check --no-cache tests/editing_conformance/test_recipe_m2_shared_auto_placement.py tests/editing_conformance/test_recipe_m2_shot_pool.py tests/editing_conformance/test_recipe_occurrence_media.py` — PASS (`All checks passed!`).
- `mypy --cache-dir=/tmp/d134-managed16-first-return-2050/mypy-cache tests/editing_conformance/test_recipe_m2_shared_auto_placement.py tests/editing_conformance/test_recipe_m2_shot_pool.py tests/editing_conformance/test_recipe_occurrence_media.py` — PASS (`Success: no issues found in 3 source files`).
- `git diff --check a30e74e901a28b39c28facba3deb00d76f186e23 --` — PASS.
- AST conservation script — PASS: 173 assertion ASTs total (71, 59, 43), all function ASTs equal to original, and the local `inputs()` AST is equal to original; the two other files import `inputs()`.

## Execution controls

No pytest, Runtime service, socket, browser, test service, provider/body execution, acquisition, or full/family suite was run. No behavior credit is claimed.
