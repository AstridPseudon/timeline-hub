## D137 report

Implemented the maker shell-closure fix:

- Exported `stage_stderr_path` and `retain_stage_stderr` across the real `Store.ensure` child-shell boundary.
- Updated the actual serialized-boundary regression for nonzero, timeout, private stderr, and rollback cleanup.
- Rebound permitted CAS/install-prep pins to candidate `f07b8093…b969f`, with current 4435 maker as preimage.
- `STORE_PY`, `STORE_VERIFY`, verifier/trust controls, and protected helpers remain byte-identical.

Tests/checks:

- 44/44 custody tests passed.
- Ruff passed.
- Bash syntax passed.
- 7 embedded Python blocks and scoped Python files compiled.
- Parent reproduced RED: `stage_stderr_path: command not found`.
- Candidate reproduced GREEN through the serialized runner.
- Installer dry-run controls passed.
- `git diff --check` passed.

No genuine request retry, install, whole-make, provider/core, Farm, or full suite was run. D137 fixture E2E remains withdrawn/NOTRUN. Evidence is in the requested worker `evidence/` directory; commit message and `DONE` marker are recorded.