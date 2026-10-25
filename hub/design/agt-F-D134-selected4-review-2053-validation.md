# Validation

- `python3.11` AST parse and `PYTHONPYCACHEPREFIX=/tmp/d134-selected4-review-2053/pycache python3.11 -m py_compile tests/sdk/test_timeline_selected_schema_runtime.py`: PASS.
- `/root/.local/bin/ruff check tests/sdk/test_timeline_selected_schema_runtime.py`: PASS.
- `/home/user/work/venv-agent/bin/python -m mypy --cache-dir=/tmp/d134-selected4-review-2053/mypy --config-file pyproject.toml tests/sdk/test_timeline_selected_schema_runtime.py`: known baseline failure only, missing `types-PyYAML` for `yaml`.
- `git diff --check a30e74e901..HEAD -- tests/sdk/test_timeline_selected_schema_runtime.py`: PASS.
- Runtime pin identity/origins: clean immutable `ab1e4f6141987706132916e2da16477f5a019464`; `runtime_protocol` resolved from `/home/user/work/wt/rt-pin-ab1e4f61`; Agent/client resolved from this worktree.
- Source-only guarded patch probe: PASS as a finding; sequential second `clips` change raises `CommandError(previous_value_mismatch)`.
- Exact own3 live command: setup refusal, 3 errors in 1.29s; no behavior credit. HTTP exact node: NOTRUN after prerequisite refusal.
