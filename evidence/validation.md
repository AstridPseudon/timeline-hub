# D134 validation

## Source and scope

- Base `tl/integration` was clean at `96a6b2deea46eb33ba5184203a10e966cc5e9179`.
- Current target preimage: `dad27a538885ab45dd03242ee1670e00ff615dd3`.
- Donor commit: `8c41696560fd278705751febdcd32527bc2cdf07`.
- Donor target and final target: `512c806487049c1b86a9d47bcafeb3dcb0ade60c`.
- Donor commit changed only the assigned source file. The donor parent differs from current head only at `tests/editing_conformance/test_commit_runtime_media_manifest_inverse.py`, the known manifest-only wrapper; that path was not imported.
- `git diff --name-only` after intake lists only the assigned source file plus these own evidence files.
- Donor patch and worktree target diff compare exactly; neither donor nor current head is an ancestor of the other.

## Checks

| Command | Result |
| --- | --- |
| `python3.11` private `compile(source, filename, "exec")` | PASS, Python 3.11.17 |
| `/root/.local/bin/ruff check tests/editing_conformance/test_occurrence_fork_source_baseline.py` | PASS |
| preimage→donor AST check: function set, ordered assertions, fork inputs | PASS, 9 functions / 31 assertions; `(before, OWNER, "selected-shot")` retained |
| donor patch vs worktree target diff | PASS, exact |
| `git diff --check` | PASS |
| `PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m scripts.reshape.compare_mypy_baseline` | BLOCKED, exit 2 before baseline comparison: missing `types-PyYAML` stubs and NumPy stubs use Python 3.12-only syntax under the shared Python 3.13 environment |

No behavioral pytest or Runtime/live-socket test was run: functional status is explicitly NOTRUN under the D134 brief.
