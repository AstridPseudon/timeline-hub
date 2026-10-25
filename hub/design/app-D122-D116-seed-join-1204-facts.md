# D122/D116 exact reviewed seed join facts

- Normal base: `cf7b8d7c2b4cb980de1d873f0498784d5210d508`
- Exact reviewed donor: `7c717062128f61adacf613b6ee05a0992abb9024`
- Donor parent: `21146cd6decaa1c15bca1753ca719f6937040798`
- Shared merge-base: `e9e3b8f78a103331c38b70c008bf020f13c46413`
- Mapping: all three allowed base files were unchanged from the merge-base, so the donor file bytes were preserved exactly. The worktree SHA-256 values and donor SHA-256 values are recorded in `facts.json`; all three compare equal.
- Donor delta SHA-256: `7f701395d628cea2103b4b28e20453f04ea6b9cbc90eb89636b255141a8ec9d5`
- Changed paths are exactly the three allowed files.
- Worktree AST, assertion-AST, reviewed-input-AST hashes equal the donor for every allowed file; syntax parsing passed.
- Protected review artifact: `PASS_SOURCE`; historical protected sample retained as `6 PASS / 2 FAIL / 0 errors / 0 skipped`. The two recipe failures remain visible and are not claimed as joined-source functional proof.

## Static acceptance

- `/home/user/work/venv-agent/bin/ruff check tests/editing_conformance/native_word_anchor_fixture.py tests/editing_conformance/test_native_word_anchor.py tests/editing_conformance/test_word_binding_recipe.py` — PASS.
- `/home/user/work/venv-agent/bin/mypy --follow-imports=skip tests/editing_conformance/native_word_anchor_fixture.py tests/editing_conformance/test_native_word_anchor.py tests/editing_conformance/test_word_binding_recipe.py` — PASS.
- `PYTHONPYCACHEPREFIX=/tmp/w-cd07f04b28/pycache /home/user/work/venv-agent/bin/python -m py_compile tests/editing_conformance/native_word_anchor_fixture.py tests/editing_conformance/test_native_word_anchor.py tests/editing_conformance/test_word_binding_recipe.py` — PASS.
- `git diff --check` — PASS.

No full, browser, service, body, P4, or functional suite was run.

