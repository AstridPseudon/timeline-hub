# Agent private84fc union-count preservation

Changed only `tests/sdk/test_timeline_current_union_schema.py`.

Exact changed assertions:

```python
assert len(_SCHEMA['$defs']) == 59
assert len(_SCHEMA['$defs']['EditCommand']['allOf']) == 33
```

The exact closed-union expected operation set now includes:

```python
'occurrence.resize'
```

The exact inventory assertion is now:

```python
assert len(actual) == len(set(actual)) == 33
```

All existing operation, closed-argument, and published-floor assertions were retained. No schema, fixture, Runtime/client/generated file, or frozen reference was edited.

## Results

- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -B -m pytest -q -p no:cacheprovider --basetemp=/tmp/agt-private84-union-current tests/sdk/test_timeline_current_union_schema.py` — **34 passed in 202.15s**.
- `PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -B -m pytest -q -p no:cacheprovider --basetemp=/tmp/agt-private84-union-floor tests/sdk/test_timeline_materialization_schema_union.py` — **22 passed in 1.14s**.
- `git diff --check` — **passed**.

No full, live, browser, or other suite was run.
