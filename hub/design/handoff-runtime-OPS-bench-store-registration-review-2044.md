# OPS-bench-store registration review

Verdict: **behavioral source PASS; exact packet acceptance CONDITIONAL/FAIL; live cutover UNKNOWN and STOPPED.**

- Copied packet hashes:

  - `bench_store.py`: `fa11f8fa12c857497c966023564a0179e7ef15882fc586935de1d9019065e4ad`
  - `test-run`: `92e43c5c0a9b5d87a1c9f29d7da7ec15c6025fbb57f66f64fe45f73a5c67f99b`
  - `test-registration.py`: `2889d0f18736b4e2255c235fc324b6948b21f654b6d3cd83b3c66f724f566c72`
  - `source.patch`: `775b4459abddfb4ef0c8e5490c171b07c38389b7d459cd26e5cd043033bfcbda`

- `PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python /tmp/w-173d90b75d/test-registration.py`: **21 passed, 0 failed, 0 skipped**.
- Coverage included exact-seven/shared-key success, managed-entry preservation, normal and `env -i` caller/CLI, custody refusal, inherited child leases, crash/recovery, concurrent serialization, stale/ambiguous/current-protected refs, symlink/hardlink/foreign-owner simulation, race handling, and outside/legacy byte preservation.
- `bash -n` caller: PASS.
- In-memory Python compile: PASS.
- Narrow Ruff (`--select E,F --ignore E501`): PASS.
- Full isolated Ruff: **FAIL, 15 existing/style findings** across source and fixture; no edits made.
- Private source patch replay: applies cleanly. Caller `cmp`: PASS. Core `cmp`: **FAIL only due `UNREGISTER` formatting** (one-line in patch replay versus multiline supplied core); AST equivalence: PASS.
- Installed six-hash comparison: PASS; before hashes match actual installed files and after equals before:

  `bench_store.py=6d9368207947aa316e1ed6486c5fa7ef843a84f50163114bb958011b538712a8`

  `test-run=f599c5ad7bf3cd61aeb01791d903ce6edfa87d5d04a39b3ebb630b3517b17ff4`

  `make-child-venv=89d82618c6c67819e40cc73d32b6d1c372f95889761d5170bb1af3a83dc5fcff`

  `make-runtime=99cca067330fd87e1f8c475045ab8282e944b2455e25d44d4c6072e77e9e4e28`

  `request-child-venv=72cafb3a5ec343f648a0e41d59a51e7c803ee51b4d04a394dc2010df828bd731`

  `request-runtime=f13a1d073699712ccfb05e8463ad97ff69dc210a2617f2c9e0140a242591f7b1`

- Runtime worktree: clean; `git diff --check`: PASS.

No live bench, queue, config, registration, process, cleanup, install, or Git mutation was performed. No new real-caller/supervisor defect was proven. The known remaining seam stands: installed core `6d9368…` lacks registration birth custody and caller `f599c5…` never leased these unmanaged names. A separate owner/supervisor cutover is required before any live migration; this packet must not be called live authority.

Foreign-UID testing is simulated owner-control only; real cross-UID `chown` proof remains unavailable (`errno 22` limitation).

Recommendation: retain the 21/21 result as prospective private API proof, repair the patch/core byte mismatch and resolve the Ruff findings or document the accepted baseline, then obtain separately reviewed cutover proof.