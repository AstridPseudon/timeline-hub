# D137 receiving note

Actual guarded receipt: `PASS_INSTALL`.

- Route: `CAS_MANAGER_ONLY`, reviewed installer `installer1826`.
- Source: commit `0c4170e42d2ff435ea855a54c940299619f6a285`, tree `b43a840b75bf895f9789732c56585175c4b367bf`.
- Installed target: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/make-child-venv`.
- Candidate: `4435d49953f583234e17a549b4df9896d9d45aa8aa7242ea51a61560ad1d0a36`, 75,503 bytes, mode `0755`.
- Retained exact backup: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/backups/make-child-venv.20261025T203242Z.bak`, `0857a5e0d9faeceb585b371f1f82cbf4b574ff20350974fd3c95f852e57b6d39`, 68,351 bytes, mode `0755`.
- Protected helper readback and byte comparison: PASS.
- Actual installed logging control: PASS; no Store, child, fixture E2E, network, or production request.

This is an installation receipt, not a publication receipt. Publication is
separate and remains for the manager/lead. D137 records the genuine fixture
E2E gate as `WITHDRAWN` / `NOTRUN` with `e2e_pass=false`; no production
acceptance claim is made.
