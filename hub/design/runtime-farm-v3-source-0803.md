Implemented the v3 packet under `ops-handoff/farm-agent-full-v3/`:

- D21b exact child request for Agent `9cd3dbe8…` + Runtime `1d9ddba5…`.
- Guarded installer replacing only the existing `full-farm` row.
- Child `python -I` execution with no `PYTHONPATH` binding.
- Exact receipt, marker, source, client, lock, Node20, Remotion, registry, backup, and rollback guards.
- Private tests and manifest.

Checks:

- `20 passed`
- Manifest: all files verified
- Ruff: pass
- Mypy with missing-imports ignored: pass
- Registration row `bash -n`: pass
- `git diff --check`: pass

No provisioning, network, live Store mutation, full Farm suite, or checkpoint was run. Actual D21b receipt and Farm-owned preflight remain required.