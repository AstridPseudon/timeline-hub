# D134 progress

- Base verified clean: `tl/integration` / `96a6b2deea46eb33ba5184203a10e966cc5e9179`.
- Preimage gate passed: current target and donor-parent target are blob `dad27a538885ab45dd03242ee1670e00ff615dd3`.
- Exact donor intake passed: donor `8c41696560fd278705751febdcd32527bc2cdf07`, target blob `512c806487049c1b86a9d47bcafeb3dcb0ade60c`, SHA-256 `3fef15b5862e044942f2d0164b37f6f9281f86d378345d8a0b262c64870af8a4`.
- Scope passed: `git diff --name-only HEAD` contains exactly the assigned target; no evidence, review, generated, Runtime, client, pin, schema, or suite files were imported.
- Static acceptance passed: donor byte/AST equality, AST assertion and input-conservation checks, Python 3.11 private compile, `/root/.local/bin/ruff check tests/editing_conformance/test_occurrence_fork_source_baseline.py`, `/home/user/work/venv-agent-typecheck-v2/bin/python -m scripts.reshape.compare_mypy_baseline` (`current=1902 baseline=1902`), and `git diff --check`.
- The first probe with `/home/user/work/venv-agent/bin/python` was environment-blocked by missing `types-PyYAML` and incompatible NumPy stubs; shared dependencies were not modified. The required private Python 3.11 baseline passed.
- Behavioral tests are explicitly NOTRUN per brief: the central immutable Runtime route is unsupported, and source intake does not clear that block.
