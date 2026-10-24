## Completed

Added `ops-handoff/child-dependency-reuse/` containing:

- Opt-in `CHILD_VENV_DEPENDENCY_WHEELHOUSE` route.
- SHA-256 lock enforcement for approved lock `236d5be9…c778`.
- Wheelhouse validation for hashes, versions, markers, tags, symlinks, missing/extra artifacts.
- `pip --no-index --find-links --require-hashes --no-deps` installation.
- Baseline scripts, manifest, install instructions, and focused tests.

Live baseline hashes were recorded; `make-child-venv.baseline` is byte-exact.

Tests:

- Focused pytest: `8 passed`
- Ruff: passed
- Bash syntax: passed
- Compile: passed
- Mypy with `--ignore-missing-imports`: passed
- Manifest hashes: passed
- `git diff --check`: passed

Not verified: live provisioning, bootstrap offline behavior, or installation into ORCH; these were explicitly out of scope. The default path remains unchanged.