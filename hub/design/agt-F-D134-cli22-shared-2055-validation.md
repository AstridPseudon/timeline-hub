# Validation

- `AST_PARSE_AND_PYCOMPILE_PASS`: Python 3.11 AST parse and `py_compile` of the
  target plus the three governing CLI source files, with bytecode emitted only
  under `/tmp/w-7937dda102/d134-cli22-compile`.
- `make PY=/home/user/work/venv-agent/bin/python ruff`: pass; governing baseline
  `current=2143 baseline=2143`.
- `make PY=/home/user/work/venv-agent/bin/python mypy`: blocked by the shared
  environment before baseline comparison: 13 missing `yaml` stubs and one
  NumPy stub using Python-3.12-only syntax under the configured Python 3.11
  check. No dependency files were changed.
- `git diff --check`: pass.
- Parser smoke: `edit commands-file` exits 2; current `commit` with its
  required `--file/--message/--idempotency-key` parses; current `apply` parses.
- Exact targeted source-control test: failed at retired CLI admission as
  recorded in `setup-proof.md`.
- No full suite, family suite, central test-service request, or remaining exact
  root-045 rerun was made.
