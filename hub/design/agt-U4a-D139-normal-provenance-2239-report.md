Implemented U4a / PLAN3 / D139.

- Updated `runtime.lock.json` provenance from `ab1e4f…` to `f103bb…`.
- Confirmed all 15 mappings, hashes, client/schema/fixture bytes unchanged.
- Runtime producer remained clean at exact `f103bb…`.
- Only tracked change: `runtime.lock.json`.

Validation:

- `refresh_runtime_client.py` — PASS
- `vendor_lock.py check` — PASS
- `artifact_manifest.py --check` — PASS
- `git diff --check` — PASS
- Evidence assertions — PASS

Evidence written to the requested absolute directory. No product/full-suite tests run per scope. Completion marker and commit message were created.