# Validation

- `PYTHONPYCACHEPREFIX=/tmp/agt-F-D134-managed105-shared-2055-check-final/pycache /home/user/work/venv-agent/bin/python -m py_compile tests/editing_conformance/test_commit_runtime_occurrence_media.py tests/editing_conformance/test_commit_runtime_parent_media_swap.py tests/editing_conformance/test_commit_runtime_video_unplace.py` — PASS.
- AST parse of the three assigned fixture files — PASS.
- `/home/user/work/venv-agent/bin/ruff check tests/editing_conformance/test_commit_runtime_occurrence_media.py tests/editing_conformance/test_commit_runtime_video_unplace.py` — PASS.
- Scoped Ruff including `test_commit_runtime_parent_media_swap.py` — baseline FAIL at existing F811 redefinition on line 226; no fix applied because the worktree is byte-clean and the task forbids unrelated edits.
- `/home/user/work/venv-agent/bin/python -m scripts.reshape.compare_mypy_baseline` — environment baseline FAIL: missing `types-PyYAML` stubs and NumPy stubs require Python 3.12; no dependency installation or source change applied.
- `git diff --check` — PASS; final source diff is empty.
- Representative integration: pinned Runtime `ab1e4f6141987706132916e2da16477f5a019464`, tree `7d8e77b2f5a4af79305c9212ce5174d3ea9fd657`, 5,538,652,160 bytes available, no heavy/render/browser route. `test_exact_capture_acceptance_inverse_redo_restart_and_retry[image-add]` — setup ERROR at SDK shot item correspondence (`shot items must be an array` boundary: `shot item correspondence changed`); this is the authenticated-source refusal, not a product-fault or green receipt.
