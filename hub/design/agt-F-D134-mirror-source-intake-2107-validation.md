# D134 source intake validation

- Preimage gate: PASS. Both current files matched their donor `a30e` preimages byte-for-byte before import.
- Exact donor content: PASS. Both final files match donor `ff88764f0d3d3b3efcb03e8dec4feb735810be78` by Git blob and SHA-256.
- AST and authored-input conservation: PASS. Python 3.11 ASTs are equal to donor ASTs; required mirror helper/test functions, reference key, change-echo/reference labels, and echo cases remain present.
- `/usr/bin/python3.11 -m py_compile tests/editing_conformance/test_native_word_anchor.py tests/editing_conformance/test_word_binding_recipe.py` with `PYTHONPYCACHEPREFIX=/tmp/w-b8b46567aa/d134-mirror-source-intake-2107-static/pyc311`: PASS.
- `/root/.local/bin/ruff check tests/editing_conformance/test_native_word_anchor.py tests/editing_conformance/test_word_binding_recipe.py --output-format concise`: PASS.
- `MYPY_CACHE_DIR=/tmp/w-b8b46567aa/d134-mirror-source-intake-2107-static/mypy PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent-typecheck-v2/bin/python -m scripts.reshape.compare_mypy_baseline`: PASS (`current=1902 baseline=1902`).
- `git diff --check`: PASS.
- Behavior selectors: NOTRUN by task policy; source intake does not provide behavior or core-count credit. The exact immutable Runtime prerequisite is `ab1e4f6141987706132916e2da16477f5a019464`.
