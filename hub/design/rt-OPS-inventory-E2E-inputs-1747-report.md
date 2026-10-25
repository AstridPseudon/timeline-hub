Implemented durable tiny-fixture E2E preparation:

- Added hashed Agent/Runtime/dependency sources and offline wheel build support.
- Added private `Store.initialize` venue preparation and strict wheel/source/maker/helper verification.
- Added runner documentation and evidence manifests.
- Preserved `make-child-venv`, embedded verifier, and Store helpers unchanged.

Tests:

- `bash -n ops-child-custody/make-child-venv` — PASS
- unittest discovery — 40/40 PASS
- Ruff — PASS
- In-memory Python compilation — 12 files PASS
- `git diff --check` — PASS

Evidence: [inputs.json](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-OPS-inventory-E2E-inputs-1747/evidence/inputs.json), [validation.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-OPS-inventory-E2E-inputs-1747/evidence/validation.md).

The genuine parent-RED/candidate-GREEN make remains NOTRUN pending an admitted receiving venue. Commit message written; `DONE` created.