# D134 mirror7 first-return validation

Source checks completed before any live test request:

- `/usr/bin/python3.11` AST parsing of both assigned files — PASS.
- `/usr/bin/python3.11` `py_compile` with output under `/tmp/w-7174a92013/d134-mirror7-static/pyc311` — PASS.
- `ruff check tests/editing_conformance/test_native_word_anchor.py tests/editing_conformance/test_word_binding_recipe.py --output-format concise` — PASS.
- `MYPY_CACHE_DIR=/tmp/w-7174a92013/d134-mirror7-static/mypy PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-ab1e4f61" /home/user/work/venv-agent/bin/python -m mypy --config-file pyproject.toml tests/editing_conformance/test_native_word_anchor.py tests/editing_conformance/test_word_binding_recipe.py` — PASS, no issues in 2 source files.
- `git diff --check` — PASS.

Pinned Runtime preflight:

- `/home/user/work/wt/rt-pin-ab1e4f61` — clean.
- HEAD `ab1e4f6141987706132916e2da16477f5a019464`.
- Tree `7d8e77b2f5a4af79305c9212ce5174d3ea9fd657`.
- Disk admission was 6 GB available, satisfying the 5 GB floor; no heavy run was active.

Live exact7 status: BLOCKED/UNVERIFIED. The central service's generic Agent
`targeted` route is bound to mutable `/home/user/work/runtime` at
`e319fdbcd512bd5fc9bc5b2c43abfa4d749c34d9`, and no configured exact-selector
route exists for the required pinned Runtime. The prior review records that
the available central exact route deselected its integration nodes. No
wrong-runtime, fallback, overlay, or local unqualified live run was performed.
