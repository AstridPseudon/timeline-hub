# Agent R2 root current-port report

- Task: `agt-R2-root-current-port-1838`
- Base: `78738040d72ce74c42ddf7731221aecb06f9246d`
- Source: `d146b4204`
- Worktree: `/home/user/work/wt/agt-R2-root-current-port-1838`
- Result: requested two source blobs imported exactly; no source design artifact imported.
- Review/merge: no merge request; source approval remains pending.

## Scope

Imported only:

1. `astrid/sdk/timeline/_root_inverse.py`
2. `tests/editing_conformance/test_transient_root_baseline.py`

The source design file `design/agent-R2-transient-root-sol-1831.md` and held R2 ancestry were not imported. No `_step_undo.py`, `inverse.py`, runtime, API, pin, or test-body edits were made.

Current file SHA-256 values equal the source blob SHA-256 values:

- `_root_inverse.py`: `6715f34f2f60609d2ed8436f0dde94b475a0966de9d869f4dc3ceade3160b3a1`
- `test_transient_root_baseline.py`: `a7aff9f48d3f2b110f01b3aab1015f75a24eb004504453019d20adec58d0c39b`

## Checks

Passing:

- `cmp <(git show d146b4204:astrid/sdk/timeline/_root_inverse.py) astrid/sdk/timeline/_root_inverse.py` and equivalent test-file comparison.
- `git diff --check`.
- `ruff check astrid/sdk/timeline/_root_inverse.py tests/editing_conformance/test_transient_root_baseline.py` — passed.
- `PYTHONPATH=/home/user/work/wt/agt-R2-root-current-port-1838:/home/user/work/runtime /home/user/work/venv-agent/bin/python -m mypy --config-file pyproject.toml --follow-imports=skip --ignore-missing-imports astrid/sdk/timeline/_root_inverse.py tests/editing_conformance/test_transient_root_baseline.py` — `Success: no issues found in 2 source files`.
- AST parse of both changed files — passed.
- Credential scan of both changed files — no credential patterns found.

Targeted test results:

- `PYTHONPATH=/home/user/work/wt/agt-R2-root-current-port-1838:/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q tests/editing_conformance/test_transient_root_baseline.py tests/editing_conformance/test_provider_step_undo_v2.py -k 'transient_root or whole_inverse_projects_each_stage or create_edit_whole_undo_redo_retains_transient_roots'` — `1 passed, 11 failed, 16 deselected`.
- `PYTHONPATH=/home/user/work/wt/agt-R2-root-current-port-1838:/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q tests/editing_conformance/test_provider_step_undo_v2.py tests/editing_conformance/test_inverse_stage_images.py` — `18 passed, 1 failed`.

## Boundary / next step

The failures are all at the same current-baseline boundary: current provider records do not contain `_inverse_stage` for the transient-root redo path, and the imported guard raises `CommandError: restored root differs from accepted source`. The existing transient-root control therefore fails during its later redo. Current HEAD does not contain held R2 `0b735c137`, `65a2e5aec`, `fb97d24bf`, or `8875589f6`; the source commit is on that separate R2 line. Per task instructions, `_step_undo.py` and `inverse.py` were not edited. The root source can merge only after review and a current-target pass, or after the orchestrator resolves this ancestry/record-shape boundary.
