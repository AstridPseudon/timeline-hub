## Report

Implemented the A4 witness correction.

- Preserves all submitted command/step fields and created ordering.
- Verifies authoritative authorship, bindings, expect, reads, selections, resolved fields.
- Verifies full authoritative step effects/dependencies from the normal provider candidate.
- Added offline mutation controls for submitted fields, created claims, bindings, effects, and step metadata.
- No production/provider/API/schema/pin changes.

Checks passed:

- `py_compile`
- Offline pytest: `1 passed` (one existing unknown-mark warning)
- Ruff
- Private mypy
- Artifact manifest
- `git diff --check`
- Retained-response + normal-provider oracle comparison
- Assertion preservation: 52/53 unchanged; only stale command equality replaced.

No live Runtime/App rerun or full suite was performed, as instructed. Completion marker and commit message were written; harness commit subject is `test(timeline): preserve authoritative image witness metadata`.