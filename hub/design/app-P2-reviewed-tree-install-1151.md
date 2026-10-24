## D30 report — PASS

Installed only the reviewed P2 caller row in `scratchpad/orch/tests/suites.conf`.

- P2 row SHA256: `6a45d0567f7dea7a3c15fbcaf687f9dd62debf4527464529d8a4faf8f8e48fee`
- Registry SHA256: `fa6ec51a5556af78c10f9d32f1cda853f498555422e3e4b7f05ecfd7b3729494`
- P3 unchanged: `23226c274dbdbb8750f009cb89d7920db40eb49513af906df7b4f76d9a7a3bf0`
- Outsiders unchanged: 247 rows, 465609 bytes, SHA256 `9acf76fafd09c0e4ecd89be6288402f8557dcb17c3a70f492ce9ae56d241e2e8`
- Source: `d6ed8cbda122d810d5836ebfce3c56c10e76e9b4`, tree `542b772e…`
- Target: `/home/user/work/wt/app-pin-d6ed8cbd`

Checks passed:

- Committed `prepare()`: exact reviewed candidate and prepared hashes.
- Review1140 controls: positive plus 7 shell refusals; 22 publication refusals.
- Registry readback and full-hash CAS under existing bench-store mutex.
- Python compile, JSON parse, decoded/wrapped Bash syntax, `git diff --check`.
- App worktree remains clean.

No service, browser, HTTP, backend, build, provision, original, or full run was performed. No live GO claim. Manager may queue the single authorized P2 service run.