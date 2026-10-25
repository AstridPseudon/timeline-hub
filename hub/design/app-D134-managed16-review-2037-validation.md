# Validation and source decision

## Static validation

- `python3.11 -m py_compile` on all three changed files with `PYTHONPYCACHEPREFIX` under an own `/tmp` directory: PASS (`compile_exit=0`). Python `3.11.17`.
- `ruff check --no-cache tests/editing_conformance/test_recipe_m2_shared_auto_placement.py tests/editing_conformance/test_recipe_m2_shot_pool.py tests/editing_conformance/test_recipe_occurrence_media.py`: PASS (`All checks passed!`).
- `mypy --cache-dir=<own /tmp>/mypy-cache` on the same three files: PASS (`Success: no issues found in 3 source files`).
- `git diff --check a30e74e90 6c5c05ac8 -- <three authorized files>`: PASS.
- Outside-scope diff check against `a30e74e90`: PASS; changed-file count outside the three authorized paths is `0`.
- AST conservation script: PASS for equal test function names, equal test-function bodies, and unchanged `inputs()` body. Assertion AST counts are shared auto `71`, shot pool `59`, occurrence media `43`.

## Execution controls

No pytest, Runtime service, socket, browser, full/family/core/profile/P2/P4/native-body, acquisition, fresh measurement, or test-service request was run by this review. The historical author-requested targeted run is recorded only as an environment ImportError and receives zero behavior credit:

`ImportError while loading conftest ... ModuleNotFoundError: No module named 'runtime_protocol'`.

The WIP remains exactly preserved for historical comparison; no source file was edited by this review.

## Decision

The source migration is FAIL/UNAPPLIED. The static gates pass, but they do not establish a supported semantic setup. The WIP routes managed16 through a source-bound emitter against a semantic-born empty shot, while the required original shot item membership is provider-managed. Return the finite seam rather than reauthoring the fixture or changing a guard.
