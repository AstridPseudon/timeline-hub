# Agent R2/G3 schema join

Joined the approved canonical inverse `steps` schema onto current G3/R2 source, retaining the reviewed schema-floor and operation-census tests. The staged delta is exactly:

- `astrid/core/timeline/schema/edit-command.schema.json`
- `tests/sdk/test_timeline_composed_schema.py`
- `tests/sdk/test_timeline_current_union_schema.py`

The schema content matches the approved SHA-256 `d106dfe8212500709b4072d7bc0486f83c27d5d8de33d215cb52b9ea7d46357d`. Targeted evidence is 77 passed, scoped Ruff passed, and Ruff no-growth is 2150 findings equal to baseline. Private scoped mypy passed; normal mypy remains environment-blocked by missing YAML stubs and the shared Python/NumPy mismatch. No Runtime wire, pin, generated-artifact, or implementation change is claimed.

