# D139a receiving note

Actual guarded receipt: `PASS_INSTALL_COMBINED_WITH_ACCEPTANCE_LIMITS`.

- Source: `0921ec1c8eb7cab668203963c5a5eeb0e4616c00` / tree `577a3cca4e23c94d051e839eb47d7b1bd7a1c9c3`.
- Maker: exact reviewed candidate installed at `ORCH/bin/make-child-venv`; exact f07 preimage retained in `backups/make-child-venv.20261025T231036Z.bak`.
- Wrapper: exact independently reviewed candidate installed at `ORCH/bin/request-child-venv`; exact bdda preimage retained in `backups/request-child-venv.20261025T231055Z.bak`.
- Checker: exact reviewed source installed into initially absent `ORCH/bin/check-child-imports` through O_EXCL/no-follow initial copy; no backup.
- Protected `bench_store.py` and `verify_dependency_seed.py` hashes are unchanged.
- Locks were cleaned after successful readback; previous backups were untouched.
- D137 decision is honest `WITHDRAWN` / `NOTRUN`, `e2e_pass=false`; no E2E or production acceptance claim is made.
- No live request, Store, child, venv, registration, acquisition, or publication occurred.

The installed checker’s canonical CLI diagnostic is expected exit 1 with the
authenticated 1146-row census and 12 missing canonical names. It is diagnostic
only and not evidence of an installed child.
