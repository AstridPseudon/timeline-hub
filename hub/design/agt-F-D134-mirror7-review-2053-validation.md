# Validation

- `/usr/bin/python3.11` AST parse and `py_compile` for both assigned files into a private temporary cache: PASS.
- `/root/.local/bin/ruff check tests/editing_conformance/test_native_word_anchor.py tests/editing_conformance/test_word_binding_recipe.py --output-format concise`: PASS.
- `git diff --check`: PASS.
- `make PY=/home/user/work/venv-agent/bin/python mypy`: BLOCKED by the known environment baseline before changed-file checking: 13 missing `yaml` stubs plus NumPy stubs using Python 3.12 `type` syntax (14 errors total here).
- Required Runtime pin `/home/user/work/wt/rt-pin-ab1e4f61` is clean at `ab1e4f6141987706132916e2da16477f5a019464`; author live evidence used `e319fdbcd512bd5fc9bc5b2c43abfa4d749c34d9` instead.
- No live selectors were rerun: the author's exact7 result was not accepted because F1/F2 are source-visible coverage losses and its Runtime identity is not the required pin. No full/family/unrelated suite was run.
