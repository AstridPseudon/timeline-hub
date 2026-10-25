# D134 validation

- `PYTHONPYCACHEPREFIX=/tmp/w-bc995b7564/agt-F-D134-media48-pycache /home/user/work/venv-agent/bin/python -m py_compile tests/editing_conformance/test_commit_runtime_occurrence_media.py` — PASS
- `ruff check tests/editing_conformance/test_commit_runtime_occurrence_media.py` — PASS
- `/home/user/work/venv-agent/bin/mypy tests/editing_conformance/test_commit_runtime_occurrence_media.py` — PASS
- `git diff --check` — PASS
- `git status --short --branch` — clean, no source delta
- Targeted source-control case before the attempted edge-preserving experiment: `ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime PYTHONPATH=/home/user/work/runtime:. /home/user/work/venv-agent/bin/python -m pytest -m integration -q tests/editing_conformance/test_commit_runtime_occurrence_media.py::test_exact_capture_acceptance_inverse_redo_restart_and_retry[image-add] --tb=short` — expected setup error at `_create_fixture`, `shot:chapter-shot` root replacement; no behavior body reached
- Edge-preserving experiment was reverted; no exact cohort rerun was made because the supported-caller seam is unavailable and the task forbids retry/transfer or weakened setup
