# D137 receiving note

`PASS_INSTALL` — exact reviewed candidate installed by the manager-only CAS route.

- Source: Composition commit `cf80cfcb918ee9e311a294fb7291ad5e11c48d0b`, tree `363a551a00e9dc081da9760e21a6383296135c06`.
- Candidate: `f07b80937dde807d9aa5dad1deed278d831e7f56fb3810708e955926b45b969f`, 75,541 bytes, mode `0755`.
- Target: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/make-child-venv`; installed hash equals candidate, regular single-link `0755`.
- Required preimage: `4435d49953f583234e17a549b4df9896d9d45aa8aa7242ea51a61560ad1d0a36`, 75,503 bytes, mode `0755`.
- New backup: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/backups/make-child-venv.20261025T211101Z.bak`; same preimage hash, 75,503 bytes, mode `0755`.
- Prior backup `make-child-venv.20261025T203242Z.bak` remains unchanged at SHA-256 `0857a5e0d9faeceb585b371f1f82cbf4b574ff20350974fd3c95f852e57b6d39`.
- Protected helper hashes: `bench_store.py` `123bb93c1f2e3d6bd23c21e50cc8445afc8853e5e659759cd30dcaa53b7adfe2`; `verify_dependency_seed.py` `116b4e6bcb791d08e6c3c548f7fb52c52e9225b9428d7e201c09b02160d7bfe2`.
- Installer: `installer1826`; route: `CAS_MANAGER_ONLY`; installer exit `0`; receiving lock cleaned up.
- Installed-byte `bash -n`, seven-block in-memory compile, and bounded serialized Store smoke: PASS.

This is an installation receipt only. Publication was not performed here (`publication_ready=false`). The fixture E2E gate remains `WITHDRAWN` / `NOTRUN` with `e2e_pass=false`; no production acceptance, child request, or Agent next request is claimed.
