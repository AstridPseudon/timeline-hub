# F-core integrated proof — PASS

Integrated read-only proof for exact HEAD `2e21af300abbefc8afbad217189fa4715cf82616` / tree `b7889d80cb59b97726a964312a377e794e582592`.

The production change is conflict-free and unchanged from reviewed commit `e1aff378381ef55629944a913859334864346f89`. Exact current blobs:

- `_effect_registry.py`: `35a4a13b42d8410d479d9188a4b30945016c0c44`
- `remotion_runtime.py`: `7cecca9d6a6438066434b2442ed82c2891db9aea`
- `root_preparation.py`: `bcff379019c39f36d7a7a9e34ea1bdd7202e484b`

The exact prescribed integrated targeted command passed **16 tests** in **24.47s**. It used the venv-agent interpreter, `PYTHONDONTWRITEBYTECODE=1`, `PYTHONPATH=.:/home/user/work/runtime`, the Runtime checkout, no pytest cache, and no addopts. The production caller path is covered through generator `main()` and the core lock boundary, with canonical env constants and Runtime `current_user()`.

Retained reviewed material was verified: R2 `f7fcb72827405ea938555db92827a5095f02a3a5`, R1 `d46210398` with matching current touched blobs, and P4 blob `afc9c112527692536a065de8cdbfc7a25c19bc26`. Ruff passed at `2149/2149`; vendor lock, artifact manifest, and `git diff --check` passed. The reviewed mypy evidence remains `1912/1912`; a fresh integrated rerun was attempted twice but exceeded the bounded 120-second window without diagnostics, so no new mypy result is claimed. Six scoped Ruff findings are inherited unchanged-line findings from review0856: `BLE001` at `remotion_runtime.py:151,459,1069`, `I001` at `160,520`, and `F401` at `520`.

No source, test, fixture, pin, contract, environment, dependency, or Git mutation was made. Full/native14/crash24/P1/P4 HTTP/heavy/browser/render duplicate suites were not run. C0 request/reply fields and required preview/error forms remain preserved.
