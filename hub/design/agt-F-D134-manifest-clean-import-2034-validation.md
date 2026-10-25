# D134 validation

- `git diff --check`: PASS.
- `git diff --name-only`: exactly the requested target file.
- Outside-target diff check (`git diff --quiet -- . ':(exclude)tests/editing_conformance/test_commit_runtime_media_manifest_inverse.py'`): PASS.
- Donor target blob equals receiving target blob: PASS (`e63d777f93b458f6276d10aafa69497b8e2a75d8`).
- Donor parent target equals receiving preimage: PASS (`18ab205665cde75e4c58d2f2e8f4ef917b63fabb`).
- Python 3.11 AST parse and `compile`: PASS.
- `ruff check tests/editing_conformance/test_commit_runtime_media_manifest_inverse.py`: PASS.
- `mypy tests/editing_conformance/test_commit_runtime_media_manifest_inverse.py`: PASS.
- `PYTHONDONTWRITEBYTECODE=1 ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime PYTHONPATH=/home/user/work/runtime:$PWD python -m pytest -q -m integration -o cache_dir=/tmp/w-226e29c166/pytest-cache-integration tests/editing_conformance/test_commit_runtime_media_manifest_inverse.py`: reaches both cases; 2 errors in fixture setup, both the known managed-edge rejection. This is the task-stated original own2 condition, not closed by this source-only import.

The first default-lane pytest invocation deselected both integration cases by design; it was followed by the explicit `-m integration` run above. No full suite was requested.
