## R3 invalid-source verification

### Result

The Runtime finding persists only as a previously unverified qualification gap; it does not persist as an Agent defect on `73df0a99bec2264777cce15b0de7277b98e575d`.
No production source change was necessary. The existing repair correctly distinguishes an invalid patch at its claimed original base from a real replay-time conflict.

### Source evidence

- `astrid/sdk/timeline/_doc_patch.py:363-366` raises `CommandError(kind="previous_value_mismatch", ref=..., path=...)` when the submitted `before` value is wrong.
- `astrid/sdk/timeline/_commit_errors.py:65-71` classifies that reason as invalid only when the evaluated head is absent or equal to the claimed base. `:90-110` emits HTTP 422 / `validation_error`, `details.status="invalid"`, code/reason, path, current head, hint, and suggested command.
- `astrid/sdk/timeline/commit.py:1058-1073` preserves replay-time guard failures as dependency/selection changes. `:1114-1127` forwards the exception path and structured failure through the production caller.
- The commit path still returns `port.preview(prepared)` unchanged at `:1095-1101`; this check did not add any wire projection or synthetic receipt.

### Direct regression evidence

Added two narrow assertions to `tests/sdk/test_timeline_commit_v2_errors.py`:

- Wrong `before` at unchanged original base returns 422 `validation_error`, `invalid`, `previous_value_mismatch`, path `['name']`, the original head in `current`, non-empty hint/suggested command, and no `accepted`, `prepared`, or head mutation.
- After a real intervening write, replay of the old patch returns 409 `conflict` / `value_conflict`, reports the actual current head, and does not append a second accepted record.

### Commands and results

- `ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime PYTHONPATH=$PWD:/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q tests/sdk/test_timeline_commit_v2_errors.py tests/editing_conformance/test_doc_patch_v2.py` — **93 passed** in 9.28s.
- `/home/user/work/venv-agent/bin/python -m ruff check --no-cache astrid/sdk/timeline/_commit_errors.py astrid/sdk/timeline/commit.py tests/sdk/test_timeline_commit_v2_errors.py` — **passed**.
- `/tmp/astrid-u2-typecheck/bin/python -m mypy --config-file pyproject.toml astrid/sdk/timeline/_commit_errors.py astrid/sdk/timeline/commit.py` — **passed**, no issues in 2 source files.
- `git diff --check` — **passed**.

### Wire limitation and next step

This is provider/DetachedPort evidence, not a live Runtime HTTP or schema qualification. It proves the Agent production caller's classification inputs and returned failure envelope, but does not claim Runtime's full v2 request/reply scope, accepted/merged `{data, receipt}`, authoritative steps/dependencies, or live preview wire behavior. No full, browser, heavy, or Runtime suite was run, and no Runtime/schema/generated files were changed. Runtime should rerun its bounded native qualification against this exact Agent source after its pending Runtime-side repairs land.
