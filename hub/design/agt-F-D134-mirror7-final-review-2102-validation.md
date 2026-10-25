# Source validation

- `python3.11` AST parse and `py_compile` for both assigned files, with pyc output in private `/tmp/w-89343cba74/...` scratch — passed.
- `/root/.local/bin/ruff check tests/editing_conformance/test_native_word_anchor.py tests/editing_conformance/test_word_binding_recipe.py --output-format concise` — passed.
- `git diff --check a30e74e901a28b39c28facba3deb00d76f186e23 HEAD` — passed.
- `make PY=/home/user/work/venv-agent/bin/python mypy` — blocked by the known environment baseline: 13 missing `types-PyYAML` stubs plus one NumPy Python-3.12 `type` syntax error; the command reported 14 errors before changed-file checking.

Behavior tests were intentionally not run. The brief requires source-first review
and says no tests until the exact immutable Runtime prerequisite is published;
live behavior remains `NOTRUN`.
