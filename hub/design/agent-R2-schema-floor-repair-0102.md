# R2 schema floor/census handoff

Independent delta review: PASS.

Base: `7689fd97b72d93061b50d3d85922b33a13703cd5` (`7689fd97b`).

This is a test-only repair in the two assigned files:

- `tests/sdk/test_timeline_current_union_schema.py` strips only the approved
  `InverseArgs.properties.steps` addition during current-to-old reconstruction,
  asserts that optional shape exactly, and retains the existing full historical
  equality checks and fixture byte-hash assertions.
- `tests/sdk/test_timeline_composed_schema.py` adds one minimal valid
  `doc.patch` sample to the existing operation census and keeps whole-undo,
  selected-step, null/empty/duplicate/blank/unknown-form refusal coverage.

Evidence:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/sdk/test_timeline_current_union_schema.py tests/sdk/test_timeline_composed_schema.py tests/editing_conformance/test_step_undo_v2.py tests/editing_conformance/test_provider_step_undo_v2.py
94 passed in 155.94s

RUFF_CACHE_DIR=/tmp/agt-R2-schema-floor-repair-0102/ruff-cache /home/user/work/venv-agent/bin/python -m ruff check tests/sdk/test_timeline_current_union_schema.py tests/sdk/test_timeline_composed_schema.py
All checks passed!

MYPY_CACHE_DIR=/tmp/agt-R2-schema-floor-repair-0102/mypy-cache /tmp/astrid-u2-typecheck/bin/python -m mypy --follow-imports=skip tests/sdk/test_timeline_current_union_schema.py tests/sdk/test_timeline_composed_schema.py
Success: no issues found in 2 source files

git diff --check
passed
```

The three original historical-floor equality failures are green with old
floors retained. The canonical production schema was not edited:
`astrid/core/timeline/schema/edit-command.schema.json` remains byte-identical
to the base and SHA256
`d106dfe8212500709b4072d7bc0486f83c27d5d8de33d215cb52b9ea7d46357d`.
Only the two assigned test files are modified. The production caller remains
`astrid/sdk/timeline/commands.py:_SCHEMA`; no Runtime or full/browser suite was
run in this test-only lane.
