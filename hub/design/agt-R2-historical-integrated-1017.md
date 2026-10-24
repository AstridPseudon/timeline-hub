# PASS — R2 historical inverse integration

- Exact integrated HEAD: `d83e8de3a1b0ba51fa50b0f890adb1c91730f2d0`; reviewed source parent: `1c9171b855`.
- Verified hashes:
  - `inverse.py`: `41faadf...9d7031c`
  - new test: `ec0bf6...7256c54`
- Production staged/landing callers use `_input_read_state`.
- Only post-R1 additions are reviewed `30cf3c00aa` capture helper/tests plus the reviewed historical-source files. No original tests rewritten.
- Runtime pin: `becfe6db...`; clean.

Tests/checks:

- Four acceptance files: **67 passed**, 0 failures/errors/skips. Durable XML: `evidence/integrated.xml`.
- Reused independent reviewed controls: **244 passed**.
- `make ruff PY=/home/user/work/venv-agent/bin/python`: **2143/2143**.
- `make mypy PY=/home/user/work/venv-agent-typecheck-v2/bin/python`: **1902/1902**.
- `git diff --check`: PASS.

The actual before/after receipt confirms fork cases changed from `identity_conflict` to pass; duplicate controls remained passing. No duplicate audit, full suite, browser, HTTP, or gate run performed. Worktree is clean; `DONE` and the required commit message were created.