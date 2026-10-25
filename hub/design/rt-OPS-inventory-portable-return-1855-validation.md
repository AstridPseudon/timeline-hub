# Portable fixture first-return validation

Validated source head: `674d13e26ce40ce9a158a7e50b226c247fbc9588`.
Validated source tree: `f2abd214b4b45fa4a6b6de0932ad5371e4f3fc4b`.
The harness will commit the two worktree changes after worker exit, so these
are the exact source SHA/tree used for this validation.

Passed commands:

```text
PYTHONDONTWRITEBYTECODE=1 TMPDIR=$(mktemp -d /tmp/portable-return-tests.XXXXXX) PYTHONPATH=ops-child-custody/tests /home/user/work/venv-agent/bin/python -m unittest -v ops-child-custody/tests/test_e2e_inventory.py ops-child-custody/tests/test_custody.py ops-child-custody/tests/test_inventory.py  PASS (42/42)
/home/user/work/venv-agent/bin/python -m py_compile ops-child-custody/tests/e2e_inventory.py ops-child-custody/tests/test_e2e_inventory.py  PASS
AST parse of ops-child-custody/tests/e2e_inventory.py and ops-child-custody/tests/test_e2e_inventory.py  PASS
/home/user/work/venv-agent/bin/ruff check --no-cache ops-child-custody/tests/e2e_inventory.py ops-child-custody/tests/test_e2e_inventory.py  PASS
pyright ops-child-custody/tests/test_e2e_inventory.py  PASS (after removing the call-shape diagnostic)
git diff --check f6b9d4d52802d3cc5cd6bf9be070cd4c40d1e2fe..HEAD -- ops-child-custody/tests/e2e_inventory.py  PASS
git diff --no-index --check /dev/null ops-child-custody/tests/test_e2e_inventory.py  PASS for whitespace diagnostics; command exit 1 is the expected no-index-difference status
```

The optional whole-source Pyright invocation is not a repository-configured
typecheck and reports five pre-existing diagnostics in `e2e_inventory.py` at
`store_module`/final inventory typing; the additive test has no diagnostics.

Raw immutable-input diff check, retained honestly:

```text
git diff --check f6b9d4d52802d3cc5cd6bf9be070cd4c40d1e2fe..HEAD  exit 2
ops-child-custody/e2e-fixtures/tiny/makers/candidate-c3226b/make-child-venv:1224: new blank line at EOF.
ops-child-custody/e2e-fixtures/tiny/makers/parent-0857/make-child-venv:1201: new blank line at EOF.
```

Those are the two frozen maker diagnostics from the prior review. Their bytes,
modes, and historical EOF whitespace remain unchanged: parent SHA-256
`0857a5e0d9faeceb585b371f1f82cbf4b574ff20350974fd3c95f852e57b6d39`, candidate
SHA-256 `c3226b93d08e035f662ff57a7512522eb13f354acf2f13123999d71772e7142e`,
both mode `755`; the shared verifier block is
`f7c7ebcc26221958ce24e36025faad167c6015a2889202752d267e03d5eda209`.

No whole-maker E2E was attempted: available space was `4717395968`, below the
unchanged `5905580032` start reserve and above the unchanged `4000000000` stop
line. No Store initialization, production install/request, package
acquisition, sockets, browser, or new Git history was performed.
