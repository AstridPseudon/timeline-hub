## Completed

- Serialized wheelhouse input through the queue; no daemon environment inheritance.
- Added `DEPENDENCY_SEED` and `SCRIPT_DIR` to `STORE_CONTEXT`.
- Added exact lock parsing, marker/tag checks, artifact SHA-256 validation, wheel metadata/WHEEL identity checks, and unsafe archive rejection.
- Added immutable authenticated snapshots used by pip.
- Pinned and verified the deployed helper hash.
- Added production-caller transport tests and security fixtures.
- Updated manifest and atomic install documentation.

## Tests

- Targeted pytest: `19 passed`
- Ruff on touched Python: passed
- `bash -n`: passed
- Python compile: passed
- `mypy bench_store.py`: passed
- `git diff --check`: passed
- Manifest/live baseline hash audit: passed

Known diagnostics:

- Unchanged `bench_store.py` Ruff baseline remains `EXE002`, `I001`, `C410`, `BLE001`.
- Verifier mypy is blocked by missing `packaging` stubs; no ignore flags added.
- No live provisioning, package installation, network, or full suite run.

No AgentREADY or authenticated real-cache claim is made. Commit message and `DONE` marker are ready for the harness.