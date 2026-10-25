# D128/F portable receiving validation

The wrapper binds the reviewed source commit/tree and all immutable helper,
maker, manifest, dependency, and bootstrap hashes. It stages only the
documented tiny source inputs and locally builds the two pinned dependency
wheels. The test service creates the two clean fixture Git commits and runs
the unchanged `Store.initialize` setup.

Local checks:

- `bash -n evidence/inventory_whole_maker.sh`: PASS.
- `git diff --check`: PASS.
- The guarded `composition inventory-whole-maker` row changed only its command;
  the previous row SHA was `fcfd280bb6441a462707e645743187efec6a6ff95d83528903579bac67b0fd8f`.

Service result:

- Service ID: `agt-OPS-portable-E2E-receive-1945-inventory-whole-maker-1025194809-23349`.
- Terminal status/exit: `fail` / `2`.
- Exact `--check-only`: PASS, `ok=true`, `missing=[]`, and all mutation flags
  false; this was preserved as the private service `check-only.json`.
- Private venue setup completed, including two fixture Stores.
- Parent command exit: `2`; stages reached `venv start`, `venv complete`, and
  `bootstrap-pip start`, then failed the expected parent inventory-refusal
  assertion (`parent did not reach the expected inventory refusal`).
- Candidate GREEN, sealed verifier, registration, and adversarial checks:
  **NOTRUN**. No retry was made.

The private raw result is retained by the service. No production Store,
installation, registration, child request, or source/product change occurred.
